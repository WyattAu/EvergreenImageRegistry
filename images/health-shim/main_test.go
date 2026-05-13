package main

import (
	"encoding/json"
	"net"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"
)

func resetState() {
	healthCmd = "echo ok"
	readyCmd = ""
	startupCmd = ""
	healthTimeout = 5 * time.Second
	startupWindow = 30 * time.Second
	startTime = time.Now()
	mu.Lock()
	startupSuccess = false
	mu.Unlock()
	metricsMu.Lock()
	for k := range probeSuccessTotal {
		delete(probeSuccessTotal, k)
		delete(probeDuration, k)
	}
	metricsMu.Unlock()
}

func TestLivezHandler(t *testing.T) {
	resetState()
	mux := newRouter()

	req := httptest.NewRequest("GET", "/livez", nil)
	rec := httptest.NewRecorder()
	mux.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Errorf("expected status 200, got %d", rec.Code)
	}
	var resp healthResponse
	if err := json.NewDecoder(rec.Body).Decode(&resp); err != nil {
		t.Fatalf("failed to decode JSON: %v", err)
	}
	if resp.Status != "ok" {
		t.Errorf("expected status ok, got %s", resp.Status)
	}
}

func TestReadyzHandler(t *testing.T) {
	resetState()
	mux := newRouter()

	req := httptest.NewRequest("GET", "/readyz", nil)
	rec := httptest.NewRecorder()
	mux.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Errorf("expected status 200, got %d", rec.Code)
	}
}

func TestStartupzHandler(t *testing.T) {
	resetState()
	mux := newRouter()

	req := httptest.NewRequest("GET", "/startupz", nil)
	rec := httptest.NewRecorder()
	mux.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Errorf("expected status 200 during startup window, got %d", rec.Code)
	}
}

func TestMetricsHandler(t *testing.T) {
	resetState()
	mux := newRouter()

	req := httptest.NewRequest("GET", "/metrics", nil)
	rec := httptest.NewRecorder()
	mux.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Errorf("expected status 200, got %d", rec.Code)
	}
	ct := rec.Header().Get("Content-Type")
	if ct != "text/plain; version=0.0.4; charset=utf-8" {
		t.Errorf("expected Prometheus text format, got '%s'", ct)
	}
	body := rec.Body.String()
	if !strings.Contains(body, "health_shim_up 1") {
		t.Error("metrics missing health_shim_up")
	}
	if !strings.Contains(body, "health_shim_uptime_seconds") {
		t.Error("metrics missing health_shim_uptime_seconds")
	}
	if !strings.Contains(body, "health_shim_startup_completed") {
		t.Error("metrics missing health_shim_startup_completed")
	}
}

func TestMetricsProbeCounters(t *testing.T) {
	resetState()
	mux := newRouter()

	mux.ServeHTTP(httptest.NewRecorder(), httptest.NewRequest("GET", "/livez", nil))
	mux.ServeHTTP(httptest.NewRecorder(), httptest.NewRequest("GET", "/livez", nil))

	req := httptest.NewRequest("GET", "/metrics", nil)
	rec := httptest.NewRecorder()
	mux.ServeHTTP(rec, req)

	body := rec.Body.String()
	if !strings.Contains(body, `health_shim_probe_success_total{probe="livez"} 2`) {
		t.Errorf("expected livez probe count 2, got:\n%s", body)
	}
	if !strings.Contains(body, `health_shim_probe_duration_seconds{probe="livez"}`) {
		t.Errorf("expected livez probe duration, got:\n%s", body)
	}
}

func TestTCPProbeHandler(t *testing.T) {
	resetState()
	mux := newRouter()

	ln, err := newTCPListener()
	if err != nil {
		t.Fatalf("failed to create listener: %v", err)
	}
	defer ln.Close()

	req := httptest.NewRequest("GET", "/tcp/"+ln.Addr().String(), nil)
	rec := httptest.NewRecorder()
	mux.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Errorf("expected status 200, got %d: %s", rec.Code, rec.Body.String())
	}
	var resp healthResponse
	if err := json.NewDecoder(rec.Body).Decode(&resp); err != nil {
		t.Fatalf("failed to decode JSON: %v", err)
	}
	if resp.Status != "ok" {
		t.Errorf("expected status ok, got %s", resp.Status)
	}
}

func TestTCPProbeFailure(t *testing.T) {
	resetState()
	mux := newRouter()

	req := httptest.NewRequest("GET", "/tcp/127.0.0.1:1", nil)
	rec := httptest.NewRecorder()
	mux.ServeHTTP(rec, req)

	if rec.Code != http.StatusServiceUnavailable {
		t.Errorf("expected status 503, got %d", rec.Code)
	}
}

func TestHTTPProbeHandler(t *testing.T) {
	resetState()
	mux := newRouter()

	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
	}))
	defer ts.Close()

	u := strings.TrimPrefix(ts.URL, "http://")
	req := httptest.NewRequest("GET", "/http/"+u, nil)
	rec := httptest.NewRecorder()
	mux.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Errorf("expected status 200, got %d: %s", rec.Code, rec.Body.String())
	}
	var resp healthResponse
	if err := json.NewDecoder(rec.Body).Decode(&resp); err != nil {
		t.Fatalf("failed to decode JSON: %v", err)
	}
	if resp.Status != "ok" {
		t.Errorf("expected status ok, got %s", resp.Status)
	}
}

func TestHTTPProbeBadStatus(t *testing.T) {
	resetState()
	mux := newRouter()

	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusInternalServerError)
	}))
	defer ts.Close()

	u := strings.TrimPrefix(ts.URL, "http://")
	req := httptest.NewRequest("GET", "/http/"+u, nil)
	rec := httptest.NewRecorder()
	mux.ServeHTTP(rec, req)

	if rec.Code != http.StatusServiceUnavailable {
		t.Errorf("expected status 503, got %d", rec.Code)
	}
}

func TestCmdProbeSuccess(t *testing.T) {
	resetState()
	mux := newRouter()

	req := httptest.NewRequest("GET", "/cmd/echo%20hello", nil)
	rec := httptest.NewRecorder()
	mux.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Errorf("expected status 200, got %d: %s", rec.Code, rec.Body.String())
	}
	var resp healthResponse
	if err := json.NewDecoder(rec.Body).Decode(&resp); err != nil {
		t.Fatalf("failed to decode JSON: %v", err)
	}
	if resp.Status != "ok" {
		t.Errorf("expected status ok, got %s", resp.Status)
	}
	if resp.Output != "hello" {
		t.Errorf("expected output 'hello', got '%s'", resp.Output)
	}
}

func TestCmdProbeFailure(t *testing.T) {
	resetState()
	mux := newRouter()

	req := httptest.NewRequest("GET", "/cmd/false", nil)
	rec := httptest.NewRecorder()
	mux.ServeHTTP(rec, req)

	if rec.Code != http.StatusServiceUnavailable {
		t.Errorf("expected status 503, got %d: %s", rec.Code, rec.Body.String())
	}
	var resp healthResponse
	if err := json.NewDecoder(rec.Body).Decode(&resp); err != nil {
		t.Fatalf("failed to decode JSON: %v", err)
	}
	if resp.Status != "error" {
		t.Errorf("expected status error, got %s", resp.Status)
	}
}

func TestInfoHandler(t *testing.T) {
	resetState()
	mux := newRouter()

	req := httptest.NewRequest("GET", "/", nil)
	rec := httptest.NewRecorder()
	mux.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Errorf("expected status 200, got %d", rec.Code)
	}
}

func TestUnknownPath(t *testing.T) {
	resetState()
	mux := newRouter()

	req := httptest.NewRequest("GET", "/nonexistent", nil)
	rec := httptest.NewRecorder()
	mux.ServeHTTP(rec, req)

	if rec.Code != http.StatusNotFound {
		t.Errorf("expected status 404, got %d", rec.Code)
	}
}

func newTCPListener() (net.Listener, error) {
	return net.Listen("tcp", "127.0.0.1:0")
}
