{{/*
*******************************************************************************
 * Copyright (c) 2022,2024 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
 * Copyright (c) 2021,2024 Contributors to the Eclipse Foundation
 *
 * See the NOTICE file(s) distributed with this work for additional
 * information regarding copyright ownership.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Apache License, Version 2.0 which is available at
 * https://www.apache.org/licenses/LICENSE-2.0.
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 *
 * SPDX-License-Identifier: Apache-2.0
 *******************************************************************************
 */}}
{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "dataprovider.fullname" -}}
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
Submodel URL helpers
*/}}
{{- define "simple-data-backend.host" -}}
    {{- if .Values.backendUrl }}
        {{- tpl .Values.backendUrl . }}
    {{- else if (index .Values "simple-data-backend" "ingress" "enabled") }}
        {{- with (first (index .Values "simple-data-backend" "ingress" "hosts")) }}
            {{- printf "https://%s" .host }}
        {{- end }}
    {{- else }}
        {{- printf "http://%s%s:8080" .Release.Name "-simple-data-backend" }}
    {{- end }}
{{- end }}

{{/*
Registry URL helpers
*/}}
{{- define "registry.host" -}}
    {{- if index .Values "digital-twin-registry" "registry" "ingress" "enabled" }}
        {{- printf "https://%s" (index .Values "digital-twin-registry" "registry" "host") }}
    {{- else }}
        {{- printf "http://%s-%s:8080" .Release.Name "digital-twin-registry" }}
    {{- end }}
{{- end }}
{{- define "registry.path" -}}
    {{- if index .Values "digital-twin-registry" "registry" "ingress" "enabled" }}
        {{- index .Values "digital-twin-registry" "registry" "ingress" "urlPrefix" }}
    {{- else }}
    {{- print "" }}
    {{- end }}
{{- end }}
{{- define "registry.url" -}}
    {{- if .Values.registryUrl }}
        {{- tpl .Values.registryUrl . }}
    {{ else }}
        {{- printf "%s%s%s" (include "registry.host" .) (include "registry.path" .) "/api/v3" }}
    {{- end }}
{{- end }}

{{/*
EDC URL helpers
*/}}

{{- define "edc.controlplane.host" -}}
    {{- if .Values.controlplanePublicUrl }}
        {{- tpl .Values.controlplanePublicUrl . }}
    {{ else }}
        {{- with (first (index .Values "tractusx-connector" "controlplane" "ingresses")) }}
            {{- if .enabled }}
                {{- printf "https://%s" .hostname }}
            {{- else }}
                {{- printf "http://%s-%s:8084" $.Release.Name "tractusx-connector-controlplane" }}
            {{- end }}
        {{- end }}
    {{ end  }}
{{- end }}

{{- define "edc.controlplane.management.host" -}}
    {{- if .Values.controlplaneManagementUrl }}
        {{- tpl .Values.controlplaneManagementUrl . }}
    {{ else }}
        {{- with (first (index .Values "tractusx-connector" "controlplane" "ingresses")) }}
            {{- if .enabled }}
                {{- printf "https://%s" .hostname }}
            {{- else }}
                {{- printf "http://%s-%s:8081" $.Release.Name "tractusx-connector-controlplane" }}
            {{- end }}
        {{- end }}
    {{ end  }}
{{- end }}

{{- define "edc.dataplane.host" -}}
    {{- if .Values.dataplaneUrl }}
        {{- tpl .Values.dataplaneUrl . }}
    {{ else }}
        {{- with (first (index .Values "tractusx-connector" "dataplane" "ingresses")) }}
            {{- if .enabled }}
                {{- printf "https://%s" .hostname }}
            {{- else }}
                {{- printf "http://%s-%s:8081" $.Release.Name "tractusx-connector-dataplane" }}
            {{- end }}
        {{- end }}
    {{ end  }}
{{- end }}

{{- define "edc.key" -}}
    {{- index .Values  "dataspace-connector-bundle" "tractusx-connector" "controlplane" "endpoints" "management" "authKey" }}
{{- end }}

{{- define "edc.bpn" -}}
    {{- index .Values  "dataspace-connector-bundle" "tractusx-connector" "participant" "id" }}
{{- end }}

