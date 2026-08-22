{{/*
Evergreen Image Registry — Helm Chart Helpers
=============================================
*/}}

{{/*
Expand the name of the chart.
*/}}
{{- define "evergreen.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "evergreen.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "evergreen.labels" -}}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
app.kubernetes.io/name: {{ include "evergreen.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Values.image.tag | default "latest" | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/part-of: evergreen-image-registry
evergreenimageregistry.io/tier: {{ .Values.tier | default "standard" | quote }}
evergreenimageregistry.io/hardened: "true"
{{- end }}

{{/*
Selector labels
*/}}
{{- define "evergreen.selectorLabels" -}}
app.kubernetes.io/name: {{ include "evergreen.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Image reference
*/}}
{{- define "evergreen.image" -}}
{{- $registry := .Values.image.registry | default "ghcr.io/wyattau/evergreenimageregistry" -}}
{{- $name := .Values.image.name | default .Chart.Name -}}
{{- $tag := .Values.image.tag | default "latest" -}}
{{- printf "%s/%s:%s" $registry $name $tag -}}
{{- end }}

{{/*
Security context — hardened defaults for EIR images
Non-root (65532), read-only root, drop all capabilities
*/}}
{{- define "evergreen.securityContext" -}}
runAsNonRoot: true
runAsUser: 65532
runAsGroup: 65532
fsGroup: 65532
seccompProfile:
  type: RuntimeDefault
allowPrivilegeEscalation: false
readOnlyRootFilesystem: {{ .Values.security.readOnlyRootFs | default true }}
capabilities:
  drop:
    - ALL
{{- end }}

{{/*
Container security context
*/}}
{{- define "evergreen.containerSecurityContext" -}}
securityContext:
  runAsNonRoot: true
  runAsUser: 65532
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: {{ .Values.security.readOnlyRootFs | default true }}
  capabilities:
    drop:
      - ALL
  seccompProfile:
    type: RuntimeDefault
{{- end }}

{{/*
Resource limits — sensible defaults per tier
*/}}
{{- define "evergreen.resources" -}}
{{- if eq (.Values.tier | default "standard") "critical" }}
requests:
  cpu: 250m
  memory: 256Mi
limits:
  cpu: 2000m
  memory: 2Gi
{{- else }}
requests:
  cpu: 100m
  memory: 128Mi
limits:
  cpu: 1000m
  memory: 1Gi
{{- end }}
{{- end }}

{{/*
Liveness probe — TCP-based for distroless images
*/}}
{{- define "evergreen.livenessProbe" -}}
{{- if .Values.health.enabled | default true }}
livenessProbe:
  tcpSocket:
    port: {{ .Values.service.port | default 8080 }}
  initialDelaySeconds: {{ .Values.health.livenessInitialDelay | default 15 }}
  periodSeconds: {{ .Values.health.livenessPeriod | default 20 }}
  timeoutSeconds: 5
  failureThreshold: 3
{{- end }}
{{- end }}

{{/*
Readiness probe
*/}}
{{- define "evergreen.readinessProbe" -}}
{{- if .Values.health.enabled | default true }}
readinessProbe:
  tcpSocket:
    port: {{ .Values.service.port | default 8080 }}
  initialDelaySeconds: {{ .Values.health.readinessInitialDelay | default 5 }}
  periodSeconds: 10
  timeoutSeconds: 3
  failureThreshold: 3
{{- end }}
{{- end }}

{{/*
Network policy — default deny all, allow ingress on service port
*/}}
{{- define "evergreen.networkPolicy" -}}
{{- if .Values.networkPolicy.enabled | default false }}
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: {{ include "evergreen.fullname" . }}
  labels:
    {{- include "evergreen.labels" . | nindent 4 }}
spec:
  podSelector:
    matchLabels:
      {{- include "evergreen.selectorLabels" . | nindent 6 }}
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - ports:
        - port: {{ .Values.service.port | default 8080 }}
  egress:
    - ports:
        - port: 53
          protocol: UDP
        - port: 53
          protocol: TCP
{{- end }}
{{- end }}
