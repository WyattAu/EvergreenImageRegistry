// health-shim — Tiny HTTP health probe server and process supervisor
//
// Serves /livez, /readyz, /startupz on port 9101 by wrapping
// native CLI health check commands (pg_isready, redis-cli ping, etc.)
//
// Three modes of operation:
//
//  1. Supervisor mode:    /shim run -c "/nginx"
//     Starts the child process, an HTTP health server, and forwards signals.
//     Child args with dashes (e.g. --appendonly, -g) are passed through
//     untouched since v1.2.0 (custom flag parser replaces flag.Parse).
//
//  2. One-shot healthcheck: /shim healthcheck --tcp 127.0.0.1:80
//     Performs a single TCP/HTTP/command probe and exits 0 or 1.
//
//  3. Standalone server:  HEALTH_CMD="pg_isready" ./shim
//     Legacy mode — serves HTTP health endpoints wrapping CLI checks.
//
// Build: CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /shim .
//
// Environment Variables (all modes):
//   HEALTH_CMD     — CLI command to execute for liveness check
//   READY_CMD      — CLI command for readiness check (defaults to HEALTH_CMD)
//   STARTUP_CMD    — CLI command for startup check (defaults to HEALTH_CMD)
//   LISTEN         — Listen address (default :9101)
//   HEALTH_TIMEOUT — Timeout per check in seconds (default 5)
//   STARTUP_WINDOW — Seconds after start during which startupz uses STARTUP_CMD (default 30)
//   LOG_LEVEL      — debug, info, warn, error (default info)

package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"log/slog"
	"net"
	"net/http"
	"net/url"
	"os"
	"os/exec"
	"os/signal"
	"strings"
	"sync"
	"sync/atomic"
	"syscall"
	"time"
)

var (
	startTime     time.Time
	startupWindow time.Duration
	healthTimeout time.Duration
	healthCmd     string
	readyCmd      string
	startupCmd    string

	startupDone atomic.Bool

	probeSuccessTotal = map[string]*uint64{}
	probeDuration     = map[string]*float64{}
	metricsMu         sync.RWMutex

	// Supervisor-mode state
	supervisorMode bool          // true when running via the "run" subcommand
	childAlive     atomic.Bool   // tracks child process liveness

	// version is set via -ldflags at build time
	version = "dev"
)

type healthResponse struct {
	Status    string `json:"status"`
	Timestamp string `json:"timestamp"`
	Check     string `json:"check,omitempty"`
	Output    string `json:"output,omitempty"`
	Error     string `json:"error,omitempty"`
}

func runCheck(ctx context.Context, cmd string) (bool, string) {
	ctx, cancel := context.WithTimeout(ctx, healthTimeout)
	defer cancel()

	parts := strings.Fields(cmd)
	if len(parts) == 0 {
		return false, "empty command"
	}

	c := exec.CommandContext(ctx, parts[0], parts[1:]...)
	c.Env = os.Environ() // inherit container env for auth variables etc.

	output, err := c.CombinedOutput()
	if err != nil {
		return false, strings.TrimSpace(string(output))
	}
	return true, strings.TrimSpace(string(output))
}

// performCheck dispatches the appropriate health check. In supervisor mode
// without an explicit command configured, it checks whether the child process
// is still running. Otherwise it executes the given CLI command.
func performCheck(ctx context.Context, cmd string) (bool, string) {
	if cmd == "" {
		if supervisorMode {
			if childAlive.Load() {
				return true, "child process running"
			}
			return false, "child process not running"
		}
		return false, "no health check configured"
	}
	return runCheck(ctx, cmd)
}

func writeJSON(w http.ResponseWriter, status int, resp healthResponse) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	if err := json.NewEncoder(w).Encode(resp); err != nil {
		slog.Error("failed to encode JSON response", "error", err)
	}
}

func handleLivez(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet && r.Method != http.MethodHead {
		w.Header().Set("Allow", "GET, HEAD")
		writeJSON(w, http.StatusMethodNotAllowed, healthResponse{Status: "error", Error: "method not allowed"})
		return
	}

	ok, output := performCheck(r.Context(), healthCmd)
	if ok {
		writeJSON(w, http.StatusOK, healthResponse{
			Status:    "ok",
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Check:     healthCmd,
			Output:    output,
		})
	} else {
		writeJSON(w, http.StatusServiceUnavailable, healthResponse{
			Status:    "error",
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Check:     healthCmd,
			Output:    output,
		})
	}
}

func handleReadyz(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet && r.Method != http.MethodHead {
		w.Header().Set("Allow", "GET, HEAD")
		writeJSON(w, http.StatusMethodNotAllowed, healthResponse{Status: "error", Error: "method not allowed"})
		return
	}

	cmd := readyCmd
	if cmd == "" {
		cmd = healthCmd
	}

	ok, output := performCheck(r.Context(), cmd)
	if ok {
		writeJSON(w, http.StatusOK, healthResponse{
			Status:    "ok",
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Check:     cmd,
			Output:    output,
		})
	} else {
		writeJSON(w, http.StatusServiceUnavailable, healthResponse{
			Status:    "error",
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Check:     cmd,
			Output:    output,
		})
	}
}

func handleStartupz(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet && r.Method != http.MethodHead {
		w.Header().Set("Allow", "GET, HEAD")
		writeJSON(w, http.StatusMethodNotAllowed, healthResponse{Status: "error", Error: "method not allowed"})
		return
	}

	cmd := startupCmd
	if cmd == "" {
		cmd = healthCmd
	}

	// Once startup succeeds once, always return OK (lock-free via atomic)
	if startupDone.Load() {
		writeJSON(w, http.StatusOK, healthResponse{
			Status:    "ok",
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Check:     cmd,
			Output:    "startup completed",
		})
		return
	}

	// During startup window, run the check
	elapsed := time.Since(startTime)
	if elapsed > startupWindow {
		// After startup window, assume started (fail-open to avoid infinite startup loops)
		startupDone.Store(true)
		writeJSON(w, http.StatusOK, healthResponse{
			Status:    "ok",
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Check:     cmd,
			Output:    fmt.Sprintf("startup window expired (%v), assuming ready", startupWindow),
		})
		return
	}

	ok, output := performCheck(r.Context(), cmd)
	if ok {
		startupDone.Store(true)
		writeJSON(w, http.StatusOK, healthResponse{
			Status:    "ok",
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Check:     cmd,
			Output:    output,
		})
	} else {
		writeJSON(w, http.StatusServiceUnavailable, healthResponse{
			Status:    "error",
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Check:     cmd,
			Output:    output,
		})
	}
}

func recordProbe(name string, success bool, duration time.Duration) {
	metricsMu.Lock()
	if probeSuccessTotal[name] == nil {
		probeSuccessTotal[name] = new(uint64)
		probeDuration[name] = new(float64)
	}
	if success {
		atomic.AddUint64(probeSuccessTotal[name], 1)
	}
	*probeDuration[name] = duration.Seconds()
	metricsMu.Unlock()
}

func handleTCPProbe(w http.ResponseWriter, r *http.Request) {
	target := strings.TrimPrefix(r.URL.Path, "/tcp/")
	if target == "" {
		writeJSON(w, http.StatusBadRequest, healthResponse{
			Status:    "error",
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Error:     "missing host:port in /tcp/<host>:<port>",
		})
		return
	}

	start := time.Now()
	conn, err := net.DialTimeout("tcp", target, healthTimeout)
	duration := time.Since(start)

	if err != nil {
		recordProbe("tcp", false, duration)
		writeJSON(w, http.StatusServiceUnavailable, healthResponse{
			Status:    "error",
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Check:     "tcp://" + target,
			Error:     err.Error(),
		})
		return
	}
	conn.Close()

	recordProbe("tcp", true, duration)
	writeJSON(w, http.StatusOK, healthResponse{
		Status:    "ok",
		Timestamp: time.Now().UTC().Format(time.RFC3339),
		Check:     "tcp://" + target,
		Output:    fmt.Sprintf("connected in %v", duration),
	})
}

func handleHTTPProbe(w http.ResponseWriter, r *http.Request) {
	target := strings.TrimPrefix(r.URL.Path, "/http/")
	if target == "" {
		writeJSON(w, http.StatusBadRequest, healthResponse{
			Status:    "error",
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Error:     "missing URL in /http/<url>",
		})
		return
	}

	if !strings.HasPrefix(target, "http://") && !strings.HasPrefix(target, "https://") {
		target = "http://" + target
	}

	client := &http.Client{Timeout: healthTimeout}
	start := time.Now()
	resp, err := client.Get(target)
	duration := time.Since(start)

	if err != nil {
		recordProbe("http", false, duration)
		writeJSON(w, http.StatusServiceUnavailable, healthResponse{
			Status:    "error",
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Check:     target,
			Error:     err.Error(),
		})
		return
	}
	resp.Body.Close()

	success := resp.StatusCode >= 200 && resp.StatusCode < 400
	recordProbe("http", success, duration)

	if success {
		writeJSON(w, http.StatusOK, healthResponse{
			Status:    "ok",
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Check:     target,
			Output:    fmt.Sprintf("HTTP %d in %v", resp.StatusCode, duration),
		})
	} else {
		writeJSON(w, http.StatusServiceUnavailable, healthResponse{
			Status:    "error",
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Check:     target,
			Output:    fmt.Sprintf("HTTP %d", resp.StatusCode),
		})
	}
}

func handleCmdProbe(w http.ResponseWriter, r *http.Request) {
	command := strings.TrimPrefix(r.URL.Path, "/cmd/")
	if command == "" {
		writeJSON(w, http.StatusBadRequest, healthResponse{
			Status:    "error",
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Error:     "missing command in /cmd/<command>",
		})
		return
	}

	command, err := url.PathUnescape(command)
	if err != nil {
		writeJSON(w, http.StatusBadRequest, healthResponse{
			Status:    "error",
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Error:     fmt.Sprintf("invalid command encoding: %v", err),
		})
		return
	}

	start := time.Now()
	ok, output := runCheck(r.Context(), command)
	duration := time.Since(start)

	recordProbe("cmd", ok, duration)

	if ok {
		writeJSON(w, http.StatusOK, healthResponse{
			Status:    "ok",
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Check:     command,
			Output:    output,
		})
	} else {
		writeJSON(w, http.StatusServiceUnavailable, healthResponse{
			Status:    "error",
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Check:     command,
			Output:    output,
		})
	}
}

func handleMetrics(w http.ResponseWriter, r *http.Request) {
	elapsed := time.Since(startTime).Seconds()
	startupOK := startupDone.Load()

	var sb strings.Builder
	fmt.Fprintf(&sb, `# HELP health_shim_up Whether the health shim is running
# TYPE health_shim_up gauge
health_shim_up 1
# HELP health_shim_uptime_seconds Seconds since health shim started
# TYPE health_shim_uptime_seconds gauge
health_shim_uptime_seconds %.0f
# HELP health_shim_startup_completed Whether startup probe has succeeded
# TYPE health_shim_startup_completed gauge
health_shim_startup_completed %d
# HELP health_shim_info Information about the health shim
# TYPE health_shim_info gauge
health_shim_info{health_cmd=%q,ready_cmd=%q,startup_cmd=%q} 1
`, elapsed, boolToInt(startupOK), healthCmd, readyCmd, startupCmd)

	metricsMu.RLock()
	if len(probeSuccessTotal) > 0 {
		sb.WriteString("# HELP health_shim_probe_success_total Total number of successful probes\n")
		sb.WriteString("# TYPE health_shim_probe_success_total counter\n")
		for name, total := range probeSuccessTotal {
			fmt.Fprintf(&sb, "health_shim_probe_success_total{probe=%q} %d\n", name, atomic.LoadUint64(total))
		}
		sb.WriteString("# HELP health_shim_probe_duration_seconds Duration of last probe\n")
		sb.WriteString("# TYPE health_shim_probe_duration_seconds gauge\n")
		for name, dur := range probeDuration {
			fmt.Fprintf(&sb, "health_shim_probe_duration_seconds{probe=%q} %.6f\n", name, *dur)
		}
	}
	metricsMu.RUnlock()

	w.Header().Set("Content-Type", "text/plain; version=0.0.4; charset=utf-8")
	w.WriteHeader(http.StatusOK)
	if _, err := w.Write([]byte(sb.String())); err != nil {
		slog.Error("failed to write metrics response", "error", err)
	}
}

func boolToInt(b bool) int {
	if b {
		return 1
	}
	return 0
}

// wrapProbe records metrics for probe endpoints without buffering the response.
func wrapProbe(name string, next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		rec := &statusRecorder{ResponseWriter: w, statusCode: http.StatusOK}
		next(rec, r)
		duration := time.Since(start)
		success := rec.statusCode >= 200 && rec.statusCode < 400
		recordProbe(name, success, duration)
	}
}

// statusRecorder wraps http.ResponseWriter to capture the status code.
type statusRecorder struct {
	http.ResponseWriter
	statusCode int
}

func (r *statusRecorder) WriteHeader(code int) {
	r.statusCode = code
	r.ResponseWriter.WriteHeader(code)
}

func newRouter() *http.ServeMux {
	mux := http.NewServeMux()
	mux.HandleFunc("/livez", wrapProbe("livez", handleLivez))
	mux.HandleFunc("/readyz", wrapProbe("readyz", handleReadyz))
	mux.HandleFunc("/startupz", wrapProbe("startupz", handleStartupz))
	mux.HandleFunc("/tcp/", handleTCPProbe)
	mux.HandleFunc("/http/", handleHTTPProbe)
	mux.HandleFunc("/cmd/", handleCmdProbe)
	mux.HandleFunc("/metrics", handleMetrics)
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		// Only match exact "/" — ServeMux sends all unmatched paths here
		if r.URL.Path != "/" {
			writeJSON(w, http.StatusNotFound, healthResponse{
				Status:    "error",
				Timestamp: time.Now().UTC().Format(time.RFC3339),
				Error:     "not found",
			})
			return
		}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(map[string]string{
			"service":   "evergreen-health-shim",
			"version":   version,
			"endpoints": "/livez, /readyz, /startupz, /tcp/<host>:<port>, /http/<url>, /cmd/<command>, /metrics",
		})
	})
	return mux
}

// ---------------------------------------------------------------------------
// Configuration helpers
// ---------------------------------------------------------------------------

// initLogging configures structured JSON logging from the EVERGREEN_LOG_LEVEL
// or LOG_LEVEL environment variable.
func initLogging() {
	logLevel := os.Getenv("EVERGREEN_LOG_LEVEL")
	if logLevel == "" {
		logLevel = os.Getenv("LOG_LEVEL")
	}
	if logLevel == "" {
		logLevel = "info"
	}

	var level slog.Level
	switch strings.ToLower(logLevel) {
	case "debug":
		level = slog.LevelDebug
	case "warn", "warning":
		level = slog.LevelWarn
	case "error":
		level = slog.LevelError
	default:
		level = slog.LevelInfo
	}

	logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: level}))
	slog.SetDefault(logger)
}

// loadEnvConfig reads configuration from environment variables into package
// globals. It is safe to call in any mode.
func loadEnvConfig() {
	healthCmd = os.Getenv("HEALTH_CMD")
	readyCmd = os.Getenv("READY_CMD")
	startupCmd = os.Getenv("STARTUP_CMD")

	timeoutStr := os.Getenv("HEALTH_TIMEOUT")
	if timeoutStr == "" {
		timeoutStr = "5"
	}
	var err error
	healthTimeout, err = time.ParseDuration(timeoutStr + "s")
	if err != nil {
		slog.Error("invalid HEALTH_TIMEOUT", "value", timeoutStr, "error", err)
		os.Exit(1)
	}

	windowStr := os.Getenv("STARTUP_WINDOW")
	if windowStr == "" {
		windowStr = "30"
	}
	startupWindow, err = time.ParseDuration(windowStr + "s")
	if err != nil {
		slog.Error("invalid STARTUP_WINDOW", "value", windowStr, "error", err)
		os.Exit(1)
	}
}

// listenAddr returns the configured listen address.
func listenAddr() string {
	listen := os.Getenv("LISTEN")
	if listen == "" {
		return ":9101"
	}
	return listen
}

// newHealthServer creates an *http.Server with standard timeouts.
func newHealthServer(listen string) *http.Server {
	return &http.Server{
		Addr:         listen,
		Handler:      newRouter(),
		ReadTimeout:  5 * time.Second,
		WriteTimeout: 10 * time.Second,
		IdleTimeout:  60 * time.Second,
	}
}

// ---------------------------------------------------------------------------
// Subcommand: run (process supervisor)
// ---------------------------------------------------------------------------

// runSupervisor starts a child process alongside the HTTP health server,
// forwards signals, and exits with the child's exit code.
func runSupervisor(args []string) {
	// We manually parse -c instead of using flag.Parse() because Go's flag
	// package would intercept any dash-prefixed args (e.g. --appendonly, -g,
	// --homepath) that are actually meant for the child process.  This custom
	// parser extracts ONLY the -c flag and treats everything else as the
	// command to supervise.
	var cmdStr string
	var remaining []string

	// Show help only if -c hasn't been seen yet. Once -c is set, --help
	// and -h belong to the child process and must pass through untouched.
	for i := 0; i < len(args); i++ {
		switch {
		case args[i] == "-c" || args[i] == "--c":
			if i+1 >= len(args) {
				fmt.Fprintln(os.Stderr, "flag needs an argument: -c")
				os.Exit(2)
			}
			cmdStr = args[i+1]
			i++ // skip the value
		case strings.HasPrefix(args[i], "-c="):
			cmdStr = strings.TrimPrefix(args[i], "-c=")
		case strings.HasPrefix(args[i], "--c="):
			cmdStr = strings.TrimPrefix(args[i], "--c=")
		case (args[i] == "-h" || args[i] == "--help" || args[i] == "help") && cmdStr == "":
			fmt.Fprintf(os.Stderr, `usage: shim run [-c command] [args...]

Start a child process with an HTTP health server on port 9101.

Options:
  -c string   command to run as a supervised child process

If -c is omitted, positional args are used as the command.
If no command is given, only the HTTP server runs.

Examples:
  shim run -c /nginx
  shim run -c "redis-server --appendonly yes"
  shim run redis-server   # positional form
`)
			return
		case args[i] == "--":
			// Everything after -- is the child command verbatim.
			remaining = append(remaining, args[i+1:]...)
			i = len(args) // stop scanning
		default:
			// First non-flag arg: this and ALL remaining args are the command.
			// We stop parsing here so child flags like -g / --port are preserved.
			remaining = append(remaining, args[i:]...)
			i = len(args) // stop scanning
		}
	}

	// If no -c flag, treat remaining positional args as the command.
	if cmdStr == "" && len(remaining) > 0 {
		cmdStr = strings.Join(remaining, " ")
	} else if cmdStr != "" && len(remaining) > 0 {
		// -c provided a base command, append extra positional args.
		cmdStr = cmdStr + " " + strings.Join(remaining, " ")
	}

	loadEnvConfig()
	supervisorMode = true

	// In supervisor mode without an explicit HEALTH_CMD, liveness is derived
	// from whether the child process is running (see performCheck).
	healthCmdExplicit := os.Getenv("HEALTH_CMD") != ""
	if healthCmdExplicit {
		slog.Info("supervisor mode: using explicit HEALTH_CMD", "health_cmd", healthCmd)
	}

	listen := listenAddr()

	slog.Info("health-shim starting (supervisor mode)",
		"listen", listen,
		"command", cmdStr,
		"health_cmd", healthCmd,
		"ready_cmd", readyCmd,
		"startup_cmd", startupCmd,
		"timeout", healthTimeout,
		"startup_window", startupWindow,
	)

	// Start the HTTP health server in the background.
	server := newHealthServer(listen)
	go func() {
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			slog.Error("health server failed", "error", err)
			os.Exit(1)
		}
	}()
	slog.Info("health server listening", "listen", listen)

	// If no child command was provided, just serve until signalled.
	if cmdStr == "" {
		slog.Info("no child command specified; running as standalone health server")
		sigCh := make(chan os.Signal, 1)
		signal.Notify(sigCh, syscall.SIGTERM, syscall.SIGINT)
		sig := <-sigCh
		slog.Info("received signal, shutting down", "signal", sig)
		shutdownCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()
		server.Shutdown(shutdownCtx)
		return
	}

	// Start the child process in its own process group so we can forward
	// signals to the entire group (covers grandchild processes).
	parts := strings.Fields(cmdStr)
	if len(parts) == 0 {
		slog.Error("invalid command", "command", cmdStr)
		os.Exit(1)
	}

	child := exec.Command(parts[0], parts[1:]...)
	child.Stdin = os.Stdin
	child.Stdout = os.Stdout
	child.Stderr = os.Stderr
	child.Env = os.Environ()
	child.SysProcAttr = &syscall.SysProcAttr{Setpgid: true}

	if err := child.Start(); err != nil {
		slog.Error("failed to start child process", "command", cmdStr, "error", err)
		os.Exit(1)
	}

	childAlive.Store(true)
	startupDone.Store(true)
	slog.Info("child process started", "command", cmdStr, "pid", child.Process.Pid)

	// Forward SIGTERM and SIGINT to the child's process group.
	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGTERM, syscall.SIGINT)
	go func() {
		for sig := range sigCh {
			slog.Info("forwarding signal to child", "signal", sig.String())
			if child.Process != nil {
				// Negative PID targets the entire process group.
				if err := syscall.Kill(-child.Process.Pid, sig.(syscall.Signal)); err != nil {
					slog.Warn("failed to forward signal", "signal", sig.String(), "error", err)
				}
			}
		}
	}()

	// Block until the child exits.
	waitErr := child.Wait()
	childAlive.Store(false)

	slog.Info("child process exited", "error", waitErr)

	// Stop accepting signals before shutting down the server.
	signal.Stop(sigCh)

	// Gracefully shut down the HTTP server.
	shutdownCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	if err := server.Shutdown(shutdownCtx); err != nil {
		slog.Error("server shutdown error", "error", err)
	}

	// Propagate the child's exit code.
	if waitErr != nil {
		if exitErr, ok := waitErr.(*exec.ExitError); ok {
			code := exitErr.ExitCode()
			if code < 0 {
				code = 1
			}
			os.Exit(code)
		}
		slog.Error("child process wait error", "error", waitErr)
		os.Exit(1)
	}
	os.Exit(0)
}

// ---------------------------------------------------------------------------
// Subcommand: healthcheck (one-shot probe)
// ---------------------------------------------------------------------------

// runHealthcheck performs a single health probe and exits 0 (healthy) or 1
// (unhealthy). Exactly one of --tcp, --http, or --cmd must be specified.
func runHealthcheck(args []string) {
	fs := flag.NewFlagSet("healthcheck", flag.ExitOnError)
	fs.Usage = func() {
		fmt.Fprintf(fs.Output(), "usage: shim healthcheck [options]\n\n")
		fmt.Fprintf(fs.Output(), "Perform a one-shot health probe and exit 0 (healthy) or 1 (unhealthy).\n\n")
		fmt.Fprintf(fs.Output(), "Options:\n")
		fs.PrintDefaults()
		fmt.Fprintf(fs.Output(), "\nExamples:\n")
		fmt.Fprintf(fs.Output(), "  shim healthcheck --tcp 127.0.0.1:80\n")
		fmt.Fprintf(fs.Output(), "  shim healthcheck --http 127.0.0.1:9000/healthz\n")
		fmt.Fprintf(fs.Output(), "  shim healthcheck --cmd \"redis-cli ping\"\n")
	}
	var tcpTarget string
	var httpTarget string
	var cmdTarget string
	var timeoutSec int
	fs.StringVar(&tcpTarget, "tcp", "", "TCP target in host:port format")
	fs.StringVar(&httpTarget, "http", "", "HTTP target URL")
	fs.StringVar(&cmdTarget, "cmd", "", "command to execute")
	fs.IntVar(&timeoutSec, "timeout", 5, "probe timeout in seconds")
	fs.Parse(args)

	if fs.NFlag() == 0 {
		fs.Usage()
		os.Exit(1)
	}

	timeout := time.Duration(timeoutSec) * time.Second

	// --- TCP probe ---
	if tcpTarget != "" {
		conn, err := net.DialTimeout("tcp", tcpTarget, timeout)
		if err != nil {
			fmt.Fprintf(os.Stderr, "TCP healthcheck failed: %s — %v\n", tcpTarget, err)
			os.Exit(1)
		}
		conn.Close()
		os.Exit(0)
	}

	// --- HTTP probe ---
	if httpTarget != "" {
		if !strings.HasPrefix(httpTarget, "http://") && !strings.HasPrefix(httpTarget, "https://") {
			httpTarget = "http://" + httpTarget
		}
		client := &http.Client{Timeout: timeout}
		resp, err := client.Get(httpTarget)
		if err != nil {
			fmt.Fprintf(os.Stderr, "HTTP healthcheck failed: %s — %v\n", httpTarget, err)
			os.Exit(1)
		}
		resp.Body.Close()
		if resp.StatusCode >= 200 && resp.StatusCode < 400 {
			os.Exit(0)
		}
		fmt.Fprintf(os.Stderr, "HTTP healthcheck failed: %s — status %d\n", httpTarget, resp.StatusCode)
		os.Exit(1)
	}

	// --- Command probe ---
	if cmdTarget != "" {
		ctx, cancel := context.WithTimeout(context.Background(), timeout)
		defer cancel()
		parts := strings.Fields(cmdTarget)
		if len(parts) == 0 {
			fmt.Fprintln(os.Stderr, "healthcheck: --cmd value is empty")
			os.Exit(1)
		}
		c := exec.CommandContext(ctx, parts[0], parts[1:]...)
		c.Env = os.Environ()
		output, err := c.CombinedOutput()
		if err != nil {
			fmt.Fprintf(os.Stderr, "command healthcheck failed: %s\n", strings.TrimSpace(string(output)))
			os.Exit(1)
		}
		os.Exit(0)
	}

	// Should not reach here if fs.NFlag() == 0 check passed, but guard anyway.
	fmt.Fprintln(os.Stderr, "healthcheck: specify one of --tcp, --http, or --cmd")
	os.Exit(1)
}

// ---------------------------------------------------------------------------
// Subcommand: none (legacy standalone HTTP server)
// ---------------------------------------------------------------------------

// runStandalone runs the original HTTP-only health server. This preserves
// backward compatibility when the binary is invoked without a subcommand.
func runStandalone() {
	loadEnvConfig()

	if healthCmd == "" {
		slog.Error("HEALTH_CMD environment variable is required")
		os.Exit(1)
	}

	listen := listenAddr()

	slog.Info("health-shim starting (standalone mode)",
		"listen", listen,
		"health_cmd", healthCmd,
		"ready_cmd", readyCmd,
		"startup_cmd", startupCmd,
		"timeout", healthTimeout,
		"startup_window", startupWindow,
	)

	server := newHealthServer(listen)

	const shutdownTimeout = 5 * time.Second

	// Graceful shutdown on SIGTERM/SIGINT
	ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGTERM, syscall.SIGINT)
	defer stop()

	go func() {
		<-ctx.Done()
		slog.Info("shutting down gracefully", "timeout", shutdownTimeout)
		shutdownCtx, cancel := context.WithTimeout(context.Background(), shutdownTimeout)
		defer cancel()
		if err := server.Shutdown(shutdownCtx); err != nil {
			slog.Error("server shutdown error", "error", err)
		}
	}()

	if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
		slog.Error("health-shim server failed", "error", err)
		os.Exit(1)
	}
	slog.Info("health-shim stopped")
}

// ---------------------------------------------------------------------------
// Entry point
// ---------------------------------------------------------------------------

func main() {
	initLogging()
	startTime = time.Now()

	// Subcommand dispatch.
	if len(os.Args) >= 2 {
		switch os.Args[1] {
		case "run":
			runSupervisor(os.Args[2:])
			return
		case "healthcheck":
			runHealthcheck(os.Args[2:])
			return
		case "help", "-h", "--help":
			printUsage()
			return
		}
	}

	// No subcommand — backward-compatible standalone HTTP server.
	runStandalone()
}

func printUsage() {
	fmt.Fprintf(os.Stderr, `evergreen health-shim %s

Usage:
  shim <subcommand> [options]
  shim                           Run as standalone HTTP health server (legacy)

Subcommands:
  run          Start a child process with HTTP health server (supervisor mode)
  healthcheck  Perform a one-shot TCP/HTTP/command probe

Examples:
  shim run -c /nginx                              Supervise nginx
  shim run -c "redis-server --appendonly yes"     Supervise redis
  shim healthcheck --tcp 127.0.0.1:80             One-shot TCP probe
  shim healthcheck --http localhost:9000/healthz  One-shot HTTP probe
  HEALTH_CMD="pg_isready" shim                    Legacy standalone server

Environment:
  HEALTH_CMD      CLI command for liveness check
  READY_CMD       CLI command for readiness (defaults to HEALTH_CMD)
  STARTUP_CMD     CLI command for startup (defaults to HEALTH_CMD)
  LISTEN          Listen address (default :9101)
  HEALTH_TIMEOUT  Timeout per check in seconds (default 5)
  STARTUP_WINDOW  Startup probe window in seconds (default 30)
  LOG_LEVEL       Log level: debug, info, warn, error (default info)

`, version)
}
