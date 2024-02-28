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
{{- define "submodelservers.host" -}}
    {{- if .Values.submodelservers.ingress.enabled }}
        {{- with (first .Values.submodelservers.ingress.hosts) }}
            {{- printf "https://%s" .host }}
        {{- end }}
    {{- else }}
        {{- print "http://test" }}
    {{- end }}
{{- end }}

{{/*
Registry URL helpers
*/}}
{{- define "registry.host" -}}
    {{- printf "https://%s" (index .Values "digital-twin-registry" "registry" "host") }}
{{- end }}
{{- define "registry.path" -}}
    {{- index .Values "digital-twin-registry" "registry" "ingress" "urlPrefix" }}
{{- end }}
{{- define "registry.url" -}}
    {{- printf "%s%s%s" (include "registry.host" .) (include "registry.path" .) "/api/v3.0" }}
{{- end }}

{{/*
EDC URL helpers
*/}}
{{- define "edc.controlplane.host" -}}
    {{- with (first (index .Values "tractusx-connector" "controlplane" "ingresses")) }}
        {{- printf "https://%s" .hostname }}
    {{- end }}
{{- end }}
{{- define "edc.dataplane.host" -}}
    {{- with (first (index .Values "tractusx-connector" "dataplane" "ingresses")) }}
        {{- printf "https://%s" .hostname }}
    {{- end }}
{{- end }}
{{- define "edc.key" -}}
    {{- index .Values "tractusx-connector" "controlplane" "endpoints" "management" "authKey" }}
{{- end }}
{{- define "edc.bpn" -}}
    {{- index .Values "tractusx-connector" "participant" "id" }}
{{- end }}

