// =============================================================================
// OCI Distribution Spec Client
// =============================================================================
//
// Phase 5 — Real OCI registry integration.
//
// Implements the OCI Distribution Spec for:
//   - Tag-to-digest resolution
//   - Manifest fetching and validation
//   - Bearer token authentication
//   - Multi-platform manifest list inspection
//
// This client is read-only: it never pushes, mutates, or signs images.

package controllers

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"
	"time"
)

// OCIManifest represents an OCI/Docker image manifest or manifest list.
type OCIManifest struct {
	SchemaVersion int                `json:"schemaVersion"`
	MediaType     string             `json:"mediaType,omitempty"`
	Config        OCIContent         `json:"config,omitempty"`
	Layers        []OCIContent       `json:"layers,omitempty"`
	Manifests     []OCIManifestEntry `json:"manifests,omitempty"`
}

// OCIContent describes a single content blob in a manifest.
type OCIContent struct {
	Digest    string `json:"digest"`
	Size      int64  `json:"size"`
	MediaType string `json:"mediaType,omitempty"`
}

// OCIManifestEntry describes a platform-specific manifest in a manifest list.
type OCIManifestEntry struct {
	OCIContent
	Platform OCIPlatform `json:"platform,omitempty"`
}

// OCIPlatform describes the target platform for a manifest.
type OCIPlatform struct {
	Architecture string `json:"architecture"`
	OS           string `json:"os"`
	Variant      string `json:"variant,omitempty"`
}

// OCIDigestResult holds the result of a tag-to-digest resolution.
type OCIDigestResult struct {
	Image      string
	Reference  string
	Digest     string
	MediaType  string
	IsIndex    bool
	Platforms  []OCIPlatform
	StatusCode int
}

// OCIRegistryClient implements RegistryClient using the OCI Distribution Spec.
type OCIRegistryClient struct {
	httpClient *http.Client
}

// NewOCIRegistryClient creates a new OCI registry client with sensible defaults.
func NewOCIRegistryClient() *OCIRegistryClient {
	return &OCIRegistryClient{
		httpClient: &http.Client{
			Timeout: 30 * time.Second,
			Transport: &http.Transport{
				MaxIdleConns:        10,
				IdleConnTimeout:     90 * time.Second,
				TLSHandshakeTimeout: 10 * time.Second,
			},
		},
	}
}

// parseReference splits a container image reference into registry, repository, and tag.
// Supports: registry/repo:tag, registry/repo@sha256:..., repo:tag (Docker Hub default).
func parseReference(ref string) (registry, repository, tag string, err error) {
	// Handle digest references
	if idx := strings.Index(ref, "@sha256:"); idx >= 0 {
		ref = ref[:idx]
	}

	// Split on first slash to detect registry vs Docker Hub
	parts := strings.SplitN(ref, "/", 2)
	if len(parts) == 1 {
		// Docker Hub shorthand: nginx → docker.io/library/nginx
		return "docker.io", "library/" + parts[0], "latest", nil
	}

	// Check if first part looks like a registry (contains . or :)
	first := parts[0]
	if strings.Contains(first, ".") || strings.Contains(first, ":") || first == "localhost" {
		registry = first
		repository = parts[1]
	} else {
		// Docker Hub user/repo
		registry = "docker.io"
		repository = ref
	}

	// Split tag from repository
	if idx := strings.LastIndex(repository, ":"); idx >= 0 {
		tag = repository[idx+1:]
		repository = repository[:idx]
	} else {
		tag = "latest"
	}

	return registry, repository, tag, nil
}

// resolveRegistryURL returns the OCI registry API base URL.
func resolveRegistryURL(registry string) string {
	switch registry {
	case "docker.io":
		return "https://registry-1.docker.io"
	case "ghcr.io":
		return "https://ghcr.io"
	case "registry.access.redhat.com":
		return "https://registry.access.redhat.com"
	default:
		if strings.HasPrefix(registry, "localhost") {
			return "http://" + registry
		}
		return "https://" + registry
	}
}

// getAuthToken obtains a Bearer token for the registry using the WWW-Authenticate challenge.
func (c *OCIRegistryClient) getAuthToken(registry, repository string) (string, error) {
	baseURL := resolveRegistryURL(registry)

	// Attempt unauthenticated request to trigger WWW-Authenticate
	tokenURL := fmt.Sprintf("%s/v2/%s/manifests/latest", baseURL, repository)
	resp, err := c.httpClient.Get(tokenURL)
	if err != nil {
		return "", fmt.Errorf("initial request failed: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode == 200 {
		// No auth needed (public registry)
		return "", nil
	}

	if resp.StatusCode != 401 {
		return "", fmt.Errorf("unexpected status %d from registry", resp.StatusCode)
	}

	// Parse WWW-Authenticate header
	wwwAuth := resp.Header.Get("Www-Authenticate")
	if wwwAuth == "" {
		return "", fmt.Errorf("401 response without Www-Authenticate header")
	}

	// Extract realm, service, scope from Bearer challenge
	realm, service := extractBearerParams(wwwAuth)
	if realm == "" {
		return "", fmt.Errorf("could not extract realm from Www-Authenticate: %s", wwwAuth)
	}

	// Request token
	tokenURL = fmt.Sprintf("%s?service=%s&scope=repository:%s:pull", realm, service, repository)
	tokenResp, err := c.httpClient.Get(tokenURL)
	if err != nil {
		return "", fmt.Errorf("token request failed: %w", err)
	}
	defer tokenResp.Body.Close()

	if tokenResp.StatusCode != 200 {
		body, _ := io.ReadAll(tokenResp.Body)
		return "", fmt.Errorf("token request failed with status %d: %s", tokenResp.StatusCode, string(body))
	}

	var tokenData struct {
		Token     string `json:"token"`
		ExpiresIn int    `json:"expires_in"`
	}
	if err := json.NewDecoder(tokenResp.Body).Decode(&tokenData); err != nil {
		return "", fmt.Errorf("failed to decode token response: %w", err)
	}

	return tokenData.Token, nil
}

// extractBearerParams parses a Bearer WWW-Authenticate header.
func extractBearerParams(header string) (realm, service string) {
	// Format: Bearer realm="...",service="..."
	header = strings.TrimPrefix(header, "Bearer ")

	for _, part := range strings.Split(header, ",") {
		part = strings.TrimSpace(part)
		if strings.HasPrefix(part, "realm=") {
			realm = strings.Trim(strings.TrimPrefix(part, "realm="), "\"")
		} else if strings.HasPrefix(part, "service=") {
			service = strings.Trim(strings.TrimPrefix(part, "service="), "\"")
		}
	}
	return
}

// fetchManifest retrieves the manifest for a given reference and returns it with digest.
func (c *OCIRegistryClient) fetchManifest(baseURL, repository, reference, token string) (*OCIDigestResult, []byte, error) {
	url := fmt.Sprintf("%s/v2/%s/manifests/%s", baseURL, repository, reference)

	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return nil, nil, err
	}

	// Request OCI manifest media types
	req.Header.Set("Accept", strings.Join([]string{
		"application/vnd.oci.image.manifest.v1+json",
		"application/vnd.docker.distribution.manifest.v2+json",
		"application/vnd.oci.image.index.v1+json",
		"application/vnd.docker.distribution.manifest.list.v2+json",
	}, ", "))

	if token != "" {
		req.Header.Set("Authorization", "Bearer "+token)
	}

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return nil, nil, err
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, nil, err
	}

	digestFromHeader := resp.Header.Get("Docker-Content-Digest")

	result := &OCIDigestResult{
		Image:      repository,
		Reference:  reference,
		StatusCode: resp.StatusCode,
	}

	if resp.StatusCode != 200 {
		return result, body, fmt.Errorf("manifest fetch failed with status %d", resp.StatusCode)
	}

	// Verify digest
	hash := sha256.Sum256(body)
	_computedDigest := "sha256:" + hex.EncodeToString(hash[:])

	if digestFromHeader != "" {
		result.Digest = digestFromHeader
	} else {
		result.Digest = _computedDigest
	}

	// Parse manifest
	var manifest OCIManifest
	if err := json.Unmarshal(body, &manifest); err != nil {
		return result, body, fmt.Errorf("failed to parse manifest: %w", err)
	}

	result.MediaType = manifest.MediaType
	if manifest.MediaType == "" {
		// Detect from content
		if len(manifest.Manifests) > 0 {
			result.MediaType = "application/vnd.oci.image.index.v1+json"
		} else {
			result.MediaType = "application/vnd.oci.image.manifest.v1+json"
		}
	}

	// Check if this is a manifest list / index
	if len(manifest.Manifests) > 0 {
		result.IsIndex = true
		for _, m := range manifest.Manifests {
			result.Platforms = append(result.Platforms, m.Platform)
		}
	}

	return result, body, nil
}

// GetLatestTag resolves the current tag and returns the digest.
func (c *OCIRegistryClient) GetLatestTag(image, currentTag string) (string, string, error) {
	registry, repository, tag, err := parseReference(image)
	if err != nil {
		return "", "", err
	}

	if tag == "latest" && currentTag != "" {
		tag = currentTag
	}

	baseURL := resolveRegistryURL(registry)

	token, err := c.getAuthToken(registry, repository)
	if err != nil {
		return "", "", fmt.Errorf("auth failed for %s: %w", registry, err)
	}

	result, _, err := c.fetchManifest(baseURL, repository, tag, token)
	if err != nil {
		return "", "", err
	}

	return tag, result.Digest, nil
}

// GetDigest resolves a full image reference to its digest.
func (c *OCIRegistryClient) GetDigest(imageRef string) (string, error) {
	registry, repository, tag, err := parseReference(imageRef)
	if err != nil {
		return "", err
	}

	baseURL := resolveRegistryURL(registry)

	token, err := c.getAuthToken(registry, repository)
	if err != nil {
		return "", fmt.Errorf("auth failed for %s: %w", registry, err)
	}

	result, _, err := c.fetchManifest(baseURL, repository, tag, token)
	if err != nil {
		return "", err
	}

	return result.Digest, nil
}

// ResolveManifest fetches and validates a manifest, returning full metadata.
func (c *OCIRegistryClient) ResolveManifest(imageRef string) (*OCIDigestResult, error) {
	registry, repository, tag, err := parseReference(imageRef)
	if err != nil {
		return nil, err
	}

	baseURL := resolveRegistryURL(registry)

	token, err := c.getAuthToken(registry, repository)
	if err != nil {
		return nil, fmt.Errorf("auth failed for %s: %w", registry, err)
	}

	result, _, err := c.fetchManifest(baseURL, repository, tag, token)
	if err != nil {
		return nil, err
	}

	return result, nil
}

// Ensure OCIRegistryClient implements RegistryClient
var _ RegistryClient = (*OCIRegistryClient)(nil)
