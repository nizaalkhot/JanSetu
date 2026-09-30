# JanSetu: Citizen-to-Policy Intelligence for BRICS

*"Jan" = people, "Setu" = bridge. It is easy to pronounce across BRICS and works as a brand. The working tagline is **"From a citizen's voice to a national budget line."***

---

## 1. Vision and Problem Framing

Citizen feedback, infrastructure data and budgets sit in separate systems. The result is misaligned spending, unnoticed gaps, and no way to tell whether a DPI initiative actually worked.

**JanSetu** closes that loop end to end:

**Listen → Understand → Correlate → Prioritise → Recommend → Track impact → Feed back to citizens**

It is built as a Digital Public Good (open source, open standards, sovereign-deployable), so each BRICS nation can run its own instance and still share anonymised insights across the bloc.

---

## 2. What Makes It Stand Out (USPs)

| # | Differentiator | Why judges and governments care |
|---|---|---|
| 1 | **Voice-first, low-literacy-first design.** Citizens speak in their own language and dialect over WhatsApp, Telegram, IVR or a web widget. | It reaches people who are normally excluded from digital governance. |
| 2 | **Demand-vs-Supply Gap Engine.** Each citizen request is geo-tagged and compared against infrastructure indices and budget allocations. | It exposes the *mismatch*, not just the complaints. |
| 3 | **Explainable Priority Score.** Every recommendation shows its evidence: number of requests, population affected, gap severity, budget headroom and equity weight. | Policymakers can defend the decisions in public. |
| 4 | **Multi-agent system on Google ADK.** Specialised agents for intake, translation, classification, geo-enrichment, analysis and policy drafting, plus a critic agent. | It is modular, auditable and easy to extend. |
| 5 | **Impact Loop.** After a project ships, the platform measures the change in complaint volume and sentiment, and in infrastructure indicators. | It answers "did this DPI investment work?", which most tools skip. |
| 6 | **BRICS Federation Layer.** Privacy-preserving cross-country comparison of the same problems (for example, rural water or last-mile internet) and of policies that worked elsewhere. | It is a natural fit for the BRICS Innovation theme. |
| 7 | **Closing the loop with citizens.** People get status updates in their own language ("Your request is now part of Project X"). | It builds trust and increases participation. |
| 8 | **Responsible AI by design.** Consent, PII redaction, bias audits, human-in-the-loop approval and audit logs. | It is government-grade and deployable. |

---

## 3. Core Feature Set

### A. Citizen Intake Channels
- WhatsApp Business API, Telegram bot, SMS, IVR/voice call, PWA web form, and a kiosk/CSC mode for assisted entry.
- Speech-to-text and text-to-speech through Google Cloud Speech and TTS, with Gemini handling multilingual understanding of Hindi, Portuguese, Russian, Mandarin, Arabic, Amharic, Persian, regional Indian languages and more.
- Dialect and code-mixed text (for example Hinglish) handled natively by Gemini.
- Offline-tolerant PWA that syncs later.

### B. Understanding Layer
- Translation and normalisation into a canonical English/pivot form, keeping the original text.
- Classification against a **unified development taxonomy** aligned to the UN SDGs (water, roads, health, education, digital connectivity, energy, sanitation and so on).
- Sentiment, urgency and severity scoring.
- Entity and location extraction, including village, ward and landmark resolution to geo-coordinates.
- Semantic deduplication and clustering so 5,000 similar requests become one demand signal.
- Coordinated-spam detection, to resist astroturfing.

### C. Data Fusion Layer
Ingest and harmonise:
- Census and demographics
- Infrastructure indices (roads, power, broadband, health facilities and so on)
- Public investment plans and budgets
- Satellite-derived indicators (night lights, road networks), optional

Everything is stored at a common geographic granularity with BRICS-specific adapters.

### D. Insight and Recommendation Engine
- **Demand Hotspot Map** at ward, district and state level.
- **Gap Score** = demand intensity × population affected ÷ current infrastructure supply.
- **Priority Score** = gap × urgency × equity weight × feasibility, adjusted for available budget.
- **Project Recommendation Cards**: problem, evidence, estimated beneficiaries, rough cost band, suggested scheme or budget head, and risks.
- **What-if Simulator**: "If we allocate X to rural broadband in these districts, how does the coverage gap change?"
- **Natural-language policy copilot** so officials can ask "Which 10 districts have the largest unmet primary healthcare demand?"

### E. Impact Measurement
- Before/after dashboards on DPI initiatives.
- Causal-inference-lite methods (difference-in-differences, synthetic control) against comparable regions.
- Citizen satisfaction re-survey, triggered automatically via the same channels.

### F. Federation and Open Platform
- Cross-country benchmarking through aggregated, anonymised indicators.
- Public open-data API and an annual "State of Citizen Voice" report generator.
- Plugin SDK for new languages, data connectors and country taxonomies.

---

## 4. Agent Architecture (Google ADK)

```
                      ┌─────────────────────┐
                      │  Orchestrator Agent │  (root agent, routes by task)
                      └─────────┬───────────┘
    ┌────────────┬──────────────┼───────────────┬───────────────┐
    ▼            ▼              ▼               ▼               ▼
 Intake &     Understanding   Data Fusion    Insight &      Impact &
 Channel      Pipeline        Agents         Recommendation Feedback
 Agents       (sequential)    (parallel)     Agents         Agents
```

| Agent | Role | ADK pattern |
|---|---|---|
| **Intake Agent** | Normalises messages from all channels and handles speech-to-text | LlmAgent + tools |
| **Language Agent** | Language ID, translation, dialect handling | LlmAgent |
| **Classifier Agent** | SDG taxonomy, urgency, sentiment, entity extraction (structured output) | LlmAgent with Pydantic schema |
| **Geo Agent** | Resolves locations to admin boundaries | Tool-using agent |
| **Dedup/Cluster Agent** | Embeddings and clustering | Tool (Vertex embeddings) |
| **Data Connector Agents** | Pull census, infrastructure and budget data | ParallelAgent |
| **Analyst Agent** | Computes gap and priority scores via code execution | LlmAgent + code-exec/tools |
| **Policy Drafting Agent** | Drafts recommendation briefs | LlmAgent |
| **Critic/Bias Auditor Agent** | Checks for bias, unsupported claims and equity issues | LoopAgent (draft → critique → revise) |
| **Impact Agent** | Runs before/after analysis | Scheduled workflow |
| **Citizen Feedback Agent** | Sends status updates in the citizen's language | LlmAgent |

**ADK practices to follow**
- SequentialAgent for the intake pipeline, ParallelAgent for data fetching, and LoopAgent for critique and refinement.
- Session state and memory services for multi-turn citizen conversations.
- MCP-style tool wrappers, or plain Python function tools, for data sources.
- ADK evaluation sets (`adk eval`) for regression tests of agent behaviour.
- Callbacks and guardrails for PII redaction before and after LLM calls.
- Agent-to-Agent (A2A) protocol for the federation layer, so each country's node can expose a standard agent interface.

---

## 5. System Architecture

```
Citizens ──► WhatsApp / Telegram / IVR / PWA
                     │
             Channel Gateway (FastAPI webhooks)
                     │
            Message Queue (Pub/Sub or Redis Streams)
                     │
        ┌────────────▼─────────────┐
        │  ADK Agent Runtime       │  (FastAPI service)
        └────────────┬─────────────┘
   ┌─────────────────┼──────────────────┐
   ▼                 ▼                  ▼
Postgres+PostGIS   Vector store      Object storage
(structured, geo)  (pgvector)        (audio, raw data)
   │                 │                  │
   └──────── Analytics layer (DuckDB / BigQuery) ───┐
                                                    ▼
                          FastAPI REST + WebSocket API
                                     │
                     Next.js Policymaker Dashboard + Citizen PWA
```

**Stack**
- **Backend:** Python 3.12, FastAPI, Pydantic v2, SQLAlchemy, Celery or Cloud Tasks for async jobs.
- **AI:** Google ADK, Gemini (Flash for high-volume intake, Pro for analysis), Vertex AI embeddings, Google Speech-to-Text and Text-to-Speech, Translation API as a fallback.
- **Data:** PostgreSQL + PostGIS + pgvector, BigQuery for heavy analytics (optional), dbt for transformations.
- **Frontend:** Next.js (App Router) + TypeScript, Tailwind + shadcn/ui, MapLibre GL or deck.gl for maps, Recharts/ECharts, next-intl for UI i18n with RTL support.
- **Infra:** Docker, Kubernetes or Cloud Run, Terraform, GitHub Actions, OpenTelemetry + Grafana.
- **Sovereignty option:** self-hostable with open-source models (for example Gemma) for countries that require on-premise data.

---

## 6. Data Model (Key Entities)

- `citizen_request` (id, channel, original_text, audio_uri, language, translated_text, category, urgency, sentiment, geo_point, admin_unit_id, cluster_id, consent_flags)
- `admin_unit` (hierarchical geography, country, population, demographic vector)
- `infra_indicator` (admin_unit_id, sector, metric, value, year, source)
- `investment_plan` (scheme, sector, admin_unit_id, allocated, spent, timeline)
- `demand_cluster` (centroid, size, summary, SDG tag, trend)
- `recommendation` (project, evidence, score components, status, reviewer, audit trail)
- `impact_assessment` (project_id, pre/post metrics, method, confidence)

---

## 7. Responsible AI, Privacy and Security

- **Consent-first:** explicit opt-in, purpose limitation, right to delete.
- **PII redaction** (Cloud DLP or a custom NER model) before anything reaches analytics.
- **Differential privacy and k-anonymity** on any cross-border or public output.
- **Bias and equity audits:** check for over-representation of digitally connected groups and re-weight accordingly. This is essential, since loud areas should not automatically win.
- **Human-in-the-loop:** AI recommends, officials approve. Everything is logged.
- **Explainability:** every score is traceable to its inputs.
- **Security:** OAuth2/OIDC, RBAC by ministry and region, encryption at rest and in transit, rate limiting, and prompt-injection defences on citizen-submitted text, which is untrusted input.
- **Compliance mapping:** India DPDP Act, Brazil LGPD, Russia's 152-FZ, China PIPL, South Africa POPIA. The design is modular so each country's rules can be swapped in.

---

## 8. Frontend Experience

**Policymaker Dashboard**
1. Command-centre map with demand heatmaps and a gap-score layer toggle.
2. Priority list with filters by sector, region and budget.
3. Recommendation detail page: evidence, simulation, and approve/reject/comment.
4. Conversational copilot ("Ask JanSetu").
5. Impact tracker per project.
6. BRICS comparison view.

**Citizen PWA and bots**
- Voice-recording button, large icons, language picker, status tracker, and community-upvote of existing requests.

**Design notes:** WCAG 2.2 AA, low-bandwidth mode, RTL and multi-script fonts.

---

## 9. Revenue Model

The core stays open source as a Digital Public Good. Revenue comes from services built on top of it:

1. **Managed SaaS / hosting for governments** (sovereign cloud deployments, SLAs, support), priced per administrative unit or per million citizens.
2. **Premium analytics modules:** causal impact engine, satellite data fusion and advanced what-if simulation.
3. **Integration and customisation services:** connectors to national ID, e-gov portals, budget systems and local languages.
4. **Multilateral and donor-funded rollouts:** World Bank, NDB (BRICS New Development Bank), UNDP and similar, where the platform supports SDG monitoring.
5. **Data and insight products:** anonymised "Citizen Voice Index" reports for think-tanks, development agencies and CSR teams.
6. **Training and certification** for civil servants.
7. **Marketplace for language and sector packs** built by the community.

**Pitch line:** *"Open core for trust, paid operations for scale."*

---

## 10. Implementation Roadmap

| Phase | Duration | Deliverables |
|---|---|---|
| **0. Discovery and design** | Weeks 1–2 | Taxonomy, data source mapping, personas, architecture, success metrics |
| **1. Foundation** | Weeks 3–5 | Repo and CI/CD, FastAPI skeleton, Postgres/PostGIS, auth, ADK project setup |
| **2. Intake and understanding** | Weeks 6–9 | WhatsApp/Telegram/web channels, speech pipeline, language and classification agents, dedup and clustering |
| **3. Data fusion** | Weeks 8–11 | Connectors for demographic, infrastructure and investment data, plus a synthetic/demo data generator |
| **4. Insight engine** | Weeks 10–14 | Gap and priority scoring, recommendation agents, critic loop, explainability |
| **5. Dashboard** | Weeks 11–15 | Next.js map, priority list, copilot, recommendation workflow |
| **6. Impact and federation** | Weeks 15–18 | Impact tracker, citizen feedback loop, cross-country benchmarking |
| **7. Hardening and launch** | Weeks 18–20 | Security review, load tests, bias audit, docs, pilot with one region |

**If this is a hackathon or competition with a short timeline,** build this MVP slice: WhatsApp/web voice intake → classification and clustering → a gap-score map → one AI-generated recommendation with evidence → a demo of the impact loop on synthetic data. Show two or three languages live.

---

## 11. Repository Structure

```
jansetu/
├── apps/
│   ├── api/                # FastAPI
│   │   ├── routers/ services/ schemas/ core/
│   ├── agents/             # ADK agents
│   │   ├── intake/ language/ classifier/ geo/
│   │   ├── analyst/ policy/ critic/ impact/ citizen_feedback/
│   │   └── evals/          # adk eval sets
│   └── web/                # Next.js (dashboard + PWA)
├── packages/
│   ├── taxonomy/           # SDG-aligned categories, multilingual
│   ├── connectors/         # country data adapters
│   └── scoring/            # gap and priority algorithms (unit-tested)
├── data/                   # synthetic datasets, seeds
├── infra/                  # Terraform, Docker, K8s
├── docs/                   # ADRs, DPG documentation, API spec
└── .github/workflows/
```

---

## 12. Engineering Best Practices

- Monorepo with typed contracts (OpenAPI → generated TypeScript client).
- Test pyramid: unit tests for scoring, integration tests for agents with mocked LLMs, ADK eval sets for behaviour, Playwright for the UI.
- Evaluation of multilingual quality per language (translation and classification accuracy), tracked as a public scorecard.
- Prompt and version registry, with LLM cost and latency tracking.
- Caching and batching (Gemini Flash for bulk work) to control cost.
- Observability: traces per citizen request across every agent step.
- DPG compliance: open licence (Apache-2.0), documentation, privacy-by-design, SDG relevance, and do-no-harm assessment, following the Digital Public Goods Alliance standard.
- Fallbacks when LLM or channel services fail, and graceful degradation for low connectivity.

---

## 13. Success Metrics (KPIs)

- **Coverage:** languages supported, share of requests coming from rural or low-literacy users.
- **Quality:** classification F1 per language, geo-resolution accuracy, recommendation acceptance rate by officials.
- **Impact:** time from request to project decision, change in complaint volume after a project, budget-alignment improvement.
- **Trust:** citizen satisfaction and repeat participation.
- **Scale:** requests per second, cost per processed request.

---

## 14. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Digital-divide bias | Equity re-weighting, assisted kiosk channel, voice and IVR support |
| LLM hallucination in recommendations | Grounded retrieval, critic agent, evidence links, human approval |
| Data availability varies by country | Adapter pattern, synthetic data, phased rollout |
| Political sensitivity | Neutral taxonomy, transparent scoring, country-controlled deployment |
| Spam or manipulation | Dedup, rate limits, anomaly detection, verified-channel weighting |
| Dialect and low-resource language quality | Continuous evaluation, community correction feedback loop |

---

## 15. The Pitch in Three Sentences

1. **JanSetu** turns millions of voices, in any BRICS language, into evidence-backed, explainable development priorities.
2. It does not just collect feedback: it **compares citizen demand against infrastructure supply and public budgets**, then **measures whether the resulting investment worked**.
3. It is an open, sovereign-deployable Digital Public Good with a federated BRICS layer, so nations can **learn from each other without sharing raw citizen data**.

