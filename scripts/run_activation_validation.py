#!/usr/bin/env python3
"""Run local activation validation checks.

This runner executes the reusable validators that back the repo activation gate.

Checks:
1. producer export examples
2. validation-result receipts
3. activation-state manifest
4. governance-pattern entries
5. machine-readable assessment Political Influence Trees and source receipts
6. machine-readable primary-record intake queues
7. individualized force-event packets
8. related-repository network manifest and documentation
9. related-repository capability and contract-audit registry
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = [
    [sys.executable, str(ROOT / "scripts" / "validate_producer_exports.py")],
    [sys.executable, str(ROOT / "scripts" / "validate_validation_results.py")],
    [sys.executable, str(ROOT / "scripts" / "validate_activation_state.py")],
    [sys.executable, str(ROOT / "scripts" / "validate_governance_patterns.py")],
    [sys.executable, str(ROOT / "scripts" / "validate_assessment_trees.py")],
    [sys.executable, str(ROOT / "scripts" / "validate_primary_record_intake.py")],
    [sys.executable, str(ROOT / "scripts" / "validate_force_event_packets.py")],
    [sys.executable, str(ROOT / "scripts" / "validate_related_repository_network.py")],
    [sys.executable, str(ROOT / "scripts" / "validate_repository_capabilities.py")],
]


def main() -> int:
    for command in CHECKS:
        label = " ".join(command)
        print(f"RUN {label}")
        result = subprocess.run(command, cwd=ROOT, check=False)
        if result.returncode != 0:
            print(f"FAIL {label}", file=sys.stderr)
            return result.returncode
        print(f"PASS {label}")

    print("Activation validation checks completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
