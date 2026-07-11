# Related Repository Native-Mechanism Audits

These audits must precede adapter construction.

```text
Discover native mechanism
-> identify schedules, contracts, outputs, receipts, privacy, and consumers
-> classify capability
-> choose smallest compatible boundary
-> build only the missing connector
```

## Current status

| Repository | Audit state | Preliminary classification | Audit file |
|---|---|---|---|
| `StegVerse-Labs/Trumpality` | partial | shared-engine-dependent / native producer candidate | `integration/native-mechanism-audit.md` |
| `StegVerse-Labs/Administrations` | partial | shared-engine-dependent / institutional producer candidate | `integration/native-mechanism-audit.md` |
| `StegVerse-Labs/Giuffre-ality` | partial | shared-engine-dependent / privacy-restricted | `integration/native-mechanism-audit.md` |
| `StegVerse-Labs/Maxwellality` | partial | shared-engine-dependent / privacy-restricted | `integration/native-mechanism-audit.md` |
| `StegVerse-Labs/Epsteinality` | partial | shared-engine-dependent / privacy-restricted | `integration/native-mechanism-audit.md` |
| `StegVerse-Labs/StegSocials` | partial | publication-consumer-ready-partial | [StegSocials audit](StegSocials.md) |
| `StegVerse-Labs/VAwatchdog` | partial | privacy-restricted-manual-source-only | [VAwatchdog audit](VAwatchdog.md) |
| `StegVerse-Labs/StegScholar` | pending | unclassified | — |
| `StegVerse-Labs/Patents` | pending | unclassified | — |
| `StegVerse-Labs/Talarico` | pending | unclassified | — |
| `StegVerse-Labs/FREE-DOM_OverSight` | pending | unclassified | — |
| `StegVerse-Labs/Randolph_Geneaology_Hub` | pending | unclassified | — |
| `StegVerse-Labs/StegLearn` | pending | unclassified | — |
| `StegVerse-Labs/StegBiography` | pending | unclassified | — |

## Current findings

- Existing recurring scans are already present in several repositories.
- Multiple biography repositories delegate to shared `StegVerse/StegVerse-Core` workflows.
- StegSocials currently has a mature governed publication queue, admission checks, credential boundary, and receipts; broad recurring source discovery is not yet confirmed.
- VAwatchdog currently presents as a sensitive, source-tiered manual intake scaffold; recurring automated discovery is not yet confirmed.

## Enforcement boundary

No repository is adapter-ready until its audit covers current workflows, schedules, source lists, categorization, outputs, archives, receipts, privacy, handoff, and downstream consumers.
