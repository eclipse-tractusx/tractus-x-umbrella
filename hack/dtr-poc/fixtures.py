# #############################################################################
# Copyright (c) 2026 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0
# #############################################################################
"""Persistent database resources for the disposable Kind acceptance cluster only."""
PG_IMAGE = "postgres:18.4@sha256:3a82e1f56c8f0f5616a11103ac3d47e632c3938698946a7ad26da0df1334744a"
DATABASE = "basyx_poc"


def database_resources(tenant):
    ns, name = tenant["namespace"], tenant["postgres"]
    labels = {"app": name}
    metadata = lambda resource: {"name": resource, "namespace": ns}
    resources = [{"apiVersion": "v1", "kind": "Namespace", "metadata": {"name": ns}},
        {"apiVersion": "v1", "kind": "PersistentVolume", "metadata": {"name": f"{ns}-{name}"},
         "spec": {"capacity": {"storage": "5Gi"}, "accessModes": ["ReadWriteOnce"],
                  "storageClassName": "", "persistentVolumeReclaimPolicy": "Retain",
                  "claimRef": {"namespace": ns, "name": name},
                  "hostPath": {"path": f"/var/local/dtr-poc/{ns}/{name}", "type": "Directory"}}},
        {"apiVersion": "v1", "kind": "PersistentVolumeClaim", "metadata": metadata(name),
         "spec": {"storageClassName": "", "volumeName": f"{ns}-{name}",
                  "accessModes": ["ReadWriteOnce"], "resources": {"requests": {"storage": "5Gi"}}}},
        {"apiVersion": "v1", "kind": "Service", "metadata": metadata(name),
         "spec": {"selector": labels, "ports": [{"name": "postgres", "port": 5432}]}},
        {"apiVersion": "apps/v1", "kind": "StatefulSet", "metadata": metadata(name),
         "spec": {"serviceName": name, "replicas": 1, "selector": {"matchLabels": labels},
                  "template": {"metadata": {"labels": labels}, "spec": {
                      "automountServiceAccountToken": False,
                      "securityContext": {"runAsUser": 999, "runAsGroup": 999, "fsGroup": 999,
                                          "runAsNonRoot": True, "seccompProfile": {"type": "RuntimeDefault"}},
                      "containers": [{"name": "postgres", "image": PG_IMAGE,
                          "securityContext": {"allowPrivilegeEscalation": False, "capabilities": {"drop": ["ALL"]}},
                          "env": [{"name": "PGDATA", "value": "/var/lib/postgresql/data/pgdata"},
                                  {"name": "POSTGRES_PASSWORD", "valueFrom": {"secretKeyRef": {
                                      "name": f"{name}-admin", "key": "password"}}}],
                          "ports": [{"containerPort": 5432}],
                          "volumeMounts": [{"name": "data", "mountPath": "/var/lib/postgresql/data"}],
                          "readinessProbe": {"exec": {"command": ["pg_isready", "-U", "postgres"]},
                                             "periodSeconds": 3},
                          "resources": {"requests": {"cpu": "50m", "memory": "128Mi"},
                                        "limits": {"cpu": "500m", "memory": "512Mi"}}}],
                      "volumes": [{"name": "data", "persistentVolumeClaim": {"claimName": name}}]}}}},
        {"apiVersion": "batch/v1", "kind": "Job", "metadata": metadata(f"{name}-bootstrap"),
         "spec": {"backoffLimit": 0, "activeDeadlineSeconds": 120, "template": {
             "spec": {"automountServiceAccountToken": False, "restartPolicy": "Never",
                 "containers": [{"name": "bootstrap", "image": PG_IMAGE,
                     "env": [{"name": "PGHOST", "value": name},
                             {"name": "PGPASSWORD", "valueFrom": {"secretKeyRef": {
                                 "name": f"{name}-admin", "key": "password"}}},
                             {"name": "APP_PASSWORD", "valueFrom": {"secretKeyRef": {
                                 "name": tenant["databaseSecret"], "key": "password"}}}],
                     "command": ["/bin/sh", "-ec", r"""psql -U postgres -d postgres -v ON_ERROR_STOP=1 <<'SQL'
\getenv app_password APP_PASSWORD
CREATE ROLE basyx_poc LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE PASSWORD :'app_password';
CREATE DATABASE basyx_poc OWNER basyx_poc;
REVOKE CONNECT ON DATABASE basyx_poc FROM PUBLIC;
ALTER ROLE basyx_poc IN DATABASE basyx_poc SET search_path = basyx_poc;
\connect basyx_poc
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
CREATE SCHEMA basyx_poc AUTHORIZATION basyx_poc;
SQL
"""]}]}}}}]
    return resources
