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
	"net/http"
	"os"
	"os/exec"
	"strings"
	"sync"
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

func handleMetrics(w http.ResponseWriter, r *http.Request) {
	elapsed := time.Since(startTime).Seconds()
	up := 1

	mu.Lock()
	startupOK := startupSuccess
	mu.Unlock()

	metrics := fmt.Sprintf(`# HELP health_shim_up Whether the health shim is running
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
`, up, elapsed, boolToInt(startupOK), healthCmd, readyCmd, startupCmd)

	w.Header().Set("Content-Type", "text/plain; version=0.0.4; charset=utf-8")
	w.WriteHeader(http.StatusOK)
	w.Write([]byte(metrics))
}

func boolToInt(b bool) int {
	if b {
		return 1
	}
	return 0
}

func main() {
	// Configure structured logging
	logLevel := os.Getenv("SOVEREIGN_LOG_LEVEL")
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

	mux := http.NewServeMux()
	mux.HandleFunc("/livez", handleLivez)
	mux.HandleFunc("/readyz", handleReadyz)
	mux.HandleFunc("/startupz", handleStartupz)
	mux.HandleFunc("/metrics", handleMetrics)

	// Also serve a basic info endpoint
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(map[string]string{
			"service": "sovereign-health-shim",
			"version": "1.0.0",
			"endpoints": "/livez, /readyz, /startupz, /metrics",
		})
	})

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
