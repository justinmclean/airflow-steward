#!/usr/bin/env bash
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# Run a single static-check / test command across every workspace
# member declared in the root `pyproject.toml`'s
# `[tool.uv.workspace] members` list. Used by the four
# workspace-* hooks in `.pre-commit-config.yaml` so adding a new
# tool doesn't require editing the pre-commit config at all —
# just append the new member's path to `[tool.uv.workspace]`.
#
# Usage:
#   tools/dev/run-workspace-check.sh <check-key> <check-cmd> [args...]
#
# `check-key` selects which auto-discovery rule applies and which
# per-member opt-out entry to consult. Recognised keys:
#
#   ruff          → runs only on members with `[tool.ruff]`
#   ruff-format   → runs only on members with `[tool.ruff]`
#   mypy          → runs only on members with `[tool.mypy]`
#   pytest        → runs only on members with `[tool.pytest.ini_options]`
#
# `check-cmd` is the actual command-line passed to `uv run`. It
# may be a multi-token string (e.g. "ruff check") quoted as a
# single argv item.
#
# Per-member opt-out: a workspace member can skip one or more
# checks by adding a `[tool.steward.checks]` block:
#
#   [tool.steward.checks]
#   skip = ["mypy", "pytest"]
#
# Examples:
#   tools/dev/run-workspace-check.sh ruff        "ruff check"
#   tools/dev/run-workspace-check.sh ruff-format "ruff format --check"
#   tools/dev/run-workspace-check.sh mypy        mypy
#   tools/dev/run-workspace-check.sh pytest      "pytest --color=yes"
#
# Exit code: 0 iff the check succeeded on every applicable
# member; 1 otherwise. The script does NOT short-circuit on the
# first failure — every member runs so the operator sees all
# failures in one pass.

set -uo pipefail

if [ "$#" -lt 2 ]; then
  echo "usage: $0 <check-key> <check-cmd> [args...]" >&2
  exit 64
fi

CHECK_KEY="$1"
CHECK_CMD="$2"
shift 2

# Discover workspace members + per-check applicability. The Python
# helper walks the root `[tool.uv.workspace] members` list, opens
# each member's pyproject.toml, and emits one line per applicable
# member: "<check>\t<path>" — with the `<check>` filter already
# applied based on (a) the presence of the relevant `[tool.*]`
# section and (b) the member's `[tool.steward.checks] skip` list.
applicable=$(python3 - "$CHECK_KEY" <<'PY'
import sys
import tomllib

check = sys.argv[1]

# Which `[tool.*]` section signals that this check is configured
# for a given member. ruff-check and ruff-format both look at
# `[tool.ruff]` because the same config drives both.
SECTION_FOR_CHECK = {
    "ruff": "ruff",
    "ruff-format": "ruff",
    "mypy": "mypy",
    "pytest": "pytest",
}

section_key = SECTION_FOR_CHECK.get(check)
if section_key is None:
    sys.stderr.write(f"error: unknown check-key {check!r}\n")
    sys.exit(2)

with open("pyproject.toml", "rb") as f:
    root = tomllib.load(f)

try:
    members = root["tool"]["uv"]["workspace"]["members"]
except KeyError:
    sys.stderr.write("error: [tool.uv.workspace] members not in root pyproject.toml\n")
    sys.exit(2)

for member in members:
    try:
        with open(f"{member}/pyproject.toml", "rb") as f:
            data = tomllib.load(f)
    except FileNotFoundError:
        sys.stderr.write(f"warning: workspace member missing pyproject.toml: {member}\n")
        continue

    tool = data.get("tool", {})

    # Opt-out check.
    skip = tool.get("steward", {}).get("checks", {}).get("skip", [])
    if check in skip:
        continue

    # Auto-discovery check — the [tool.<X>] block must exist.
    # `pytest` looks at the nested `[tool.pytest.ini_options]` table.
    if section_key == "pytest":
        if "ini_options" not in tool.get("pytest", {}):
            continue
    else:
        if section_key not in tool:
            continue

    print(member)
PY
)
status=$?
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

if [ -z "$applicable" ]; then
  echo "→ ${CHECK_KEY}: no applicable workspace members (nothing to run)"
  exit 0
fi

count=$(echo "$applicable" | wc -l | tr -d ' ')
echo "→ workspace-check: ${CHECK_KEY} (${CHECK_CMD} $*) across ${count} members"

failed=()
for member in $applicable; do
  name=$(basename "$member")
  # `uv run --directory` so each member runs with its own `cwd` —
  # ruff / mypy / pytest configs resolve paths relative to the
  # member root.
  # shellcheck disable=SC2086 # CHECK_CMD may legitimately be multi-token
  if ! uv run --directory "$member" $CHECK_CMD "$@"; then
    failed+=("$name")
  fi
done

if [ "${#failed[@]}" -gt 0 ]; then
  echo "✗ ${CHECK_KEY} failed for: ${failed[*]}" >&2
  exit 1
fi
echo "✓ ${CHECK_KEY} passed for all ${count} applicable members"
