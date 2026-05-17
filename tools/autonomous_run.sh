#!/bin/bash
echo "[DEPRECATED] tools/autonomous_run.sh is moving to scripts/. Run instead:" >&2
echo "  cd \"$(cd \"$(dirname \"$0\")/..\" && pwd)\" && bash scripts/autonomous_run.sh \"$@\"" >&2
echo "This stub will be removed on 2026-06-02." >&2
exit 1
