#!/bin/sh

# #############################################################################
# Copyright (c) 2022,2024 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
# Copyright (c) 2021,2024 Contributors to the Eclipse Foundation
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

SUBMODELURL=$1
REGISTRYURL=$2
CONTROLPLANEURL=$3
DATAPLANEURL=$4
EDCKEY=$5
ALLOWEDBPNS=$6
MANAGEMENTURL=$7

echo "Submodel: $SUBMODELURL"
echo "Registry: $REGISTRYURL"
echo "Controlplane: $CONTROLPLANEURL"
echo "Dataplane: $DATAPLANEURL"
echo "EDC Key: $EDCKEY"
echo "Allowed BPNs: $ALLOWEDBPNS"

pip install -r /opt/scripts/requirements.txt

# Wait until the EDC management endpoint and the DTR registry are reachable.
# In resource-constrained environments (e.g. CI runners) the pods may take
# several minutes to start: this loop retries every 10 s for up to 10 minutes.
wait_for_tcp() {
  _url="$1"
  _label="$2"
  echo "Waiting for $_label ($_url) ..."
  python3 - "$_url" <<'PYEOF'
import socket, urllib.parse, time, sys
url   = sys.argv[1]
p     = urllib.parse.urlparse(url)
host  = p.hostname
port  = p.port or (443 if p.scheme == "https" else 80)
for i in range(60):
    try:
        s = socket.create_connection((host, port), timeout=5)
        s.close()
        print(f"[{host}:{port}] connection successful")
        sys.exit(0)
    except OSError as e:
        print(f"Attempt {i+1}/60: {host}:{port} not ready – {e}")
        time.sleep(10)
print(f"[{host}:{port}] did not become available after 10 minutes")
sys.exit(1)
PYEOF
  if [ $? -ne 0 ]; then
    echo "ERROR: $_label did not become available. Aborting."
    exit 1
  fi
}

MGMT_URL="${MANAGEMENTURL:-$CONTROLPLANEURL}"
wait_for_tcp "$MGMT_URL"  "EDC management API"
wait_for_tcp "$REGISTRYURL" "Digital Twin Registry"

if [ -z "$MANAGEMENTURL" ]; then
  python /opt/scripts/upload.py -f /opt/scripts/testdata.json -s "$SUBMODELURL" -a "$REGISTRYURL" -edc "$CONTROLPLANEURL" --edcBPN "$ALLOWEDBPNS" -d "$DATAPLANEURL" -k "$EDCKEY" -p test --allowedBPNs "$ALLOWEDBPNS"
else
  echo "Management: $MANAGEMENTURL"
  python /opt/scripts/upload.py -f /opt/scripts/testdata.json -s "$SUBMODELURL" -a "$REGISTRYURL" -edc "$CONTROLPLANEURL" --edcBPN "$ALLOWEDBPNS" -eu "$MANAGEMENTURL" -d "$DATAPLANEURL" -k "$EDCKEY" -p test --allowedBPNs "$ALLOWEDBPNS"
fi
