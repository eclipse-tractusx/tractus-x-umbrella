{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "semantic-hub.chart" -}}
    {{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "semantic-hub.labels" -}}
    service: {{ .Chart.Name }}
{{- end -}}

{{/*
Selector labels
*/}}
{{- define "semantic-hub.selectorLabels" -}}
    service: {{ .Chart.Name }}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "semantic-hub.serviceAccountName" -}}
    {{- if .Values.serviceAccount.create -}}
        {{- default .Chart.Name .Values.serviceAccount.name -}}
    {{- else -}}
        {{- default "default" .Values.serviceAccount.name -}}
    {{- end -}}
{{- end -}}