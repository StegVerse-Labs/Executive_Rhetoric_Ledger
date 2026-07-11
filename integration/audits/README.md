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
| `StegVerse-Labs/Talarico` | pending | unclassified | — |
| `StegVerse-Labs/FREE-DOM_OverSight` | pending | unclassified | — |
| `StegVerse-Labs/Randolph_Geneaology_Hub` | pending | unclassified | — |
| `StegVerse-Labs/StegLearn` | pending | unclassified | — |
| `StegVerse-Labs/StegBiography` | pending | unclassified | — |

## Current findings

- Existing recurring scans are already present in several repositories.
- Multiple biography repositories delegate to shared `StegVerse/StegVerse-Core` workflows.
- StegSocials is both a governed publication system and a platform-source intake environment. LinkedIn, X, Facebook, and long-form surfaces may contribute claims, reactions, corrections, moderation events, deletions, and circulation evidence. Broad autonomous scanning remains unconfirmed.
- VAwatchdog interacts with VA, VBA, DOJ, OIG, FOIA, court, oversight, benefits, payment, identity, call-center, and IT environments that may supply or alter evidentiary state. Automated retrieval remains unconfirmed.
- StegScholar runs a daily StegDB canonical-overlay sync and interacts with scholarly publication, submission, DOI, citation, correction, retraction, and repository platforms. Peer review, citation count, venue prestige, and search rank remain source-posture signals rather than proof.
- Patents runs a daily StegDB canonical-overlay sync and declares a Patent Watcher, portfolio manifest, templates, allowlists, exclusions, and deadline policy. The current watcher implementation and external patent-office integrations remain unaudited.
- Platform interaction must be audited separately from repository workflows because platform state, visibility, edits, deletions, authentication, corrections, and access limitations can materially affect evidence posture.

## Enforcement boundary

No repository is adapter-ready until its audit covers current workflows, schedules, source lists, platform interactions, categorization, outputs, archives, receipts, privacy, handoff, and downstream consumers.
