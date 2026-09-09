# Inzora — Project Roadmap & Planning Document

*Turn raw data into actionable insights*

---

## 1. Why This Project (Portfolio Positioning)

| Existing project | What it proves |
|---|---|
| MedicareDB | Relational design, SQL depth, stored procedures |
| PlayRift | Full-stack integration, external API usage |
| Sideflicks | CRUD, auth, Docker, REST |

**Gap:** none of these show *analytical judgment* — deciding what's worth knowing about data, not just storing and serving it.

**Inzora's job:** prove you can take an unfamiliar dataset and independently figure out what matters in it. The insight engine is the resume story. Everything else is delivery mechanism.

**Rule of thumb for the whole project:** if a feature makes the analytics smarter, it's high priority. If it makes the app prettier or more "enterprise," it's a stretch goal.

---

## 2. Finalized MVP

### Must ship (MVP)
1. **CSV upload + validation** — file type check, size limit, malformed-CSV handling with useful error messages.
2. **Dataset profiling** — rows, columns, dtypes, missing values, duplicates, unique counts.
3. **Data quality score** — transparent, formula-based (e.g., weighted penalty for missing %, duplicate %, type inconsistency). Document the formula from day one.
4. **Descriptive statistics** — numeric (mean/median/min/max/std/distribution) and categorical (unique/mode/frequency) summaries.
5. **Chart recommendation logic** — rule-based mapping from column-type pairs to chart type (this is a lookup table, not a research problem — don't over-invest here).
6. **Insight engine (the core deliverable)**, covering:
   - Missing-data flags
   - Outlier detection (IQR and/or Z-score — pick one, document why, mention the other as a limitation)
   - Correlation detection (with an explicit "correlation ≠ causation" caveat in the UI copy)
   - Trend detection (% change over time; linear regression only if a dataset has a real date axis)
   - Priority tiers: High / Medium / Informational, with a documented, rule-based scoring method

### Explicitly deferred out of MVP
- **PostgreSQL** — use local file/JSON storage for MVP. Revisit as a Phase 6 enhancement if you want persistent dataset history.
- Docker — added once the analytics core is stable, not while iterating on it.
- Full test suite — targeted tests on analytics functions from the start; broader coverage later.
- Category-performance comparisons, dataset comparison, advanced ML — stretch goals only.

---

## 3. Core Technology Decisions

| Layer | Choice | Reasoning |
|---|---|---|
| Analytics | Python, Pandas, NumPy, SciPy (for stats tests) | Core deliverable — invest most learning time here |
| Backend | FastAPI | Lightweight, async, plays well with Pandas, fast to build endpoints |
| Frontend | React + JavaScript (TypeScript optional stretch) | You already know it — don't relearn tooling mid-project, spend saved time on analytics |
| Visualization | Plotly (via Plotly.js or React wrapper) | Interactive, good default styling, minimal custom chart code |
| Storage (MVP) | Local filesystem / JSON | Zero schema overhead, ships faster |
| Storage (later) | PostgreSQL | Add only if you want persistent history — Phase 6, optional |
| Dev tooling | Git, GitHub, Pytest, Postman/Bruno | Standard, don't overbuild for a solo repo |

---

## 4. Four-Month Roadmap

**Phase 1 — Analytics Foundation (Weeks 1–3)**
- Set up repo, Python project structure, virtual env
- Build dataset profiling functions (rows, cols, dtypes, missing, duplicates) as pure Python/Pandas functions — no API yet
- Write unit tests for profiling functions as you go
- Deliverable: a script that takes a CSV path and prints a profile report to console

**Phase 2 — Data Quality & Descriptive Stats (Weeks 4–6)**
- Implement data quality scoring formula (document it in a markdown file as you build it)
- Implement descriptive stats for numeric + categorical columns
- Test against 3–4 varied sample CSVs (clean, messy, mixed types, large)
- Deliverable: quality score + stats output, still CLI/script-based

**Phase 3 — Insight Engine (Weeks 7–11)** ← the heart of the project, budget the most time here
- Outlier detection (IQR or Z-score)
- Correlation detection + causation-caveat logic
- Trend detection (% change, moving average)
- Priority scoring (High/Medium/Informational) — write out your rules explicitly before coding them
- Deliverable: given a CSV, output a ranked list of findings in plain English

**Phase 4 — Backend API (Weeks 12–13)**
- Wrap Phases 1–3 in FastAPI endpoints (upload, profile, quality, insights)
- Input validation, error handling, basic Postman/Bruno test collection
- Deliverable: working API, testable without a frontend

**Phase 5 — Frontend Dashboard (Weeks 14–16)**
- Upload UI, dataset overview, chart rendering via Plotly, insight cards with priority tiers
- Deliverable: working end-to-end app

**Phase 6 — Polish, Testing, Deployment, Docs (Weeks 17–18)**
- Expand test coverage on analytics + API
- Dockerize (optional but recommended at this stage — it's cheap once things are stable)
- Deploy (see Section 6)
- Write README, architecture doc, analytics methodology doc
- **Only now** consider stretch goals if time remains: Postgres persistence, dataset comparison, automated reports

Total: ~18 weeks (~4.5 months), matches your target with buffer.

---

## 5. Architecture

**MVP flow:**
```
CSV Upload → FastAPI → Analytics Engine (Pandas/NumPy) → Insight Generator → JSON response → React Dashboard
```

**Later (if Postgres added):**
```
React Frontend
      │
      ▼
   FastAPI
      │
 ┌────┴────┐
 ▼         ▼
Analytics  PostgreSQL (dataset metadata, history)
Engine
 │
 ▼
Insight Generator
```

Keep the analytics engine as a **standalone Python package** (importable, testable independently of FastAPI). This is a good architecture talking point for interviews: "the analytics core has no framework dependency, so it's unit-testable in isolation and could be swapped into a CLI tool or notebook."

---

## 6. GitHub & Workflow Plan (right-sized for solo dev)

**Repo structure:**
```
Inzora/
├── analytics/          # pure Python analytics engine (no FastAPI deps)
│   ├── profiling.py
│   ├── quality.py
│   ├── stats.py
│   ├── insights.py
│   └── tests/
├── backend/             # FastAPI app
│   ├── main.py
│   ├── routers/
│   └── tests/
├── frontend/             # React app
├── docs/
│   ├── architecture.md
│   └── analytics-methodology.md
├── sample_data/          # example CSVs for demo/testing
├── README.md
└── docker-compose.yml    # added in Phase 6
```

**Branching:** `main` (always working) + short-lived feature branches (`feature/outlier-detection`). No need for `develop`/gitflow — that's overkill for one contributor.

**Commits:** Conventional commits (`feat:`, `fix:`, `test:`, `docs:`) — clean history, and it's a talking point for "professional practices."

**Issues:** Use GitHub Issues as your task list per phase (one issue per feature above), close via PR even if you're merging your own branches — gives you a visible project history for your portfolio/GitHub profile.

**README (build progressively, don't leave to the end):** overview → problem statement → features → architecture diagram → screenshots → tech stack → install/usage → sample dataset walkthrough → future improvements.

---

## 7. Progress Tracker

**COMPLETED**
- Project concept & scope
- MVP finalized
- Architecture planned
- Roadmap defined

**IN PROGRESS**
- (nothing yet — planning complete, implementation not started)

**NEXT**
- Phase 1: repo setup + dataset profiling functions