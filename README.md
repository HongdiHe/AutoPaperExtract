# AutoPaperExtract

Autoresearch-style autonomous literature extraction and review writing system for coordination-driven self-assembly papers.

## Project Structure

```
AutoPaperExtract/
├── program.md              # Agent instructions for PDF extraction
├── review_program.md       # Agent instructions for review writing (autoresearch-style)
├── start.sh                # Launcher: extract | enrich | review
├── REFACTOR_PLAN.md        # Future refactoring roadmap (Phase 1-3)
│
├── scripts/                # Python tools
│   ├── schema.py           # Shared schema, terminology table, filters
│   ├── normalize_md.py     # Section normalization + review paper tagging
│   ├── audit.py            # Fact audit (ligand terms, data anomalies)
│   ├── validate.py         # Template compliance check
│   ├── fix_format.py       # Legacy format fixer
│   ├── rebuild_csv.py      # Rebuild CSV from MD files (UTF-8 BOM)
│   └── discover.py         # Literature discovery (citation graph, keyword search, frontier tracking)
│
├── output/
│   ├── papers/             # 84 paper MD files (one per paper)
│   ├── papers_database.csv # Master CSV database
│   ├── review/             # Review drafts, logs, candidates
│   └── reports/            # Audit reports, discovery reports
│
├── 三联吡啶/               # PDF files (terpyridine papers)
├── 单吡啶/                 # PDF files (pyridine papers)
└── 联吡啶/                 # PDF files (bipyridine papers)
```

## Quick Start

```bash
# Extract new PDFs
bash start.sh

# Enrich incomplete MD files
bash start.sh enrich

# Write a review (autoresearch-style iterative loop)
bash start.sh review
```

## How It Works

Inspired by [Karpathy's autoresearch](https://github.com/karpathy/autoresearch):

### PDF Extraction
- Agent reads each PDF, extracts metadata + full content
- Writes structured MD files with: metadata, abstract, background, methods, results, conclusions
- Auto-validates with `audit.py` (terminology) and `validate.py` (template compliance)

### Review Writing (autoresearch-style loop)
```
LOOP:
  1. RESEARCH  — Read 3-5 paper MDs
  2. THINK     — Analyze connections and contrasts
  3. WRITE     — Write 300-500 words with citations
  4. VERIFY    — Check terms, data, anti-plagiarism
  5. SAVE      — Append to review_draft.md
  6. LOG       — Record to review_log.md
```

### Literature Discovery
```bash
python3 scripts/discover.py --mode citations   # Citation graph analysis
python3 scripts/discover.py --mode search      # Keyword search (OpenAlex)
python3 scripts/discover.py --mode frontier    # Frontier tracking (2023-2026)
```

## Key Features

- **Anti-plagiarism**: Review papers in corpus are tagged and excluded from writing sources
- **Terminology guard**: terpyridine / bipyridine / tris(bipyridine) confusion auto-detected
- **Concurrent lock**: Prevents double-running via `flock`
- **Post-processing pipeline**: normalize → validate → audit → auto-fix → rebuild CSV
- **UTF-8 BOM CSV**: Excel-compatible on Chinese Windows

## Stats

- 84 papers processed (JACS, Science, Nature, Nat Chem, Angew Chem, etc.)
- 2 review papers tagged and excluded from writing
- 153 frontier papers discovered (2023-2026)
