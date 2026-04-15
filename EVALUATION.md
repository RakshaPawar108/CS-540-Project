# Performance Evaluation Plan
**CS 540 — Medical Chatbot Strategy Comparison (Team Pentacle)**

---

## Team Assignments

| Member | Responsibility |
|--------|---------------|
| P1 | LangSmith integration |
| P2 | Vector DB hosting and seeding (all domains) |
| P3 | Dataset 2 generation |
| P4 | Performance script + Google Sheets logging |
| P5 | Chatbot UI |
| All | Run evaluation sessions in parallel once Dataset 2 is ready |
| Shared | Qualitative analysis with medical professionals (one lead + all contribute) |

---

## Dependency Order

Tasks have hard dependencies. Nothing should be run out of order.

```
Phase 1 — Infrastructure (Parallel, no dependencies between members)
├── P1: Integrate LangSmith into all 4 strategy endpoints
├── P2: Host ChromaDB on a server + seed all 5 domain groups
├── P3: Generate Dataset 2 from PubMedQA
├── P4: Write performance script + set up Google Sheet
└── P5: Build chatbot UI

Phase 2 — Integration & Smoke Test (all depend on Phase 1)
├── All connect to hosted vector DB
├── P1 verifies LangSmith traces appear for all 4 strategies
├── P4 does a dry run of the performance script on 1 session
└── P2 confirms vector DB is reachable from all 5 machines

Phase 3 — Parallel Evaluation (depends on Phase 2 passing)
└── All 5 members run their session subset simultaneously
    └── Results auto-logged to shared Google Sheet

Phase 4 — Analysis (depends on Phase 3)
├── Aggregate Google Sheet results
└── Qualitative sessions with medical professionals
```

---

## Phase 1 — Infrastructure Details

### P1 — LangSmith Integration

**Goal:** Every LLM call across S1–S4 is automatically traced with latency, token counts, and cost.

**What to do:**
- Add `LANGCHAIN_API_KEY`, `LANGCHAIN_TRACING_V2=true`, `LANGCHAIN_PROJECT` to `.env`
- Wrap LangChain LLM calls in `llm_service.py` with LangSmith tracing
- Tag each trace with `strategy` (S1/S2/S3/S4) and `session_id` so runs are filterable in the dashboard

**What LangSmith covers automatically:** latency, prompt tokens, completion tokens, cost (if model pricing is configured)

**Verify:** After a test call to each endpoint, confirm traces appear in the LangSmith project dashboard with correct tags.

---

### P2 — Vector DB Hosting and Seeding

**Goal:** A single hosted ChromaDB instance reachable by all 5 members' machines during evaluation.

**Hosting options (pick one):**
- Deploy ChromaDB server mode on a shared VM (GCP/AWS/Render) — all members point `CHROMA_HOST` at it
- Use a free-tier managed vector DB (Pinecone, Weaviate Cloud) if self-hosting is complex

**Seeding:**
- P2 runs `seed_db.py` for all 5 domain groups (or coordinates each member to run their own `--member N`)
- All groups load into the **same collection** — combined coverage of all medical domains
- P2 verifies final chunk count and collection size after all groups are loaded

**Domain groups to seed:**

| Group | Domain | Queries (~10 each) |
|-------|--------|-------------------|
| 1 | Cardiovascular & Respiratory | Heart failure, hypertension, stroke, asthma, COPD, ARDS |
| 2 | Oncology & Hematology | Breast/lung/colorectal cancer, leukemia, lymphoma, immunotherapy |
| 3 | Neurology & Mental Health | Alzheimer, Parkinson, epilepsy, depression, schizophrenia |
| 4 | Infectious Disease & Immunology | Antibiotics, COVID-19, sepsis, HIV, vaccines, autoimmune |
| 5 | Metabolic, Endocrine & Pharmacology | Diabetes, obesity, thyroid, drug interactions, renal/liver disease |

~10 queries × 200 abstracts × 5 groups = **~10,000 unique abstracts** in the shared vector store.

**Important:** PubMedQA source abstracts are intentionally **not** pre-loaded. The RAG pipeline must retrieve the correct context from a large noisy corpus — this is what makes the context recall metric meaningful.

**Verify:** Query the hosted ChromaDB from two different machines, confirm retrieval returns results. Check total document count matches expected range.

---

### P3 — Dataset 2 Generation

**Goal:** 50 multi-turn evaluation sessions (10 per domain) derived from PubMedQA, with Claude-generated follow-up questions and reference answers. Output is an Excel file shared with the team.

**Why Claude-generated follow-ups:**
Splitting `long_answer` into fragments produces unreliable reference answers — the text is 2–4 sentences total and doesn't consistently follow a finding → evidence → implication structure. Claude generates contextually meaningful follow-up Q&A pairs grounded in the actual abstract, giving reliable reference answers for BERTScore scoring.

> **Important distinction:** Claude is used here only for **dataset creation** (one-time, offline). Evaluation metrics are still computed without any LLM calls.

---

**Source:** PubMedQA `pqa_labeled` — 1,000 expert-labeled questions  
**Fields used:**
- `question` — Turn 1 input
- `long_answer` — Turn 1 reference answer (used in full, not split)
- `final_decision` — yes / no / maybe (Turn 1 label accuracy ground truth)
- `CONTEXTS` — source abstract paragraphs fed to Claude for grounded follow-up generation + used as context recall ground truth during eval
- `MESHES` — MeSH tags (domain filtering per member)

---

**Generation process (per member, 10 sessions each):**

1. Filter PubMedQA by MESH domain keywords to get the member's question subset
2. For each selected entry, call Claude with the following prompt structure:

   > "Given this PubMed research question, its reference answer, and the source abstract, generate exactly 2 follow-up questions a clinician might ask next, along with reference answers grounded strictly in the abstract text. Do not use outside knowledge. Keep each reference answer to 2–3 sentences."

   Inputs provided per call: `question`, `long_answer`, `final_decision`, and the full `CONTEXTS` paragraphs

3. Parse Claude's structured response into Turn 2 and Turn 3 Q&A pairs
4. Write all sessions to a shared Excel file

**~50 Claude API calls total — negligible cost.**

---

**Session structure (3 turns each):**

```
Session
├── pubid, topic, final_decision
├── contexts[]          ← PubMedQA source paragraphs, NOT loaded into vector DB
│                          used as: (a) Claude grounding context, (b) context recall ground truth
└── turns[]
    ├── Turn 1: original PubMedQA question
    │           reference_answer: full long_answer
    │           ground_truth_label: yes / no / maybe
    │
    ├── Turn 2: Claude-generated follow-up question
    │           reference_answer: Claude-generated answer grounded in CONTEXTS
    │           ground_truth_label: null
    │
    └── Turn 3: Claude-generated follow-up question
                reference_answer: Claude-generated answer grounded in CONTEXTS
                ground_truth_label: null
```

---

**Output — Excel file columns:**

| Column | Description |
|--------|-------------|
| `pubid` | PubMedQA article ID |
| `topic` | Member's domain |
| `member` | Which team member owns this session |
| `turn` | 1 / 2 / 3 |
| `question` | Question for this turn |
| `reference_answer` | Ground truth answer |
| `ground_truth_label` | yes / no / maybe (Turn 1 only) |
| `contexts` | PubMedQA abstract paragraphs (semicolon-separated) |

**50 sessions × 3 turns = 150 rows total in the Excel file.**

---

**Spot-check before use:**
Each member reviews their 10 sessions (30 rows) and confirms that Claude-generated reference answers are actually supported by the `contexts` text. Flag any that appear hallucinated and regenerate. Takes ~10 minutes per person.

**Verify:** All 150 rows present, no empty `reference_answer` cells, all Turn 1 rows have a valid `ground_truth_label`.

---

### P4 — Performance Script and Google Sheets Logging

**Goal:** A single script any team member can run against their assigned sessions. Results auto-append to a shared Google Sheet.

**Script inputs:**
- Path to their `dataset2_memberN.json`
- Backend base URL (pointing to hosted or local FastAPI server)
- Google Sheets credentials

**What the script does per session:**
1. For each turn, calls all 4 endpoints (S1–S4)
2. For S3/S4: uses the same `session_id` across turns within a session
3. After each session: deletes S3/S4 session to reset state before the next session
4. Computes all metrics locally (no LLM calls)
5. Appends one row per (session × turn × strategy) to the shared Google Sheet

**Metrics logged:**

| Column | Turns | Strategies |
|--------|-------|-----------|
| `session_id` | All | All |
| `pubid` | All | All |
| `topic` | All | All |
| `turn` | All | All |
| `strategy` | All | All |
| `question` | All | All |
| `answer` | All | All |
| `reference_answer` | All | All |
| `label_accuracy` | Turn 1 | All — yes/no/maybe keyword match |
| `bert_score_f1` | All | All — vs `reference_answer` |
| `hallucination_label` | All | All — ENTAILMENT / NEUTRAL / CONTRADICTION |
| `is_hallucination` | All | All — True if CONTRADICTION |
| `context_recall` | All | S2, S4 — cosine sim of retrieved chunks vs `contexts` |
| `coherence` | Turn 2, 3 | S3, S4 — cosine sim to previous turn answer |
| `latency_ms` | All | All — wall clock per API call |
| `prompt_tokens` | All | All — from API response |
| `completion_tokens` | All | All — from API response |

**Google Sheet structure:**
- One tab per member (`Member1`, `Member2`, etc.)
- One aggregated `Summary` tab (formula-driven, no manual work)

**Verify:** P4 does a dry run with 1 session, confirms rows appear in the correct sheet tab with no errors.

---

### P5 — Chatbot UI

**Goal:** A working frontend that lets users interact with all 4 strategies, used for both the demo and qualitative testing sessions.

**Requirements for evaluation:**
- Strategy selector (S1/S2/S3/S4) so testers can switch between systems
- Session ID is generated and maintained per conversation
- Displays retrieved chunks (for S2/S4) so medical testers can see what context was used
- No strategy labels visible to testers during qualitative sessions (shown as System A–D)

---

## Phase 2 — Integration Checklist

All of the following must pass before Phase 3 (parallel evaluation) begins.

- [ ] All 4 endpoints are live and return valid responses
- [ ] LangSmith traces appear for all 4 strategies with correct `strategy` tag
- [ ] Hosted ChromaDB is reachable from all 5 machines (test with a sample query)
- [ ] Vector DB collection count matches expected range (~10,000+ chunks)
- [ ] Dataset 2 Excel validated — all 150 rows present, no empty `reference_answer` cells, all Turn 1 rows have `ground_truth_label`, spot-check of Claude-generated answers done by each member
- [ ] Performance script dry run completes on 1 session, rows appear in Google Sheet
- [ ] Google Sheet is shared with edit access for all 5 members
- [ ] S3/S4 session deletion confirmed working (no stale sessions between eval runs)
- [ ] API rate limits understood — the script should have a short delay between calls to avoid 429s

---

## Phase 3 — Parallel Evaluation Session Division

Once Phase 2 passes, divide the 50 sessions across 5 members so all can run simultaneously.

| Member | Sessions | Dataset file |
|--------|----------|-------------|
| P1 | Sessions 1–10 (Cardiovascular & Respiratory) | `dataset2_member1.json` |
| P2 | Sessions 11–20 (Oncology & Hematology) | `dataset2_member2.json` |
| P3 | Sessions 21–30 (Neurology & Mental Health) | `dataset2_member3.json` |
| P4 | Sessions 31–40 (Infectious Disease & Immunology) | `dataset2_member4.json` |
| P5 | Sessions 41–50 (Metabolic, Endocrine & Pharmacology) | `dataset2_member5.json` |

Each member runs:
```
python eval/run_evaluation.py --input eval/data/dataset2_memberN.json
```

Results append to their tab in the shared Google Sheet in real time.

---

## Phase 4 — Analysis

### Quantitative

Once all 5 members have completed their sessions:
1. Open the `Summary` tab in Google Sheet — aggregated metrics per strategy are pre-computed
2. Compare across strategies on each metric:
   - Accuracy: S1 vs S2 vs S3 vs S4 on Turn 1 label match
   - BERTScore: answer quality across all turns
   - Hallucination rate: `count(is_hallucination) / total turns` per strategy
   - Context recall: S2 vs S4 — did adding memory hurt or help retrieval?
   - Coherence: S3 vs S4 — does RAG + memory improve topic continuity?
   - Latency p50/p95/p99: per strategy (from LangSmith dashboard)
   - Cost per query: from LangSmith + token counts

### Qualitative

**Testers:** Medical professionals (doctors, residents) and medical students  
**Method:** Each tester uses all 4 strategies (labeled System A–D) and asks 3–5 questions from their own expertise

**Feedback form dimensions:**

| Dimension | Scale |
|-----------|-------|
| Clinical accuracy | 1–5 |
| Explanation clarity | 1–5 |
| Hallucination observed | Yes / No + example |
| Follow-up coherence (S3/S4) | 1–5 |
| Preferred strategy overall | A / B / C / D |
| Open feedback | Text |

**Analysis:** Aggregate ratings per strategy, cross-reference hallucination incidents with quantitative hallucination rate, note professional vs. student preference differences.

---

## Error Attribution Framework

When an answer scores poorly, the metrics identify the root cause:

```
Wrong or low-scoring answer
├── S2 or S4 (RAG strategies)
│   ├── context_recall low  → Retrieval failure (wrong abstract fetched from large corpus)
│   └── context_recall high → Generation failure (correct context, LLM produced bad answer)
│
└── S1 or S3 (no RAG)
    └── Baseline generation quality — no retrieval involved
```

---

## File Structure

```
eval/
├── generate_dataset2.py        ← P3 writes this (calls Claude API, outputs Excel)
├── run_evaluation.py           ← P4 writes this (reads Excel, logs to Google Sheet)
└── data/
    └── dataset2.xlsx           ← shared with team, 150 rows, 5 domain tabs

backend/
└── seed_db.py                  ← P2 updates and runs this (--member 1..5)
```

---

## Dependencies to Add (requirements.txt)

```
bert-score
datasets
langsmith
gspread
oauth2client
```

`sentence-transformers` and `transformers` are already present.  
The NLI model (`cross-encoder/nli-deberta-v3-small`) downloads automatically on first use.
