# Orli Shull AI Governance — Cross-Domain Comparison Matrix

Candidate: `ERL-2026-09-03-ORLI-SHULL-AI-GOVERNANCE-COLLAPSE-001`  
Owner: Issue `#63`  
Handoff: `docs/ORLI_SHULL_AI_GOVERNANCE_COLLAPSE_MIRROR_HANDOFF.md`  
State: **RESEARCH ACTIVE / PARTIAL**  
Finding authorized: **false**  
Publication authorized: **false**

## Purpose

Test the candidate transition:

`observation -> inference -> authoritative state -> consequence`

against real governance regimes that regulate automated or AI-assisted decisions. This matrix separates inference authority from consequence authority and records whether a human can merely observe a system, must review it, can override it, can stop it, can reverse its output, or must provide an affected person with a challenge/appeal mechanism.

This is comparative evidence, not a finding that any one regime is sufficient, deficient, or endorsed by the source author.

## Matrix

| Domain / regime | AI or automated role | Inference can directly acquire consequence authority? | Human role | Challenge / explanation rights | Reversibility / stop authority | Temporal posture | Candidate implication |
|---|---|---|---|---|---|---|---|
| U.S. credit decisions — ECOA / Regulation B + CFPB Circular 2022-03 | Complex algorithms may participate in underwriting and adverse-action decisions. | **Bounded.** A creditor may use an algorithm, but adverse action remains legally attributable to the creditor and the creditor must identify the specific principal reasons actually used. Opacity is not a defense. | No categorical human pre-approval requirement identified in this source set. Institutional accountability remains with the creditor. | Affected applicant must receive specific and accurate reasons for adverse action. This creates post-decision contestability and exposes misinformation/inadequate information to correction. | The source establishes explanation/accountability, not an explicit real-time stop or mandatory reversal right. Existing correction/appeal mechanisms may operate outside this source set. | Primarily consequence-then-explanation; the notice occurs when adverse action is taken. | Demonstrates that inference may produce consequence while law still refuses to let the institution collapse model opacity into unreviewable authority. Explanation is a governance boundary, but not equivalent to pre-consequence interruption. |
| New York City employment — Local Law 144 AEDT | Automated employment decision tools may screen candidates or employees. | **Yes, within bounded procedural conditions.** Use is permitted after required audit/publication/notice conditions are met; the law does not itself require a human to approve each tool-assisted employment decision. | Human presence is not the central control in the cited requirements. Governance is implemented through pre-use bias audit, transparency, notice, and complaint mechanisms. | Candidates/employees must receive notice; DCWP accepts complaints for specified violations. The cited official materials do not establish a decision-specific right to demand human reconsideration of every AEDT output. | No explicit output-level override/stop/reversal requirement identified in the cited official materials. | Some governance occurs **before** use: bias audit and notice precede deployment/assessment; complaint operates afterward. | Useful discriminator against the proposition that governance necessarily requires a human interrupting each inference. Structural preconditions can constrain consequence without output-level human veto authority. |
| European Union — AI Act Article 14, high-risk AI | High-risk AI systems may provide outputs used in decisions affecting health, safety, or fundamental rights. | **Not unbounded.** Systems must be designed for effective human oversight; for specified remote biometric identification uses, action/decision based on identification generally requires separate verification and confirmation by two qualified humans, subject to statutory exceptions. | Human overseers must be able to understand limitations, monitor operation, resist automation bias, correctly interpret output, decide not to use the system, disregard/override/reverse output, and interrupt the system into a safe state. | Article 14 itself centers operator oversight rather than a universal affected-person appeal right; other AI Act provisions and applicable law may create complaint/rights mechanisms outside this matrix row. | **Explicit.** Oversight includes disregard, override, reverse, intervene, and interrupt/stop capabilities as appropriate and proportionate. | Strongly pre-consequence and in-operation for covered high-risk uses. | Closest observed statutory analogue to the candidate's "interrupt the collapse" concept, but it shows that effective interruption depends on actual competence, training, authority, and technical ability—not nominal human presence. |
| U.S. federal agencies — OMB M-24-10, rights-/safety-impacting AI | Federal agencies may use AI in decisions/actions that significantly affect rights or safety subject to minimum risk-management practices. | **Bounded.** Agencies must identify decisions/actions where AI is not permitted to act without additional human oversight, intervention, and accountability. | Agencies must train operators, address automation bias, add human oversight for significant impacts, and use appropriate alternatives/fail-safes where immediate intervention is impracticable. | For covered rights-impacting use, the memorandum requires opportunities to appeal to a human reviewer where required by the policy framework; where appeal cannot be provided because of law, government-wide guidance, or impracticability, agencies must establish alternative human-oversight mechanisms. It also requires an opt-out to a human alternative where practicable, with stated exceptions/waiver conditions. | Agencies must mitigate newly identified risks and stop using AI when risks exceed acceptable levels and mitigation is insufficient. | Mix of pre-use assessment, ongoing monitoring, periodic review, decision-time human oversight, and post-decision appeal/alternative mechanisms. | Demonstrates a layered model: human authority is not a single "loop" but a set of distinct intervention points—design, deployment, operation, individual appeal, opt-out, risk escalation, and system shutdown. |

## Primary sources

### U.S. credit / ECOA

- Consumer Financial Protection Bureau, **Consumer Financial Protection Circular 2022-03: Adverse action notification requirements in connection with credit decisions based on complex algorithms**.  
  https://www.consumerfinance.gov/compliance/circulars/circular-2022-03-adverse-action-notification-requirements-in-connection-with-credit-decisions-based-on-complex-algorithms/
- Consumer Financial Protection Bureau, **Regulation B § 1002.9 — Notifications**.  
  https://www.consumerfinance.gov/rules-policy/regulations/1002/2023-04-19/9/

### NYC automated employment decisions

- New York City Department of Consumer and Worker Protection, **Automated Employment Decision Tools (AEDT)**.  
  https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page
- NYC311, **Automated Employment Decision Tools**.  
  https://portal.311.nyc.gov/article/?kanumber=KA-03552

### European Union AI Act

- EUR-Lex, **Regulation (EU) 2024/1689, Article 14 — Human oversight**.  
  https://eur-lex.europa.eu/eli/reg/2024/1689

### U.S. federal agency AI governance

- Office of Management and Budget, **M-24-10, Advancing Governance, Innovation, and Risk Management for Agency Use of Artificial Intelligence** (2024).  
  https://www.whitehouse.gov/wp-content/uploads/2024/03/M-24-10-Advancing-Governance-Innovation-and-Risk-Management-for-Agency-Use-of-Artificial-Intelligence.pdf

## Initial discriminators

1. **Human presence is not equivalent to human authority.** The EU AI Act specifies concrete operator capabilities—ignore, override, reverse, interrupt—while NYC Local Law 144 largely governs conditions of use rather than each individual decision.
2. **Contestability can occur after consequence.** ECOA requires specific reasons for adverse credit action, providing a correction/contestability surface without requiring pre-decision human veto.
3. **Governance can exist at multiple transition points.** OMB M-24-10 distributes controls across pre-use review, operational oversight, individual appeal/opt-out, risk mitigation, and system shutdown.
4. **A structural control can constrain collapse without a universal human reviewer.** NYC's audit/notice regime is an example to test against any claim that only human interruption can prevent inference from acquiring institutional consequence.
5. **Authority must be distinguishable from cognition.** In all four regimes, the legal/institutional actor remains accountable even where the computational system produces the operative score, recommendation, classification, or decision input.

## Evidence gaps / next work

- Custody the native Orli Shull LinkedIn permalink, complete post text, timestamp, and edit state.
- Add at least one benefits/public-services case and one healthcare case with primary-source governance documentation.
- Identify a deployed system where nominal human review failed because the reviewer lacked time, information, competence, or authority.
- Identify a disconfirming case where automated finalization is bounded, reversible, demonstrably superior, and does not materially collapse unresolved identity or context.
- Separate rights afforded to the **operator** from rights afforded to the **affected person** in every added row.
- For each domain, distinguish pre-consequence control, decision-time control, post-consequence contestability, and system-level shutdown authority.

## Current assessment posture

The current evidence supports a narrower proposition than the source framing: the meaningful governance variable is not simply whether a human is "in the loop," but whether the system preserves distinct authority boundaries and supplies effective mechanisms at the points where an inference may acquire consequence. The evidence is not yet sufficient to determine which combination of controls is necessary or sufficient across domains.
