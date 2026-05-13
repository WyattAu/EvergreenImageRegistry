package main

import (
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

func TestLivezHandler(t *testing.T) {
	startTime = time.Now()
	mux := newRouter()

	req := httptest.NewRequest("GET", "/livez", nil)
	rec := httptest.NewRecorder()
	mux.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Errorf("expected status 200, got %d", rec.Code)
	}
	if body := rec.Body.String(); body != "ok" {
		t.Errorf("expected body 'ok', got '%s'", body)
	}
}

func TestReadyzHandler(t *testing.T) {
	startTime = time.Now()
	mux := newRouter()

	req := httptest.NewRequest("GET", "/readyz", nil)
	rec := httptest.NewRecorder()
	mux.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Errorf("expected status 200, got %d", rec.Code)
	}
}

func TestStartupzHandler(t *testing.T) {
	startTime = time.Now()
	startupWindow = 30 * time.Second
	mux := newRouter()

	req := httptest.NewRequest("GET", "/startupz", nil)
	rec := httptest.NewRecorder()
	mux.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Errorf("expected status 200 during startup window, got %d", rec.Code)
	}
}

func TestMetricsHandler(t *testing.T) {
	startTime = time.Now()
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
}

func TestInfoHandler(t *testing.T) {
	startTime = time.Now()
	mux := newRouter()

	req := httptest.NewRequest("GET", "/", nil)
	rec := httptest.NewRecorder()
	mux.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Errorf("expected status 200, got %d", rec.Code)
	}
}

func TestUnknownPath(t *testing.T) {
	startTime = time.Now()
	mux := newRouter()

	req := httptest.NewRequest("GET", "/nonexistent", nil)
	rec := httptest.NewRecorder()
	mux.ServeHTTP(rec, req)

	if rec.Code != http.StatusNotFound {
		t.Errorf("expected status 404, got %d", rec.Code)
	}
}
