{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "irs-provider-backend.chart" -}}
    {{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "irs-provider-backend.labels" -}}
    service: {{ .Chart.Name }}
{{- end -}}

{{/*
Selector labels
*/}}
{{- define "irs-provider-backend.selectorLabels" -}}
    service: {{ .Chart.Name }}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "irs-provider-backend.serviceAccountName" -}}
    {{- if .Values.serviceAccount.create -}}
        {{- default .Chart.Name .Values.serviceAccount.name -}}
    {{- else -}}
        {{- default "default" .Values.serviceAccount.name -}}
    {{- end -}}
{{- end -}}