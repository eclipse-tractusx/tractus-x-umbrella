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

if [ -z "$MANAGEMENTURL" ]; then
  python /opt/scripts/upload.py -f /opt/scripts/testdata.json -s "$SUBMODELURL" -a "$REGISTRYURL" -edc "$CONTROLPLANEURL" --edcBPN "$ALLOWEDBPNS" -d "$DATAPLANEURL" -k "$EDCKEY" -p test --allowedBPNs "$ALLOWEDBPNS"
else
  echo "Management: $MANAGEMENTURL"
  python /opt/scripts/upload.py -f /opt/scripts/testdata.json -s "$SUBMODELURL" -a "$REGISTRYURL" -edc "$CONTROLPLANEURL" --edcBPN "$ALLOWEDBPNS" -eu "$MANAGEMENTURL" -d "$DATAPLANEURL" -k "$EDCKEY" -p test --allowedBPNs "$ALLOWEDBPNS"
fi
