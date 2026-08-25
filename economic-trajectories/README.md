# Economic Trajectories

This directory contains two independent national evidence lanes and a comparison-only overlay.

- `canada/trajectory.v1.json`
- `united-states/trajectory.v1.json`
- `comparison/overlay.v1.json`
- `measurement-dictionary.v1.json`
- `research-lanes.v1.json`

`research-lanes.v1.json` drives weekly, independent official-source monitoring for Canada and the United States. Source changes are fingerprinted and routed to declared national gaps as review tasks. The comparison overlay has no source adapters and consumes only independently reviewed national findings.

Generated automation receipts live on the governed `automation/economic-research-lanes` candidate branch and remain non-evidentiary until reviewed.

The comparison layer may consume only reviewed national finding IDs. It may not compare raw observations or infer an effect absent from either national record.

See:

- `CANADA_ECONOMIC_TRAJECTORY_MIRROR_HANDOFF.md`
- `US_ECONOMIC_TRAJECTORY_MIRROR_HANDOFF.md`
- `COMPARATIVE_ECONOMIC_TRAJECTORIES_MIRROR_HANDOFF.md`
- `standards/economic-trajectory-comparison-standard.md`
