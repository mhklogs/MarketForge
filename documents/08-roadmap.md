# MarketForge — Delivery Roadmap (v3)

> **Provenance note.** This roadmap was produced on **2026-09-29** from the same
> static analysis as the rest of `documents/` (see `00-index.md`). Backlog items are
> derived from the functional requirements in `02-functional-requirements.md`, the
> non-functional targets in `03-non-functional-requirements.md`, and the market
> findings in `01-market-analysis.md`. Timeline targets are `[TO BE VALIDATED]`
> where they depend on future estimates rather than shipped code.

> **Known doc gap.** `01-market-analysis.md` describes this repo as a "Jupyter
> market-research notebook" aimed at "learners, course reviewers". That does not
> match the shipped Flask + Gemini product-launch content generator. This roadmap
> follows the source tree; correcting `01-market-analysis.md` is PBI-11.

## 1. Objective & horizon

Marketing assets + research generator. This roadmap plans the next **5–6 weeks** of incremental delivery in
lockstep with the SDLC phases and traceability rules in `07-sdlc-lifecycle.md`
(Requirements → Design → Implement → Verify → Release/Operate → Improve).

Current shipped state: `https://marketforge-kappa.vercel.app` (production), source committed, v2 documentation set complete.
`app.py` is a Flask app exposing `POST /generate`, chaining three Gemini calls —
`MarketingCampaignBrief` → `AdCopy` → storyboard — with schema-constrained JSON
output, a PWA shell, and a Vercel deploy config.

## 2. Product backlog

Prioritised with MoSCoW. Items are phrased as outcomes (not tasks) and map to FR/NFR ids.

| ID | Item (outcome) | Source | Priority |
| --- | --- | --- | --- |
| PBI-01 | `POST /generate` returns the brief and ad copy conforming to the declared Pydantic schemas, or fails with an explicit error — never partial assets | FR-5, FR-1.01 | Must |
| PBI-02 | The storyboard is schema-enforced like the other two stages, closing the gap the README already flags | FR-5 | Must |
| PBI-03 | Every generative call records model, prompt version, and token usage, so a campaign's cost is attributable | FR-5 (inferred) | Must |
| PBI-04 | A missing or empty `GEMINI_API_KEY` produces a clear error at request time rather than a traceback | FR-8 | Must |
| PBI-05 | The product profile is validated and length-bounded before any of the three stages is invoked | NFR-5.4 | Should |
| PBI-06 | `POST /generate` is rate limited and no longer an unauthenticated, unmetered public endpoint | NFR-5.5 | Should |
| PBI-07 | Provider outages and timeouts return a typed error, with an explicit timeout and retry budget across the three chained calls | NFR-4.1 | Should |
| PBI-08 | Per-request cost ceiling and maximum output token budget are set and observable | NFR-4.2, NFR-4.3 | Should |
| PBI-09 | Prompt-injection exposure of the product profile field is assessed and documented | NFR-4.4 | Should |
| PBI-10 | Automated tests cover the three-stage chain and the schema contract | NFR-6.1 | Should |
| PBI-11 | `01-market-analysis.md` is corrected to describe the shipped product and its actual competitive set | doc accuracy (`01-market-analysis.md` §1, §5) | Should |
| PBI-12 | CI runs the test suite plus lint on every push, and the Vercel deploy stays green | NFR-6.3, NFR-6.2 | Should |
| PBI-13 | Generated drafts carry an in-product "requires human review" marker for claims and localization | market differentiator (§6) | Could |
| PBI-14 | Latency and cold-start figures measured against NFR-1 targets | NFR-1.1, NFR-1.5 | Won't (this horizon) |

## 3. Sprint plan

**Sprint cadence:** 1 week = 1 sprint; stand-up daily (15 min), sprint review + retrospective at the end of each sprint.

| Sprint | Goal | PBI delivered | Done/exit criteria | Phase (SDLC) |
| --- | --- | --- | --- | --- |
| Sprint 1 | Make all three assets schema-constrained | PBI-01, PBI-02 | storyboard returns structured scenes/timing/visuals; a schema violation surfaces as an error, not prose | Implement → Verify |
| Sprint 2 | Attribute cost and fail loudly on bad config | PBI-03, PBI-04 | token usage retrievable per stage; absent key yields a clear request-time error | Implement → Verify |
| Sprint 3 | Validate and bound the inputs | PBI-05, PBI-08 | malformed or oversized profile rejected before stage 1; cost budget trips below the ceiling | Verify |
| Sprint 4 | Protect the public endpoint | PBI-06, PBI-07 | rate limiting in place; simulated provider failure returns a typed error with a bounded retry budget | Verify |
| Sprint 5 | Test, pipeline, and correct the docs | PBI-09, PBI-10, PBI-11, PBI-12 | CI green on every push; `01-market-analysis.md` describes the shipped product | Verify → Release |
| Sprint 6 | Human-review affordance and release cut | PBI-13, backlog refinement | review marker visible on every generated asset; use-case walkthrough updated; release cut to `https://marketforge-kappa.vercel.app` | Release & Operate → Improve |

## 4. Ceremonies

- **Daily stand-up (15 min):** what shipped since yesterday, what's blocked, what's next — tied to the active sprint's PBI board.
- **Sprint review (30 min, end of sprint):** demo PBI outcomes against the sprint goal; update `05-use-cases.md` walkthrough where behavior changed.
- **Retrospective (30 min, end of sprint):** inspect + adapt; record one actionable improvement per sprint in git notes.
- **Backlog refinement (before sprint 1):** re-prioritise PBIs against latest market findings.

## 5. Burndown (planned)

Tracked as PBI points remaining per sprint. Planned trajectory below; the team records actuals at each sprint review. `[TO BE MEASURED]` until the first sprint completes.

| Sprint | Planned remaining points |
| --- | --- |
| Start | 14 |
| Sprint 1 | 12 |
| Sprint 2 | 10 |
| Sprint 3 | 8 |
| Sprint 4 | 6 |
| Sprint 5 | 3 |
| Sprint 6 (Done, 0) | 0 |

## 6. Rollout & deploy

- Build/deploy per `07-sdlc-lifecycle.md` §5 (release policy).
- Production: `https://marketforge-kappa.vercel.app` — Flask on Vercel via `vercel.json`; the PWA shell in `static/` ships with it.
- Health: a broken build blocks the next sprint's first commit; security findings are release blockers.

## 7. Risks

| Risk | Mitigation |
| --- | --- |
| Requirements drift vs. implemented code | PBI↔FR↔use-case traceability check per change (`07-sdlc-lifecycle.md` §3) |
| Unmeasured NFRs treated as done | `[TO BE MEASURED]` targets stay visible until instrumented |
| Burndown actuals fall off plan | Over-plan cut scope in the retrospective, not mid-sprint |
| Unauthenticated `/generate` endpoint burns the Gemini key | PBI-06 rate limiting is a release blocker, not a nice-to-have |
| Generated copy read as publish-ready creative | Keep the "starting draft, needs human review" limitation visible (PBI-13) |
| `01-market-analysis.md` misdescribes the product | PBI-11 corrects the doc; no market or pricing claim is made from it until then |
