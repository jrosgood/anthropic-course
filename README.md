# Anthropic Course Companion

A working set of Jupyter notebooks that mirror the modules of Anthropic's [**Building with the Claude API**](https://anthropic.skilljar.com/claude-with-the-anthropic-api) course. Each notebook contains the runnable code from the corresponding video module, so you can follow along with the course without pausing to type code from the screen.

Intended for technical *and* non-technical learners — if you can launch Jupyter Lab, you can run every cell.

> New to Python or Jupyter? Jump to [Newbie Quickstart](#newbie-quickstart) at the bottom.

## What's in this repo

Each notebook maps 1:1 to a course module:

| Course module | Notebook | Topics |
|---|---|---|
| 2. Accessing Claude with the API | [01_api_intro.ipynb](01_api_intro.ipynb) | Sending your first message; multi-turn chat; system prompts; temperature; streaming; structured output |
| 3. Prompt Evaluation | [02_api_prompt_evaluation.ipynb](02_api_prompt_evaluation.ipynb) | Generating test datasets with Claude; model-graded and code-graded evaluations; HTML reports |
| 4. Prompt Engineering | [03_api_prompt_engineering.ipynb](03_api_prompt_engineering.ipynb) | Clarity & specificity; few-shot examples; XML structure; iterative improvement; reusable `PromptEvaluator` class |
| 5. Tool Use | [04_api_tool_use.ipynb](04_api_tool_use.ipynb) | Defining tool schemas; multi-turn tool loops; multiple tools; web search tool |
| 6. RAG & Agentic Search | [05_api_rag_and_agentic_search.ipynb](05_api_rag_and_agentic_search.ipynb) | Chunking; local embeddings; vector + BM25 search; Reciprocal Rank Fusion; end-to-end RAG |
| 7–11. Features, MCP, Agents | — | _Not yet implemented_ |

Sample data, generated reports, and the source document used by the RAG notebook all live in [`artifacts/`](artifacts/).

## Prerequisites

- Python 3.13 (PyTorch does not yet ship 3.14 wheels)
- [Poetry](https://python-poetry.org/docs/#installation)
- An [Anthropic API key](https://console.anthropic.com/) — needed for any notebook that calls Claude (most of them). The embedding model used in Notebook 05 runs locally and does not need an API key.
- ~3 GB free disk space (embedding model weights cache to `~/.cache/huggingface/`)
- Optional: NVIDIA GPU with CUDA 12.x, or Apple Silicon (auto-detected at runtime)

## Setup

```bash
# Install dependencies
poetry install

# Create a .env file with your API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env
```

The notebooks load `.env` automatically via `python-dotenv`, so your API key never has to be hard-coded into a cell.

## How to use these notebooks

A guide for first-time users — especially if you're following along with the course videos.

- **One notebook per course module.** Open the notebook listed in the table above next to the module you're watching. Cells are ordered to match the video.
- **Read before you run.** Markdown cells explain *what* each code block does. Outputs from previous runs are checked into git, so you can preview the results before executing anything.
- **Run cells with Shift+Enter.** Cells must run top-to-bottom — earlier cells define variables and helper functions that later cells use.
- **If something breaks**, the fastest fix is **Kernel → Restart Kernel and Clear Outputs of All Cells**, then re-run from the top. This clears stale state without losing the saved code.
- **Where the data comes from.** Sample datasets, generated reports, and the source document used by the RAG notebook all live in [`artifacts/`](artifacts/). Notebooks read these files with relative paths, so launch Jupyter from the repo root.
- **API costs.** Most cells make one or two API calls each; running all five notebooks end-to-end on Sonnet 4.6 typically costs well under $1. The exact spend depends on the model you choose — see [Anthropic's pricing page](https://www.anthropic.com/pricing).
- **You can skip ahead.** Each notebook is self-contained — you can jump straight to Notebook 05 without running 01–04 first. The only state shared across notebooks is the `.env` file and the contents of `artifacts/`.

## Notebook 05 — RAG & Hybrid Search

Notebook 05 builds a full retrieval-augmented generation pipeline from scratch:

- **Text chunking** — character-delimited, sentence-delimited, and section-delimited strategies
- **Local embeddings** — [`microsoft/harrier-oss-v1-0.6b`](https://huggingface.co/microsoft/harrier-oss-v1-0.6b) runs entirely on-device (no API key, no network calls after first download)
- **VectorIndex** — cosine and Euclidean similarity search backed by NumPy arrays
- **BM25Index** — classic lexical search with IDF computed via NumPy
- **Retriever** — wraps any combination of indexes and fuses their results using Reciprocal Rank Fusion (RRF)
- **End-to-end RAG** — retrieved context passed to Claude to answer questions grounded in the document

### Local embedding hardware notes

- Default `poetry install` ships **CPU PyTorch**. Embedding all chunks of the sample report takes ~5–15 s on CPU.
- **NVIDIA GPU upgrade (optional):**
  ```bash
  poetry run pip install --upgrade torch --index-url https://download.pytorch.org/whl/cu124
  ```
- **Apple Silicon (M-series):** MPS is auto-detected — no extra steps.
- **First run downloads ~1.5 GB** for the model. To pre-download outside the notebook:
  ```bash
  poetry run huggingface-cli download microsoft/harrier-oss-v1-0.6b
  ```
- To relocate the cache (e.g. small C: drive on Windows): set `HF_HOME=D:\hf-cache` before launching Jupyter.

## Running the Notebooks

```bash
poetry run jupyter lab
```

Your browser will open Jupyter Lab automatically. Pick a notebook from the file list on the left and start with the topmost cell.

---

## Newbie Quickstart

Step-by-step for a clean machine (Windows / macOS / Linux). If a step looks unfamiliar, copy-paste the command verbatim into your terminal.

1. **Install Python 3.13** (PyTorch does not yet ship 3.14 wheels):
   - Windows: download the [python.org 3.13 installer](https://www.python.org/downloads/) — during install, check **Add Python to PATH**.
   - macOS: `brew install python@3.13` (install [Homebrew](https://brew.sh) first if you don't have it).
   - Fedora/RHEL: `sudo dnf install python3.13`.
2. **Install Poetry** (the dependency manager this project uses):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
   On Windows PowerShell: `(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -`
3. **Clone this repo and enter its directory:**
   ```bash
   git clone <repo-url>
   cd anthropic-course
   ```
4. **Install all dependencies** (2–5 minutes — downloads PyTorch, ~200 MB):
   ```bash
   poetry install
   ```
5. **Add your Anthropic API key** (get one at [console.anthropic.com](https://console.anthropic.com/)):
   ```bash
   echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
   ```
6. **Launch Jupyter Lab:**
   ```bash
   poetry run jupyter lab
   ```
   Your browser will open automatically.
7. **Open a notebook** — start with [01_api_intro.ipynb](01_api_intro.ipynb), then work your way down. See [How to use these notebooks](#how-to-use-these-notebooks) for tips on running cells and recovering from errors.
8. **For Notebook 05 (RAG):** the first time you run the embedding cell, it will appear paused for 1–3 minutes while it downloads the ~1.5 GB embedding model. This only happens once — subsequent runs are instant.

### Common issues

- **Out of memory** → in Jupyter Lab, click **Kernel → Restart Kernel**.
- **Notebook 05 is slow on CPU** → use the NVIDIA GPU upgrade command in the [Notebook 05 hardware notes](#local-embedding-hardware-notes) section above.
- **`HF_TOKEN` errors** → harrier-oss is a public model; you do not need a Hugging Face account.
- **`poetry: command not found`** → restart your terminal after installing Poetry, or follow the [Poetry PATH setup docs](https://python-poetry.org/docs/#installation).
- **Wrong Python version** → run `python3 --version` to confirm 3.13.x. If a different Python is found, run `poetry env use python3.13` from the repo directory before `poetry install`.
