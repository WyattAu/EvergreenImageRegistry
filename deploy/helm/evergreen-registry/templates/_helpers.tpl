{{/*
Expand the name of the chart.
*/}}
{{- define "evergreen-registry.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "evergreen-registry.fullname" -}}
{{- if contains .Chart.Name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Chart.Name .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "evergreen-registry.labels" -}}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
app.kubernetes.io/name: {{ include "evergreen-registry.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- with .Values.security -}}
evergreen.security.cap-drop: {{ .capDropAll | default false }}
evergreen.security.no-new-privileges: {{ .noNewPrivileges | default false }}
evergreen.security.read-only-rootfs: {{ .readOnlyRootFs | default false }}
{{- end -}}
{{- end -}}

{{/*
Selector labels
*/}}
{{- define "evergreen-registry.selectorLabels" -}}
app.kubernetes.io/name: {{ include "evergreen-registry.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}
