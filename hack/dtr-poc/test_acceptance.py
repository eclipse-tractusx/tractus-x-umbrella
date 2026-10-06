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
"""Check hook overrides and cleanup diagnostics without creating a cluster."""
import base64
import json
import secrets
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from acceptance import Acceptance
from tenant_profile import ROOT, profile


class CleanupDiagnosticsTests(unittest.TestCase):
    def test_cleanup_failures_preserve_redacted_artifacts_and_original_failure(self):
        for stage in ("delete", "timeout", "verify", "remaining-cluster"):
            with self.subTest(stage=stage), tempfile.TemporaryDirectory() as folder:
                directory = Path(folder)
                test = Acceptance(directory, directory / "temporary")
                test.created = True
                credential = secrets.token_urlsafe(32)
                encoded = base64.b64encode(credential.encode()).decode()
                test.secret_values.append(credential)
                original_failure = "RuntimeError: original acceptance failure"
                test.results.update(result="FAIL", failure=original_failure)
                test.commands.append({"argv": [credential, encoded, test.redact(str(test.kubeconfig))], "exitCode": 1})
                test.events.append({"diagnostic": credential})
                failure = RuntimeError("cleanup failed: " + credential)
                outcomes = {
                    "delete": [failure],
                    "timeout": [subprocess.TimeoutExpired(["kind", "delete", "cluster"], 1)],
                    "verify": ["", failure],
                    "remaining-cluster": ["", test.cluster + "\n"],
                }
                with patch.object(test, "run", side_effect=outcomes[stage]):
                    with self.assertRaises((RuntimeError, subprocess.TimeoutExpired, AssertionError)) as raised:
                        test.finish()
                if stage != "remaining-cluster":
                    self.assertIs(raised.exception, outcomes[stage][-1])
                for name in ("commands.json", "results.json", "api-events.json"):
                    self.assertTrue((directory / name).is_file(), name)
                    text = (directory / name).read_text(encoding="utf-8")
                    self.assertNotIn(credential, text)
                    self.assertNotIn(encoded, text)
                    self.assertNotIn(str(test.kubeconfig), text)
                    json.loads(text)
                result = json.loads((directory / "results.json").read_text())
                self.assertEqual(result["result"], "FAIL")
                self.assertEqual(result["failure"], original_failure)
                self.assertEqual(result["checks"]["temporaryClusterRemoved"], "FAIL")
                self.assertIn("cleanupFailure", result)
                commands = json.loads((directory / "commands.json").read_text())
                self.assertEqual(commands[0]["argv"], ["<redacted>", "<redacted>", "<temporary-kubeconfig>"])

    def test_cleanup_failure_turns_success_into_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            directory = Path(folder)
            test = Acceptance(directory, directory / "temporary")
            test.created = True
            test.results["result"] = "PASS"
            with patch.object(test, "run", side_effect=RuntimeError("cleanup failed")):
                with self.assertRaises(RuntimeError):
                    test.finish()
            self.assertEqual(json.loads((directory / "results.json").read_text())["result"], "FAIL")
            self.assertEqual(json.loads((directory / "api-events.json").read_text()), [])

    def test_successful_cleanup_keeps_success_and_saves_empty_events(self):
        with tempfile.TemporaryDirectory() as folder:
            directory = Path(folder)
            test = Acceptance(directory, directory / "temporary")
            test.created = True
            test.results["result"] = "PASS"
            with patch.object(test, "run", side_effect=["", ""]):
                test.finish()
            result = json.loads((directory / "results.json").read_text())
            self.assertEqual(result["result"], "PASS")
            self.assertEqual(result["checks"]["temporaryClusterRemoved"], "PASS")
            self.assertNotIn("cleanupFailure", result)
            self.assertEqual(json.loads((directory / "api-events.json").read_text()), [])

    def test_failure_before_cluster_creation_still_saves_diagnostics(self):
        with tempfile.TemporaryDirectory() as folder:
            directory = Path(folder)
            test = Acceptance(directory, directory / "temporary")
            test.results["result"] = "FAIL"
            with patch.object(test, "run", side_effect=AssertionError("must not call Kind")):
                test.finish()
            self.assertEqual(json.loads((directory / "results.json").read_text())["result"], "FAIL")
            self.assertEqual(json.loads((directory / "api-events.json").read_text()), [])


class StartupPrerequisitesTests(unittest.TestCase):
    def render(self, override):
        values, _ = profile("umbrella-basyx-poc", "basyx-dtr-poc", "poc-a")
        values["digital-twin-basyx-bundle"]["basyx"].update(override)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "values.yaml"
            path.write_text(yaml.safe_dump(values), encoding="utf-8")
            return subprocess.run(["helm", "template", "basyx-dtr-poc", str(ROOT / "charts/tx-data-provider"),
                                   "-n", "umbrella-basyx-poc", "-f", str(path)],
                                  text=True, encoding="utf-8", capture_output=True, timeout=60)

    def test_default_and_explicit_weights_preserve_rendered_hook_order(self):
        for override in ({}, {"configurationService": {"hook": {"weight": "-10"}}}):
            with self.subTest(override=override):
                result = self.render(override)
                self.assertEqual(result.returncode, 0, result.stderr)
                objects = [o for o in yaml.safe_load_all(result.stdout) if o]
                job = next(o for o in objects if o["kind"] == "Job")
                account = next(o for o in objects if o["kind"] == "ServiceAccount"
                               and o["metadata"]["name"] == job["spec"]["template"]["spec"]["serviceAccountName"])
                self.assertEqual(job["metadata"]["annotations"]["helm.sh/hook-weight"], "-10")
                self.assertEqual(account["metadata"]["annotations"]["helm.sh/hook-weight"], "-20")
                self.assertEqual(account["metadata"]["annotations"]["helm.sh/hook-delete-policy"], "before-hook-creation")

    def test_job_weight_override_is_rejected(self):
        result = self.render({"configurationService": {"hook": {"weight": "-30"}}})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("weight -10", result.stderr)

    def test_early_service_account_deletion_is_rejected(self):
        for policy in ("hook-succeeded", "before-hook-creation,hook-succeeded"):
            with self.subTest(policy=policy):
                result = self.render({"serviceAccount": {"annotations": {"helm.sh/hook-delete-policy": policy}}})
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("before-hook-creation", result.stderr)

    def test_job_annotations_cannot_override_validated_helm_hooks(self):
        for key, value in (("helm.sh/hook", "post-install"), ("helm.sh/hook-weight", "-30"),
                           ("helm.sh/hook-delete-policy", "hook-succeeded")):
            with self.subTest(key=key):
                result = self.render({"configurationService": {"hook": {"annotations": {key: value}}}})
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("must not override Helm hook annotations", result.stderr)


if __name__ == "__main__":
    unittest.main()
