# UAP Disclosure / Documentary Feedback Loop — Research Candidate

Status: `research_candidate`
Date opened: 2026-08-15
Repository: `StegVerse-Labs/Executive_Rhetoric_Ledger`

## Originating observation

A noticeable increase in documentary-style UAP/UFO video and streaming content appears to have occurred over the last several years. A plausible explanation is that this media growth coincides with, and may be partly driven by, the United States government's incremental release, acknowledgment, reporting, hearing activity, declassification, and institutionalization of UAP-related material.

This document records that relationship as a **research hypothesis**, not a causal finding.

## Core hypothesis

`H1`: Incremental official UAP disclosure/reporting activity materially increased the supply, legitimacy, discoverability, or commercial viability of documentary-style UAP content.

Competing explanations must remain live:

- `H0`: the apparent increase is primarily a platform/distribution effect rather than a government-disclosure effect;
- `H2`: audience demand and algorithmic recommendation independently drove production;
- `H3`: a broader true-crime/investigative-documentary boom raised production across many subjects, with UAP content merely participating;
- `H4`: specific high-profile witnesses, whistleblowers, congressional hearings, or entertainment releases caused temporary spikes rather than a sustained disclosure-driven trend;
- `H5`: government and media activity are mutually reinforcing and neither direction alone explains the observed pattern.

## Research questions

1. Did documentary-style UAP publication volume materially increase from 2017 through 2026?
2. Do release spikes cluster around identifiable official events such as ODNI reports, AARO releases, congressional hearings, statutory changes, declassification events, or major witness testimony?
3. What is the lag between an official event and associated documentary/video publication?
4. Are the same source documents, witnesses, clips, or claims repeatedly reused across productions?
5. Does the language of productions change as the government vocabulary shifts from `UFO` toward `UAP`, formal reporting, classification, congressional oversight, and AARO?
6. Can the media increase be distinguished from the general growth of documentary-style streaming content?
7. Which productions introduce genuinely new evidence, and which primarily repackage existing claims?
8. Does renewed interest in older figures such as Bob Lazar correlate with new evidence about those figures, or with broader UAP disclosure cycles?

## Mandatory evidence-class separation

Evidence classes must remain in **different physical repository locations**. Classification metadata alone is insufficient. A source object must not share its canonical storage namespace with analytical conclusions, secondary reporting, documentary media, testimony, or reconstructed claims.

Canonical UAP workstream root:

`assessments/uap-media/`

Required physical namespaces:

- `assessments/uap-media/evidence/official-records/` — native or transformed authoritative government records, official reports, statutes, hearing records, agency releases, declassified records, and custody receipts tied to those records;
- `assessments/uap-media/evidence/testimony/` — first-person witness statements, sworn testimony, interviews, affidavits, and attributable witness transcripts; official hearing containers remain in `official-records`, while extracted witness testimony objects live here and point back to the official container;
- `assessments/uap-media/evidence/media-primary/` — documentary/video/audio productions being studied as media objects, including publication metadata and preserved source receipts;
- `assessments/uap-media/evidence/secondary-reporting/` — journalism, books, commentary, derivative reporting, and intermediary summaries;
- `assessments/uap-media/evidence/technical-scientific/` — peer-reviewed papers, laboratory results, physical/technical reference material, scientific standards, and independently verifiable technical evidence;
- `assessments/uap-media/evidence/archival-historical/` — historical records that are neither current official records nor secondary media, including contemporaneous archival material, directories, advertisements, historical photographs, and preserved institutional records;
- `assessments/uap-media/claims/` — atomic claims only; each claim references evidence objects by immutable identity and never embeds evidence as if it were the claim;
- `assessments/uap-media/chronologies/` — derived event timelines built from evidence references;
- `assessments/uap-media/lineage/` — claim-propagation and source-reuse graphs;
- `assessments/uap-media/controls/` — comparison corpora and non-UAP control datasets;
- `assessments/uap-media/analysis/` — statistical analysis, causal testing, hypothesis updates, and model-generated analytical products;
- `assessments/uap-media/reviews/` — contradiction review, independent reconstruction, reviewer findings, and adjudication artifacts;
- `assessments/uap-media/receipts/` — execution, validation, and reconstruction receipts that do not replace the custody records colocated with their source class.

### Separation invariants

1. **No source promotion by relocation.** Moving or copying an item into an `official-records` path cannot make it official; provenance determines class.
2. **No documentary-as-evidence collapse.** A documentary is stored as a `media-primary` object even when it displays an official record. The official record must be independently acquired and stored under `official-records` before it can be cited as such.
3. **No testimony-as-fact collapse.** Testimony is stored under `testimony`; any factual proposition derived from it is represented as a claim and requires its own corroborating evidence references.
4. **No secondary-source laundering.** Journalism or commentary cannot be copied into another class to increase evidentiary weight.
5. **Analysis never resides with evidence.** Confidence scores, causal inferences, hypothesis rankings, and model output remain under `analysis/` or `reviews/`.
6. **Cross-class linkage is by reference, not co-location.** Claim lineage and chronology may connect classes but must preserve each object's original class and provenance.
7. **Original and transformed forms remain distinguishable.** Native bytes, transformed text, transcripts, metadata extracts, and summaries must have explicit relationships and separate identities.
8. **Conflicting evidence stays preserved.** Contradictory evidence is not overwritten or merged into a consensus object.

## ERL-compatible evidence lanes

### A. Official-event chronology

Capture authoritative records for:

- ODNI UAP assessments and annual reports;
- AARO reports, case releases, historical reports, and presentations;
- congressional hearings and hearing records;
- enacted statutory reporting requirements and relevant authorization language;
- formally released or declassified records;
- official DoD, intelligence-community, NASA, or other relevant agency statements.

Canonical source location: `assessments/uap-media/evidence/official-records/`.

Each event should preserve publication date, event date, issuing authority, document identity, provenance, and source custody.

### B. Documentary/media chronology

Build a dated corpus of documentary-style releases across major platforms and independent channels.

Canonical source location: `assessments/uap-media/evidence/media-primary/`.

Record at minimum:

- title;
- publisher/platform;
- publication/release date;
- format and duration;
- named witnesses/officials;
- official documents cited;
- major claims;
- whether new primary evidence is introduced;
- whether the production relies on prior productions as evidence.

### C. Claim lineage

For recurring claims, trace:

`original evidence object -> atomic claim -> official acknowledgment/rebuttal -> intermediary reporting -> documentary reuse -> later derivative reuse`

Canonical derived location: `assessments/uap-media/lineage/`.

This is particularly important for Bob Lazar, Area 51/S-4 claims, alleged recovered craft, reverse-engineering claims, element 115, military sensor incidents, whistleblower claims, and recovered-material allegations.

### D. Causal testing

Do not treat temporal proximity as causation. Test whether official events predict media-production changes after controlling for:

- general documentary output;
- streaming-platform growth;
- search-interest changes;
- algorithmic amplification;
- major entertainment releases;
- independent breaking-news events.

Control data lives under `assessments/uap-media/controls/`; analytical results live under `assessments/uap-media/analysis/`.

Useful measures include event-window counts, lag distributions, source-reuse frequency, terminology changes, and control-topic comparisons.

### E. Documentary admissibility

A production may point to several distinct evidence classes, but the classes remain physically separate. A documentary object must never become the storage container for the underlying evidence it depicts.

Classify what a production contributes by reference to separately stored objects:

- authenticated official record;
- first-person testimony;
- technical/scientific evidence;
- archival/historical evidence;
- secondary reporting;
- dramatization/reconstruction;
- unsupported assertion;
- inference/speculation.

A documentary's existence or production quality must not increase the admissibility of the underlying claim.

## Bob Lazar sub-question

The Lazar story is a useful longitudinal test case because the principal public claims date to 1989 while renewed media cycles occur decades later.

Research should distinguish and physically separate:

1. archival or independently established biographical evidence;
2. Lazar's own testimony/interviews;
3. official records concerning facilities, programs, or government statements;
4. technical/scientific evidence concerning claimed technologies or materials;
5. secondary reporting about Lazar;
6. documentary productions that re-present Lazar's story;
7. atomic claims concerning S-4, recovered craft, reverse engineering, gravity propulsion, and stable element 115;
8. analysis of whether later facts are merely broadly consistent with the story or specifically corroborate a Lazar claim.

No one category may be stored as though it were another.

## Can this research report operate similarly to ERL?

Yes, **if it is implemented as an ERL-governed research workstream rather than as a narrative report**.

The same core ERL method applies:

`Observation -> candidate explanations -> expected signatures -> source acquisition -> class-specific custody -> experiments/comparisons -> observed results -> confidence updates -> remaining hypothesis space -> next experiment`

The report can therefore perform research similar to ERL over public and obtainable records by maintaining:

- physically separated evidence classes;
- source custody;
- chronology;
- claim lineage;
- competing hypotheses;
- controls;
- disconfirming evidence;
- confidence updates;
- independent reconstruction;
- durable receipts.

It cannot infer facts from classified material it cannot obtain, and it must distinguish an unresolved official case from evidence of extraterrestrial origin.

## Proposed first execution slice

`UAP-MEDIA-001`

Build independently sourced evidence stores and derived timelines covering 2017-01-01 through 2026-08-15:

1. official U.S. UAP disclosure/reporting/hearing/declassification evidence under `evidence/official-records/`;
2. documentary-style UAP releases under `evidence/media-primary/`;
3. separately stored testimony, secondary reporting, technical/scientific evidence, and archival/historical evidence as encountered;
4. derived chronologies under `chronologies/`, linked by immutable references rather than mixed-source storage.

Then perform a first-pass event-window comparison and source-lineage audit under `analysis/` and `lineage/` without asserting causal direction.

## Completion boundary

This candidate becomes assessable only after:

- physical evidence-class separation is installed and validation can detect class mixing;
- the official-event timeline has source custody;
- the media-release corpus has reproducible inclusion criteria;
- controls for general documentary growth are installed;
- Bob Lazar claims are separated into atomic claim/evidence pairs with class-correct source references;
- analysis outputs are physically separate from source evidence;
- at least one independent reconstruction reproduces the timeline and classifications.

No publication finding or causal conclusion is authorized from this candidate document alone.
