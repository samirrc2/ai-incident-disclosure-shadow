#!/usr/bin/env bash
# Top-level entry point (local + Code Ocean). Delegates to code/scripts/reproduce.sh.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
exec bash "$ROOT/code/scripts/reproduce.sh" "$@"
