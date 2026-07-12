#!/usr/bin/env python3
"""Run local activation validation checks.

This runner executes the reusable validators that back the repo activation gate.

Checks:
1. producer export examples
2. producer acknowledgment examples and succession
3. validation-result receipts
4. activation-state manifest
5. governance-pattern entries
6. machine-readable assessment Political Influence Trees and source receipts
7. machine-readable primary-record intake queues
8. individualized force-event packets
9. related-repository network manifest and documentation
10. related-repository capability registry
11. repository contract-audit registry
12. portable FREE-DOM evidence intake packets
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = [
    [sys.executable, str(ROOT / "scripts" / "validate_producer_exports.py")],
    [sys.executable, str(ROOT / "scripts" / "validate_producer_acknowledgments.py")],
    [sys.executable, str(ROOT / "scripts" / "validate_validation_results.py")],
    [sys.executable, str(ROOT / "scripts" / "validate_activation_state.py")],
    [sys.executable, str(ROOT / "scripts" / "validate_governance_patterns.py")],
    [sys.executable, str(ROOT / "scripts" / "validate_assessment_trees.py")],
    [sys.executable, str(ROOT / "scripts" / "validate_primary_record_intake.py")],
    [sys.executable, str(ROOT / "scripts" / "validate_force_event_packets.py")],
    [sys.executable, str(ROOT / "scripts" / "validate_related_repository_network.py")],
    [sys.executable, str(ROOT / "scripts" / "validate_repository_capabilities.py")],
    [sys.executable, str(ROOT / "scripts" / "validate_repository_contract_audits.py")],
    [sys.executable, str(ROOT / "scripts" / "validate_portable_evidence_intake.py")],
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
