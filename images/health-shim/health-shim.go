package main

import (
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"
)

var (
	startTime = time.Now()
	version   = "unknown"
)

func main() {
	port := os.Getenv("METRICS_PORT")
	if port == "" {
		port = "9101"
	}

	version = os.Getenv("IMAGE_VERSION")
	if version == "" {
		version = "dev"
	}

	mux := http.NewServeMux()
	mux.HandleFunc("/livez", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprint(w, "ok")
	})
	mux.HandleFunc("/readyz", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprint(w, "ok")
	})
	mux.HandleFunc("/metrics", func(w http.ResponseWriter, r *http.Request) {
		uptime := time.Since(startTime).Seconds()
		w.Header().Set("Content-Type", "text/plain; version=0.0.4")
		fmt.Fprintf(w, "# HELP sovereign_image_info Sovereign image metadata\n")
		fmt.Fprintf(w, "# TYPE sovereign_image_info gauge\n")
		fmt.Fprintf(w, "sovereign_image_info{version=\"%s\"} 1\n", version)
		fmt.Fprintf(w, "# HELP sovereign_up_seconds Time since image start\n")
		fmt.Fprintf(w, "# TYPE sovereign_up_seconds gauge\n")
		fmt.Fprintf(w, "sovereign_up_seconds %f\n", uptime)
	})

	server := &http.Server{
		Addr:    ":" + port,
		Handler: mux,
	}

	go func() {
		sigCh := make(chan os.Signal, 1)
		signal.Notify(sigCh, syscall.SIGTERM, syscall.SIGINT)
		<-sigCh
		server.Close()
	}()

	server.ListenAndServe()
}
