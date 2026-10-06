#!/usr/bin/env python3
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
"""Filter the unused TLS Issuer emitted by official BaSyx chart 3.15.0.

Standard library only, so it runs wherever python3 is available. Every other
document is passed through unchanged.
"""
import re
import sys

KIND = re.compile(r"^kind:\s*['\"]?Issuer['\"]?\s*$", re.MULTILINE)
NAME = re.compile(r"^metadata:\s*\n(?:[ \t]+.*\n|\s*\n)*?[ \t]+name:\s*['\"]?internal-issuer['\"]?\s*$", re.MULTILINE)


def keep(document):
    return not (KIND.search(document) and NAME.search(document))


documents = re.split(r"^---[ \t]*$\n?", sys.stdin.read(), flags=re.MULTILINE)
sys.stdout.write("".join("---\n" + d for d in documents if d.strip() and keep(d)))
