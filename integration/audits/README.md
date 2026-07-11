# Related Repository Native-Mechanism Audits

These audits must precede adapter construction.

```text
Discover native mechanism
-> identify schedules, contracts, outputs, receipts, privacy, platforms, and consumers
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
| `StegVerse-Labs/StegSocials` | partial | platform-interacting publication and source-intake system | [StegSocials audit](StegSocials.md) |
| `StegVerse-Labs/VAwatchdog` | partial | platform-interacting privacy-restricted evidence intake | [VAwatchdog audit](VAwatchdog.md) |
| `StegVerse-Labs/StegScholar` | partial | scheduled canonical-sync scholarly-context producer | [StegScholar audit](StegScholar.md) |
| `StegVerse-Labs/Patents` | partial | scheduled canonical-sync patent-monitoring and portfolio producer | [Patents audit](Patents.md) |
| `StegVerse-Labs/Talarico` | partial | public-figure manual source only / blocked incomplete | [Talarico audit](Talarico.md) |
| `StegVerse-Labs/FREE-DOM_OverSight` | partial | privacy-restricted oversight clearinghouse | [FREE-DOM_OverSight audit](FREE-DOM_OverSight.md) |
| `StegVerse-Labs/Randolph_Geneaology_Hub` | partial | historical identity and genealogy context producer | [Randolph Genealogy audit](Randolph_Geneaology_Hub.md) |
| `StegVerse-Labs/StegLearn` | partial | educational publication consumer and private learning-receipt system | [StegLearn audit](StegLearn.md) |
| `StegVerse-Labs/StegBiography` | partial | shared-engine-dependent biographical context producer | [StegBiography audit](StegBiography.md) |

## Current findings

- All fourteen declared repositories now have at least a partial native-mechanism and platform audit.
- Existing recurring scans are already present in several repositories.
- Multiple biography repositories delegate to shared `StegVerse/StegVerse-Core` workflows.
- StegSocials is both a governed publication system and a platform-source intake environment.
- VAwatchdog and FREE-DOM_OverSight require privacy-preserving evidence boundaries and cannot export raw sensitive material.
- StegScholar and Patents run daily StegDB canonical-overlay synchronization.
- Talarico remains blocked-incomplete because only a minimal public-figure purpose is currently documented.
- Randolph_Geneaology_Hub has canonical identity, source registry, and evidence-grading mechanisms but requires living-person and DNA privacy controls.
- StegLearn may consume reviewed ledger content for education, but learner records and child data must not flow into the ledger.
- StegBiography remains dependent on the unaudited shared biography engine and requires identity and privacy review.
- Platform interaction must be audited separately from repository workflows because platform state, visibility, edits, deletions, authentication, corrections, and access limitations can materially affect evidence posture.

## Enforcement boundary

No repository is adapter-ready until its audit covers current workflows, schedules, source lists, platform interactions, categorization, outputs, archives, receipts, privacy, handoff, and downstream consumers.

The next phase is not generic adapter construction. It is contract discovery and capability verification for the most mature native producers and consumers.
