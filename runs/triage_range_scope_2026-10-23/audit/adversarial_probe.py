#!/usr/bin/env python3
"""Adversarial probes against v031/scripts/triage_range_scope.py.

Imports the tool under audit (read-only) and feeds it synthetic records.
Run: python3 -I adversarial_probe.py
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location(
    "triage_range_scope", ROOT / "v031/scripts/triage_range_scope.py"
)
tool = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(tool)

CURL_NAMES = {tool.normalized_name(n) for n in ("curl", "libcurl")}


def show(label, value, expected):
    mark = "OK " if value == expected else "DEFECT"
    print(f"[{mark}] {label}\n         expected={expected!r} actual={value!r}")


def osv_record(entries, rid="GHSA-test-0000-0000"):
    return {"id": rid, "aliases": [], "affected": entries}


def entry(name, eco, ranges, versions=None):
    a = {"package": {"name": name, "ecosystem": eco}, "ranges": ranges}
    if versions is not None:
        a["versions"] = versions
    return a


def nvd_record(cpes, rid="CVE-0000-0000", desc=""):
    node = {"cpeMatch": cpes}
    return {
        "id": rid,
        "descriptions": [{"value": desc}],
        "configurations": [{"nodes": [node]}] if cpes is not None else [],
    }


def cpe(criteria, **kw):
    c = {"criteria": criteria, "vulnerable": kw.pop("vulnerable", True)}
    c.update(kw)
    return c


print("== tag parsing ==")
for tag, want in [
    ("curl-8_3_0", (8, 3)),
    ("netty-4.1.137.Final", (4, 1, 137)),
    ("jenkins-2.441", (2, 441)),
    ("v/0.23.4", (0, 23, 4)),
    ("R_2_6_2", (2, 6, 2)),
    ("4.2.13", (4, 2, 13)),
    ("v1.7.16", (1, 7, 16)),
]:
    show(f"parse_version({tag!r})", tool.parse_version(tag), want)

print("\n== OSV range semantics ==")
show(
    "open {introduced:0} alone (all versions affected) -> range_contains",
    tool.range_contains([{"introduced": "0"}], (5, 0)),
    None,  # unsupported/open-ended, NOT False
)
same_entry = [
    entry("curl", "GitHub", [{"type": "ECOSYSTEM", "events": [{"introduced": "0"}]}]),
    entry("curl", "GitHub", [{"type": "ECOSYSTEM", "events": [{"introduced": "1.0"}, {"fixed": "2.0"}]}]),
]
st, det, _ = tool.evaluate_osv(osv_record([same_entry[0]]), (5, 0), "curl")
show("evaluate_osv: open {introduced:0} only", st, "indeterminate")
st, det, _ = tool.evaluate_osv(
    osv_record([entry("curl", "GitHub", [
        {"type": "ECOSYSTEM", "events": [{"introduced": "0"}]},
        {"type": "ECOSYSTEM", "events": [{"introduced": "1.0"}, {"fixed": "2.0"}]},
    ])]),
    (5, 0), "curl",
)
show("evaluate_osv: open {introduced:0} + bounded 1.0-2.0 at 5.0", st, "indeterminate")
st, det, _ = tool.evaluate_osv(
    osv_record([entry("curl", "GitHub", [{"type": "ECOSYSTEM", "events": [{"introduced": "1.0"}, {"last_affected": "2.0"}]}])]),
    (2, 0), "curl",
)
show("last_affected is inclusive at 2.0", st, "possible_affected_range")
st, det, _ = tool.evaluate_osv(
    osv_record([entry("curl", "GitHub", [{"type": "ECOSYSTEM", "events": [{"introduced": "1.0"}, {"limit": "3.0"}]}])]),
    (2, 0), "curl",
)
show("limit event treated as exclusive upper", st, "possible_affected_range")
st, det, _ = tool.evaluate_osv(
    osv_record([entry("curl", "Debian:12", [{"type": "ECOSYSTEM", "events": [{"introduced": "0"}, {"fixed": "1.0"}]}])]),
    (5, 0), "curl",
)
show("Debian affected entry with an upstream query", st, "unsupported_ecosystem")
st, det, _ = tool.evaluate_osv(
    osv_record([entry("Django", "PyPI", [{"type": "ECOSYSTEM", "events": [{"introduced": "1.0"}, {"fixed": "2.0"}]}])]),
    (5, 0), "django",
)
show("package-name filter is case-insensitive", st, "not_affected_range")
st, det, _ = tool.evaluate_osv(
    osv_record([entry("django", "PyPI", [{"type": "GIT", "events": [{"introduced": "a" * 40}, {"fixed": "b" * 40}]}])]),
    (5, 0), "django",
)
show("GIT commit range", st, "indeterminate")

print("\n== NVD CPE semantics ==")
rec = nvd_record([cpe("cpe:2.3:a:curl:curl:*:*:*:*:*:*:*:*", versionEndExcluding="7.84.0")], desc="curl before 7.84.0")
show("versionEndExcluding 7.84.0 at 8.3.0", tool.evaluate_nvd(rec, (8, 3), CURL_NAMES)[0], "not_affected_range")
rec = nvd_record([cpe("cpe:2.3:a:curl:curl:*:*:*:*:*:*:*:*", versionStartIncluding="1.0")], desc="curl from 1.0")
show("start-only CPE (open-ended) at 8.3.0", tool.evaluate_nvd(rec, (8, 3), CURL_NAMES)[0], "possible_affected_range")
rec = nvd_record([cpe("cpe:2.3:a:curl:curl:*:*:*:*:*:*:*:*", versionEndExcluding="0.0.0")],
                 desc="parse_string in cJSON.c before 2016-10-02")
show("nonsense versionEndExcluding 0.0.0 at 1.4.6", tool.evaluate_nvd(rec, (1, 4, 6), CURL_NAMES)[0], "indeterminate")
rec = nvd_record([cpe("cpe:2.3:a:apple:mac_os_x:*:*:*:*:*:*:*:*", versionEndExcluding="10.9.2")],
                 desc="curl and libcurl 7.27.0 through 7.35.0, as used in Apple OS X")
show("CVE-2014-1263-like: mac_os_x CPE for curl at 8.3.0", tool.evaluate_nvd(rec, (8, 3), CURL_NAMES)[0], "no_matching_package")
rec = nvd_record([cpe("cpe:2.3:a:python:python:*:*:*:*:*:*:*:*", versionEndExcluding="3.10.0")],
                 desc="When an Expat parser with a registered ElementDeclHandler ...")
show("CVE-2026-4224-like: python CPE, Expat description", tool.evaluate_nvd(rec, (2, 6, 2), CURL_NAMES)[0], "no_matching_package")
rec = nvd_record([cpe("cpe:2.3:a:curl:curl:7.30.0:*:*:*:*:*:*")], desc="curl 7.30.0")
show("exact CPE 7.30.0 at 7.30.0", tool.evaluate_nvd(rec, (7, 30, 0), CURL_NAMES)[0], "possible_affected_range")
show("exact CPE 7.30.0 at 8.3.0", tool.evaluate_nvd(rec, (8, 3), CURL_NAMES)[0], "not_affected_range")
rec = nvd_record([cpe("cpe:/a:curl:curl:7.30.0")], desc="CPE 2.2 style")
show("CPE 2.2 URI at 8.3.0", tool.evaluate_nvd(rec, (8, 3), CURL_NAMES)[0], "indeterminate")
rec = nvd_record([cpe("cpe:2.3:a:curl:curl:*:*:*:*:*:*:*:*", vulnerable=False)], desc="")
show("all matching CPEs vulnerable=false", tool.evaluate_nvd(rec, (8, 3), CURL_NAMES)[0], "indeterminate")
rec = nvd_record([], desc="keyword hit, no configurations")
show("record with no configurations", tool.evaluate_nvd(rec, (8, 3), CURL_NAMES)[0], "no_configuration")
rec = nvd_record([cpe("cpe:2.3:a:apple:curl:*:*:*:*:*:*:*:*", versionEndExcluding="7.35.0")], desc="")
show("vendor ignored: apple:curl product matches curl", tool.evaluate_nvd(rec, (8, 3), CURL_NAMES)[0], "not_affected_range")

print("\n== aggregation (two records: one fixed before, one after) ==")
statuses = []
for r in [
    nvd_record([cpe("cpe:2.3:a:curl:curl:*:*:*:*:*:*:*:*", versionEndExcluding="7.0.0")], rid="CVE-1"),
    nvd_record([cpe("cpe:2.3:a:curl:curl:*:*:*:*:*:*:*:*",
                   versionStartIncluding="10.0", versionEndExcluding="11.0")], rid="CVE-2"),
]:
    statuses.append(tool.evaluate_nvd(r, (8, 3), CURL_NAMES)[0])
proposal = (
    "possible_affected_range" if "possible_affected_range" in statuses
    else "not_affected_range" if all(s == "not_affected_range" for s in statuses)
    else "indeterminate"
)
show("one record fixed<8.3, one fixed>8.3", (statuses, proposal),
     (["not_affected_range", "indeterminate"], "indeterminate"))
print("\nDone.")
