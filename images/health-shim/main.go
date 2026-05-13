// health-shim — Tiny HTTP health probe server for database images
//
// Serves /livez, /readyz, /startupz on port 9101 by wrapping
// native CLI health check commands (pg_isready, redis-cli ping, etc.)
//
// Build: CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /dev/null .
// Usage: HEALTH_CMD="pg_isready -h localhost" LISTEN=:9101 ./health-shim
//
// Environment Variables:
//   HEALTH_CMD     — CLI command to execute for liveness check (required)
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
	"fmt"
	"log/slog"
	"net"
	"net/http"
	"net/http/httptest"
	"net/url"
	"os"
	"os/exec"
	"strings"
	"sync"
	"sync/atomic"
	"time"
)

var (
	startTime      time.Time
	startupWindow  time.Duration
	healthTimeout  time.Duration
	healthCmd      string
	readyCmd       string
	startupCmd     string
	mu             sync.Mutex
	startupSuccess bool

	probeSuccessTotal = map[string]*uint64{}
	probeDuration     = map[string]*float64{}
	metricsMu         sync.RWMutex
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
	c.Env = os.Environ() // inherit container env for auth vars etc.

	output, err := c.CombinedOutput()
	if err != nil {
		return false, strings.TrimSpace(string(output))
	}
	return true, strings.TrimSpace(string(output))
}

func writeJSON(w http.ResponseWriter, status int, resp healthResponse) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(resp)
}

func handleLivez(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	cmd := healthCmd
	mu.Unlock()

	if cmd == "" {
		writeJSON(w, http.StatusServiceUnavailable, healthResponse{
			Status:    "error",
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Error:     "HEALTH_CMD not configured",
		})
		return
	}

	ok, output := runCheck(r.Context(), cmd)
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

func handleReadyz(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	cmd := readyCmd
	if cmd == "" {
		cmd = healthCmd
	}
	mu.Unlock()

	if cmd == "" {
		writeJSON(w, http.StatusServiceUnavailable, healthResponse{
			Status:    "error",
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Error:     "no readiness check configured",
		})
		return
	}

	ok, output := runCheck(r.Context(), cmd)
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
	mu.Lock()
	cmd := startupCmd
	if cmd == "" {
		cmd = healthCmd
	}
	mu.Unlock()

	if cmd == "" {
		writeJSON(w, http.StatusServiceUnavailable, healthResponse{
			Status:    "error",
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Error:     "no startup check configured",
		})
		return
	}

	// Once startup succeeds once, always return OK
	mu.Lock()
	if startupSuccess {
		mu.Unlock()
		writeJSON(w, http.StatusOK, healthResponse{
			Status:    "ok",
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Check:     cmd,
			Output:    "startup completed",
		})
		return
	}
	mu.Unlock()

	// During startup window, run the check
	elapsed := time.Since(startTime)
	if elapsed > startupWindow {
		// After startup window, assume started (fail-open to avoid infinite startup loops)
		mu.Lock()
		startupSuccess = true
		mu.Unlock()
		writeJSON(w, http.StatusOK, healthResponse{
			Status:    "ok",
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Check:     cmd,
			Output:    fmt.Sprintf("startup window expired (%v), assuming ready", startupWindow),
		})
		return
	}

	ok, output := runCheck(r.Context(), cmd)
	if ok {
		mu.Lock()
		startupSuccess = true
		mu.Unlock()
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
			Check:     "http://" + target,
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
	up := 1

	mu.Lock()
	startupOK := startupSuccess
	mu.Unlock()

	var sb strings.Builder
	sb.WriteString(fmt.Sprintf(`# HELP health_shim_up Whether the health shim is running
# TYPE health_shim_up gauge
health_shim_up %d
# HELP health_shim_uptime_seconds Seconds since health shim started
# TYPE health_shim_uptime_seconds gauge
health_shim_uptime_seconds %.0f
# HELP health_shim_startup_completed Whether startup probe has succeeded
# TYPE health_shim_startup_completed gauge
health_shim_startup_completed %d
# HELP health_shim_info Information about the health shim
# TYPE health_shim_info gauge
health_shim_info{health_cmd="%s",ready_cmd="%s",startup_cmd="%s"} 1
`, up, elapsed, boolToInt(startupOK), healthCmd, readyCmd, startupCmd))

	metricsMu.RLock()
	for name, total := range probeSuccessTotal {
		dur := probeDuration[name]
		sb.WriteString(fmt.Sprintf(`# HELP health_shim_probe_success_total Total number of successful probes
# TYPE health_shim_probe_success_total counter
health_shim_probe_success_total{probe="%s"} %d
# HELP health_shim_probe_duration_seconds Duration of last probe
# TYPE health_shim_probe_duration_seconds gauge
health_shim_probe_duration_seconds{probe="%s"} %.6f
`, name, atomic.LoadUint64(total), name, *dur))
	}
	metricsMu.RUnlock()

	w.Header().Set("Content-Type", "text/plain; version=0.0.4; charset=utf-8")
	w.WriteHeader(http.StatusOK)
	w.Write([]byte(sb.String()))
}

func boolToInt(b bool) int {
	if b {
		return 1
	}
	return 0
}

// newRouter creates and returns the HTTP mux with all routes registered.
func wrapProbe(name string, next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		rec := httptest.NewRecorder()
		next(rec, r)

		duration := time.Since(start)
		success := rec.Code == http.StatusOK
		recordProbe(name, success, duration)

		for k, vv := range rec.Header() {
			w.Header()[k] = vv
		}
		w.WriteHeader(rec.Code)
		w.Write(rec.Body.Bytes())
	}
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
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(map[string]string{
			"service":   "evergreen-health-shim",
			"version":   "1.0.0",
			"endpoints": "/livez, /readyz, /startupz, /tcp/<host>:<port>, /http/<url>, /cmd/<command>, /metrics",
		})
	})
	return mux
}

func main() {
	// Configure structured logging
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

	startTime = time.Now()

	// Read configuration
	healthCmd = os.Getenv("HEALTH_CMD")
	readyCmd = os.Getenv("READY_CMD")
	startupCmd = os.Getenv("STARTUP_CMD")

	listen := os.Getenv("LISTEN")
	if listen == "" {
		listen = ":9101"
	}

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

	if healthCmd == "" {
		slog.Error("HEALTH_CMD environment variable is required")
		os.Exit(1)
	}

	slog.Info("health-shim starting",
		"listen", listen,
		"health_cmd", healthCmd,
		"ready_cmd", readyCmd,
		"startup_cmd", startupCmd,
		"timeout", healthTimeout,
		"startup_window", startupWindow,
	)

	mux := newRouter()

	server := &http.Server{
		Addr:         listen,
		Handler:      mux,
		ReadTimeout:  5 * time.Second,
		WriteTimeout: 10 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	if err := server.ListenAndServe(); err != nil {
		slog.Error("health-shim server failed", "error", err)
		os.Exit(1)
	}
}
