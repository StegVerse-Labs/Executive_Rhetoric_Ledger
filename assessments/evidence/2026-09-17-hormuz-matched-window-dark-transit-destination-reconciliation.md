# Hormuz matched-window / dark-transit / destination reconciliation — 2026-09-17

**Goal Task ID:** `ERL-RC-OIL-FLOW-2026`  
**COSV:** `40000100100000`  
**Status:** `RESEARCH_ACTIVE / FINDING_NOT_AUTHORIZED / PUBLICATION_NOT_AUTHORIZED`

## Purpose

Reconstruct the closest public same-day and same-seven-day comparisons among U.S./CENTCOM-facilitated transit claims and Lloyd's List Intelligence, Kpler, IMF PortWatch, Windward, Vortexa, and TankerTrackers observations. Preserve preliminary-to-revised count changes, keep Hormuz waterborne throughput separate from bypass routes, and trace identifiable cargoes to destination arrival/discharge evidence where public records permit.

The comparison is source-relative. A number is not promoted merely because it is larger, newer, official, commercial, AIS-derived, or satellite-assisted.

## Measurement classes

- **US_FACILITATED_TRANSIT** — U.S.-stated or CENTCOM-assisted vessel movement.
- **AIS_DERIVED_TRANSIT** — movement observable from AIS-derived chokepoint data.
- **COMMODITY_VESSEL_PRELIMINARY** — Kpler near-real-time commodity-vessel count subject to later revision.
- **DARK_RECONSTRUCTED_TRANSIT** — movement added or detected through non-AIS/satellite/imagery/reconstruction.
- **NON_IRANIAN_LINKED_CARGO_TRANSIT** — Lloyd's defined ownership/trade/sanctions population, >10,000 dwt.
- **HORMUZ_OIL_VOLUME** — crude/products physically crossing Hormuz.
- **BYPASS_OIL_VOLUME** — pipeline, Red Sea, Gulf-of-Oman-terminal, or outside-strait STS export volume.
- **DESTINATION_ARRIVAL** — vessel arrival/berthing at destination.
- **DESTINATION_DISCHARGE** — independently evidenced cargo discharge.

## Seven-day vessel comparison

### Window: 2026-09-07 through 2026-09-13

| Provider / class | Publicly reconstructable observation | Total / average | Boundary |
|---|---|---:|---|
| IMF PortWatch-derived total vessel transits | Sep 7=5, Sep 8=6, Sep 9=3, Sep 10=5, Sep 11=8, Sep 12=2, Sep 13=8 | 37 / 5.29 per day | AIS-derived PortWatch chokepoint series; not a census of AIS-dark traffic |
| Kpler commodity-vessel reports | Sep 7=9; Sep 8 initially 6 then reported next day as 12; Sep 9 initially 7 then reported next day as 11; Sep 10=7; Sep 11=14; Sep 12-13 combined=14 | 67 latest-publicly-reported/reconstructed total for the window | Commodity-vessel population; preliminary daily reports change as later tracking evidence arrives; weekend public report provides a combined two-day count, not a defensible daily split |
| Lloyd's List Intelligence | at least 97 non-Iranian-linked transits; 47 westbound; 60 crude-tanker transits already captured | >=97 / >=13.86 per day | Cargo-carrying vessels >10,000 dwt in Lloyd's defined non-Iranian-linked population; explicitly preliminary and expected to revise upward as dark transits are verified |

These totals are **not interchangeable denominators**. The 37/67/>=97 spread is itself evidence of observation/classification differences, not proof that any one source is necessarily incorrect.

## U.S.-stated vs AIS bridge

A UKMTO weekly overview reported a seven-day presentation of 108 outbound plus 102 inbound movements when AIS-derived and U.S.-stated facilitated categories were combined. Its breakdown was 22 AIS-derived outbound + 23 AIS-derived inbound, versus 86 U.S.-stated facilitated outbound + 79 facilitated inbound. The report separately summarized U.S.-stated facilitated southern-route traffic at about 20/day versus about 6/day AIS-derived.

The arithmetic of the displayed facilitated subtotals (165 / 7 = 23.6/day) does not exactly equal the narrative "~20/day" summary. ERL preserves both values and treats the difference as an unresolved report-aggregation/method boundary rather than silently correcting either one.

The public report also states that U.S.-facilitated numbers are U.S.-stated, that overlap with AIS-derived counts is assumed to be limited, and that UKMTO cannot independently verify all facilitated/AIS-dark movements. Accordingly, the combined 210 presentation is not treated as an independently verified physical census.

## Preliminary -> revised Kpler evidence

The public reporting sequence demonstrates why initial visible counts must not overwrite later reconstructed state:

| Transit date | Initial/public early count | Later public reference | ERL state |
|---|---:|---:|---|
| 2026-09-08 | 6 | 12 | `REVISED_UPWARD` |
| 2026-09-09 | 7 | 11 | `REVISED_UPWARD` |
| 2026-09-14 | 4 | 7 | `REVISED_UPWARD` |
| 2026-09-15 | 4 | 12 | `REVISED_UPWARD` |

Kpler/Reuters repeatedly warns that vessels operating with AIS transponders off may be absent from early totals. ERL therefore preserves both initial and later counts. It does **not** claim every revision was caused exclusively by dark transit identification unless the provider says so for the particular vessel.

Windward's September 16 daily intelligence provides an independent mechanism check: with data as of September 15, it recorded nine Hormuz transits in the preceding 24 hours and stated that four of the nine were dark, including imagery-only detections. This demonstrates that a rolling observation combining imagery and AIS can diverge materially from a near-real-time commodity-AIS count even before vessel-class differences are considered.

## Same-day / near-same-day cross-section — September 15

- U.S. Energy Secretary Chris Wright said on September 16 that approximately **18 million barrels of oil and oil products** made it through Hormuz on Tuesday, September 15, with a seven-day running average of roughly **11 million bpd**.
- Kpler's September 16 preliminary report counted **4 commodity-vessel transits** for September 15; the September 17 report referred to **12** vessels for the prior day, preserving a 4 -> 12 public revision.
- Windward's September 16 report, using data as of September 15, recorded **9 transits in the past 24 hours**, including dark/imagery detections.

Barrels/day and vessel counts cannot be converted into each other without cargo state, vessel class, capacity/utilization, direction, and time-window alignment. This cross-section therefore establishes a measurement gap and revision behavior, not a truth/falsehood conclusion.

## Hormuz throughput vs bypass exports

### Hormuz-specific / waterway estimates

- Reuters reported on September 9 that the Energy Secretary had cited flows above 17 million bpd, while Kpler estimates were roughly 4.3–5 million bpd during the opaque dark-transit period.
- Vortexa's seven-day moving-average crude-plus-products flow **through Hormuz** was reported at roughly **8 million bpd**.
- TankerTrackers' current self-published 28-day decomposition reports **5.04 million bpd through Hormuz**.

### Bypass / outside-strait flows

- TankerTrackers reports another **2.49 million bpd** from oil terminals along the Gulf of Oman in the same complete 28-day decomposition, for 7.54 million bpd along its broader "US Navy blockade line."
- Reuters reported early-September Saudi Yanbu loadings of roughly **3.7 million bpd (Vortexa)** or **2.9 million bpd (Kpler)** before the East-West pipeline was shut following attacks. Yanbu is a Red Sea outlet and bypasses Hormuz.
- Reuters also reported Saudi Aramco use of STS transfers off Fujairah/Sohar outside the strait and at least 4 million barrels sold to China in the August transaction set.
- After the East-West pipeline shutdown, Reuters reported renewed Saudi use of Sohar/Oman STS transfer options.

These bypass figures are not added mechanically to Hormuz figures unless their date window, commodity class, and double-counting boundary are aligned. A cargo can cross Hormuz on a shuttle, be transferred outside the strait, and then appear in an outside-strait delivery chain; adding both legs as separate exported barrels would double count the same physical oil.

## Destination / discharge trace

### Confirmed destination arrival and berth: Al Marrouna -> Pakistan

The Qatari LNG carrier **Al Marrouna** crossed Hormuz on September 7 and arrived/berthed at Pakistan's Port Qasim / Engro Elengy Terminal on September 10. Port Qasim reporting cited approximately **142,217 cubic metres** / roughly **82,000 tonnes** of LNG. This is the strongest currently preserved public end-to-end example in this lane: Gulf loading -> Hormuz transit -> destination arrival/berth.

ERL classifies:
- `DESTINATION_ARRIVAL = CONFIRMED_PUBLIC_PORT_REPORTING`
- `DESTINATION_BERTH = CONFIRMED_PUBLIC_PORT_REPORTING`
- `DESTINATION_DISCHARGE = REPORTED_FOR_TERMINAL_DELIVERY / NATIVE_TERMINAL_METERING_NOT_CUSTODIED`

### Gas Polaris -> India

Kpler reported a single 0.06 mt ADNOC Das Island LNG cargo aboard **Gas Polaris bound for India**. The Kpler source establishes route/destination intent, not a final Indian discharge. ERL retains:
- `DESTINATION_INTENT = INDIA`
- `DESTINATION_ARRIVAL = NOT_YET_CUSTODIED`
- `DESTINATION_DISCHARGE = NOT_YET_CUSTODIED`

### Saudi crude STS -> China

Reuters reported at least **4 million barrels** of Saudi crude sold to China, including STS transfers to **Xin Hui Yang** (expected Ningbo) and **Xin Han Yang** (expected Zhanjiang). Current public evidence in this research pass does not independently prove that those exact cargoes discharged at the named Chinese terminals. ERL therefore retains:
- `DESTINATION_INTENT = CHINA / NINGBO_OR_ZHANJIANG`
- `DESTINATION_ARRIVAL = PENDING_FOR_EXACT_CARGO`
- `DESTINATION_DISCHARGE = PENDING_FOR_EXACT_CARGO`

### Macro destination evidence is not shipment identity

China's aggregate import/refinery data and European/Saudi customer data can establish market-level receipt or supply stress, but they may not be used to claim that a specific Hormuz or STS cargo reached a specific buyer without vessel/cargo linkage.

## What this advancement resolves

1. A matched seven-day public comparison now exists for PortWatch, latest-public Kpler reconstruction, and Lloyd's.
2. The preliminary/revised count lifecycle is explicitly preserved rather than silently replacing early data.
3. U.S.-stated facilitated traffic is separated from AIS-derived traffic and from independently reconstructed dark traffic.
4. Hormuz barrels are separated from Red Sea, Gulf-of-Oman terminal, pipeline, and outside-strait STS bypass flows.
5. At least one end-to-end energy cargo, Al Marrouna to Port Qasim, has public arrival/berth evidence after a Hormuz crossing.
6. Several destination-intent cases remain properly below the discharge-proof threshold.

## What remains unresolved

- exact CENTCOM/NCAGS/JMIC vessel-by-vessel facilitated manifests for matched calendar days;
- exact U.S. definition behind each daily "ships" and barrels/day statement;
- same-window barrel-volume series from Kpler, Vortexa, Windward, TankerTrackers, and official U.S. sources;
- fully reconstructed Sep 7–13 dark-transit daily sequence rather than weekly lower bounds;
- native terminal/metering evidence for destination discharge;
- exact Chinese discharge evidence for the cited Saudi STS cargoes;
- provider-independent review.

## Finding boundary

No falsehood, deception, intent, motive, or political-performance finding is authorized. Current evidence supports a narrower conclusion only: **public Hormuz measurements are drawn from materially different observation populations and revision cycles; dark-transit reconstruction explains part of the vessel-count divergence, while the oil-volume gap and destination-delivery denominator remain incompletely reconciled.**
