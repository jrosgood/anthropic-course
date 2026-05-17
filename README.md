# Anthropic Course Companion

> **Unofficial.**  This is a community-built companion to Anthropic's course — not affiliated with, endorsed by, or sponsored by Anthropic.  Just one person working through their course and publishing the code along the way.

Working notebooks that pair 1:1 with the modules of Anthropic's [**Building with the Claude API**](https://anthropic.skilljar.com/claude-with-the-anthropic-api) course.  Open the notebook for the module you're watching and run the cells alongside the video, instead of pausing every thirty seconds to retype code from the screen.

Intended for technical *and* non-technical learners — if you can launch Jupyter Lab, you can run every cell.  If you aren't the kind of person that was installing Red Hat Linux 9 on your home computer in high school (yes, I'm a nerd), jump straight to the [Newbie Quickstart](#newbie-quickstart).

## What's in this repo

Each notebook maps 1:1 to a course module:

| Course module | Notebook | Topics |
|---|---|---|
| 2. Accessing Claude with the API | [01_api_intro.ipynb](01_api_intro.ipynb) | Sending your first message; multi-turn chat; system prompts; temperature; streaming; structured output |
| 3. Prompt Evaluation | [02_api_prompt_evaluation.ipynb](02_api_prompt_evaluation.ipynb) | Generating test datasets with Claude; model-graded and code-graded evaluations; HTML reports |
| 4. Prompt Engineering | [03_api_prompt_engineering.ipynb](03_api_prompt_engineering.ipynb) | Clarity & specificity; few-shot examples; XML structure; iterative improvement; reusable `PromptEvaluator` class |
| 5. Tool Use | [04_api_tool_use.ipynb](04_api_tool_use.ipynb) | Defining tool schemas; multi-turn tool loops; multiple tools; web search tool |
| 6. RAG & Agentic Search | [05_api_rag_and_agentic_search.ipynb](05_api_rag_and_agentic_search.ipynb) | Chunking; local embeddings; vector + BM25 search; Reciprocal Rank Fusion; end-to-end RAG |
| 7. API Features of Claude | [06_api_features_of_claude.ipynb](06_api_features_of_claude.ipynb) | Extended thinking; image input; PDF input; document citations; prompt caching with `cache_control`; Files API and the code execution tool |
| 8. Model Context Protocol | [07_model_context_protocol.ipynb](07_model_context_protocol.ipynb) + [artifacts/cli_project/](artifacts/cli_project/) | FastMCP server with tools, resources, prompts; async stdio MCP client; CLI with `/`-commands and `@`-mentions; testing via `mcp dev` Inspector |
| 9. Anthropic Apps — Claude Code and Computer Use | — | _Covered by Anthropic's own docs — see § below_ |
| 10. Agents and Workflows | [09_agents_and_workflows.ipynb](09_agents_and_workflows.ipynb) | Evaluator-Optimizer loop; Parallelization with `ThreadPoolExecutor`; Chaining with inter-step validation; Routing with classifier + specialist dispatch |

Sample data, generated reports, and the source document used by the RAG notebook all live in [`artifacts/`](artifacts/).

## Prerequisites

- Python 3.13 (PyTorch does not yet ship 3.14 wheels)
- [Poetry](https://python-poetry.org/docs/#installation)
- An [Anthropic API key](https://console.anthropic.com/) — needed for any notebook that calls Claude (most of them).  The embedding model used in Notebook 05 runs locally and does not need an API key.
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

- **One notebook per course module.**  Open the notebook listed in the table above next to the module you're watching.  Cells are ordered to match the video.
- **Read before you run.**  Markdown cells explain what each code block does.  Outputs from previous runs are checked into git, so you can preview the results before executing anything.
- **Run cells with Shift+Enter.**  Cells must run top-to-bottom — earlier cells define variables and helper functions that later cells use.
- **If something breaks**, the fastest fix is **Kernel → Restart Kernel and Clear Outputs of All Cells**, then re-run from the top.  This clears stale state without losing the saved code.
- **Where the data comes from.**  Sample datasets, generated reports, and the source document used by the RAG notebook all live in [`artifacts/`](artifacts/).  Notebooks read these files with relative paths, so launch Jupyter from the repo root.
- **API costs.**  Most cells make one or two API calls each; running all seven API-calling notebooks (01–06 plus 09 — notebook 07 is markdown-only) end-to-end on Sonnet 4.6 typically costs ~$1–2.  The exact spend depends on the model you choose — see [Anthropic's pricing page](https://www.anthropic.com/pricing).
- **You can skip ahead.**  Each notebook is self-contained — you can jump straight to Notebook 05 without running 01–04 first.  The only state shared across notebooks is the `.env` file and the contents of `artifacts/`.

## Notebook 05 — RAG & Hybrid Search

Notebook 05 builds a full retrieval-augmented generation pipeline from scratch.  The course recommends VoyageAI — an external embedding service — for this section.  I didn't like the idea of standing up a second paid account just to embed a few thousand chunks for a course exercise, so the notebook installs [`microsoft/harrier-oss-v1-0.6b`](https://huggingface.co/microsoft/harrier-oss-v1-0.6b) and runs the embeddings locally instead.  The model is small but performant, and more than enough for this course.

What you get:

- **Text chunking** — character-delimited, sentence-delimited, and section-delimited strategies
- **Local embeddings** — `harrier-oss-v1-0.6b` runs entirely on-device (no API key, no network calls after the first download).  Uses CUDA if it's available, Apple Silicon MPS if you're on an M-series Mac, CPU otherwise.
- **VectorIndex** — cosine and Euclidean similarity search backed by NumPy arrays
- **BM25Index** — classic lexical search with IDF computed via NumPy
- **Retriever** — wraps any combination of indexes and fuses their results using *Reciprocal Rank Fusion* (RRF)
- **End-to-end RAG** — retrieved context passed to Claude to answer questions grounded in the document

In short: the whole RAG pipeline runs on your laptop with zero external dependencies beyond the Anthropic API key.

### Local embedding hardware notes

- Default `poetry install` ships **CPU PyTorch**.  Embedding all chunks of the sample report takes ~5–15 s on CPU — fine for this course.
- **NVIDIA GPU upgrade (optional):**
  ```bash
  poetry run pip install --upgrade torch --index-url https://download.pytorch.org/whl/cu124
  ```
- **Apple Silicon (M-series):** MPS is auto-detected — no extra steps.
- **First run downloads ~1.5 GB** for the model.  To pre-download outside the notebook:
  ```bash
  poetry run huggingface-cli download microsoft/harrier-oss-v1-0.6b
  ```
- To relocate the cache (e.g. small C: drive on Windows): set `HF_HOME=D:\hf-cache` before launching Jupyter.

## Notebook 07 — Model Context Protocol

The MCP module is the structural outlier in this repo.  Every other notebook holds runnable Python; this one is markdown-only.  The implementation — a FastMCP server, an async MCP client, and a CLI that wires them together — lives in [`artifacts/cli_project/`](artifacts/cli_project/) as a real installable Python package, and the notebook is just a guided tour of that code.

Why split it out?  MCP is a multi-process protocol — the client launches the server as a subprocess and talks to it over standard I/O (stdio).  Hosting both sides in a single Jupyter kernel makes the lifecycle awkward; the server has no clean shutdown when a cell errors.  Treating cli_project as a real app side-steps the problem and lets you actually use it.

What's in cli_project:

- **FastMCP server** (`mcp_server.py`) — two tools, two resources, one prompt over a small in-memory document store.  Runs over stdio for Inspector and client compatibility.
- **Async MCP client** (`mcp_client.py`) — `MCPClient` wraps the SDK's `ClientSession` with an `AsyncExitStack`-based lifecycle and an async context manager.
- **Interactive CLI** (`core/cli.py`, `core/cli_chat.py`) — `prompt-toolkit`-driven REPL with tab completion for `/`-commands (MCP prompts) and `@`-mentions (MCP resources for document IDs).

In short: the CLI is the artifact, the notebook is the narration.  See [`artifacts/cli_project/README.md`](artifacts/cli_project/README.md) for operational details — running the CLI, adding documents, launching the MCP Inspector with the `poetry -P ../..` invocation.

## Module 9 — Anthropic Apps (Claude Code and Computer Use)

This module covers Claude Code (Anthropic's coding CLI) and the computer use API.  Neither lives in this repo, on purpose.

Claude Code is a standalone CLI you install and run against a real repository — there's nothing meaningful to wrap in a Jupyter cell, and the install + usage walkthrough is already covered well by Anthropic's own documentation.

Computer use *is* programmable through the API, but exercising it safely needs a sandboxed VM or container that can take screenshots and inject mouse/keyboard events.  Setting that up for a learning notebook is more friction than the demo is worth — Anthropic's `computer-use-demo` reference image in their `anthropic-quickstarts` GitHub repo is the right place to start if you want to play with it.

For both, follow the course module through Anthropic's documentation directly.

## Notebook 09 — Agents and Workflows

The agents-and-workflows module is the only coding module that doesn't ship runnable code.  Earlier coding modules all walked through code you could execute; this one walks through the patterns conceptually and stops there.  Notebook 09 supplies the code the course didn't — runnable, cell-by-cell examples tailored to the course's subsections so you can step through each pattern while you watch the videos.

Course subsections implemented with runnable code:

- **Parallelization workflows** — split one complex task into specialized sub-tasks that run concurrently via `ThreadPoolExecutor`, then aggregate the slices into a single decision.  The notebook also runs the sequential equivalent so the wall-clock speedup is something you measure, not something you take on faith.
- **Chaining workflows** — feed each step's output into the next as a focused, validated handoff (extract → enrich → compose).  A real JSON-schema check sits between steps 1 and 2, so a regression in step 1 stops the chain rather than poisoning steps 2 and 3.
- **Routing workflows** — a cheap classifier dispatches to one of N specialist prompts, with an explicit `unknown` fallback for out-of-scope requests.

Plus one bonus pattern Anthropic's [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) article covers alongside the three above:

- **Evaluator-Optimizer** — an optimizer drafts a candidate, an evaluator grades it against a fixed rubric and returns actionable feedback, and the loop runs until the evaluator accepts or a max-iteration cap kicks in.

The course's *Agents and tools*, *Environment inspection*, *Workflows vs agents*, and quiz subsections aren't reproduced as code — they're conceptual or evaluative, and runnable examples wouldn't add anything.

Each pattern's section closes with a *Things to try* checklist — small variations (model swaps, temperature changes, deliberately-broken prompts) that surface *why* the pattern is shaped the way it is.  The point isn't just to copy the pattern; it's to feel where it breaks.

## Running the Notebooks

```bash
poetry run jupyter lab
```

Your browser will open Jupyter Lab automatically.  Pick a notebook from the file list on the left and start with the topmost cell.

## Running the Notebooks in VSCode

If you'd rather work in VSCode than browser Jupyter:

1. Open the repo folder in VSCode.  The committed `.vscode/settings.json` already points Python and Pylance at the in-project `.venv`.
2. Install the **Python** and **Jupyter** extensions from the marketplace if you don't have them.
3. **Register a Jupyter kernel** that points at the venv's Python.  One-time setup:
   ```bash
   poetry run python -m ipykernel install --user --name=anthropic-course --display-name="Python (anthropic-course)"
   ```
   This is needed because the stock kernels Jupyter ships with use a bare `python` PATH lookup that VSCode's kernel launcher doesn't resolve cleanly — notebooks otherwise show no selectable kernel.
4. **Reload the VSCode window** (Cmd/Ctrl+Shift+P → **Developer: Reload Window**) so the Jupyter extension re-scans kernelspecs.
5. Open a notebook → click the kernel picker in the top-right → **Select Another Kernel...** → **Jupyter Kernel...** → **Python (anthropic-course)**.

Run cells with Shift+Enter as usual.  See [How to use these notebooks](#how-to-use-these-notebooks) for the rest of the workflow.

## License and attribution

Joel's original work in this repo — notebooks 01–06 and 09, [`artifacts/cli_project/`](artifacts/cli_project/), and the various test outputs and helper scripts — is licensed under the [MIT license](LICENSE).

A handful of input data files in [`artifacts/`](artifacts/) (a PDF, satellite images, a CSV dataset) originated from Anthropic's course exercises and are kept here for convenience.  Those files are not licensed by me; see [`artifacts/README.md`](artifacts/README.md) for the explicit list.  The full Anthropic course materials are not redistributed — get those from [Anthropic's Skilljar course](https://anthropic.skilljar.com/claude-with-the-anthropic-api) directly.

---

## Newbie Quickstart

Step-by-step for a clean machine (Windows / macOS / Linux).  If a step looks unfamiliar, copy-paste the command verbatim into your terminal — that's exactly what it's there for.

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
7. **Open a notebook** — start with [01_api_intro.ipynb](01_api_intro.ipynb), then work your way down.  See [How to use these notebooks](#how-to-use-these-notebooks) for tips on running cells and recovering from errors.
8. **For Notebook 05 (RAG):** the first time you run the embedding cell, it will appear paused for 1–3 minutes while it downloads the ~1.5 GB embedding model.  This only happens once — subsequent runs are instant.
9. **Prefer VSCode over browser Jupyter?**  See [Running the Notebooks in VSCode](#running-the-notebooks-in-vscode) — one extra step (registering a kernelspec) and you're set.

### Common issues

- **Out of memory** → in Jupyter Lab, click **Kernel → Restart Kernel**.
- **Notebook 05 is slow on CPU** → use the NVIDIA GPU upgrade command in the [Notebook 05 hardware notes](#local-embedding-hardware-notes) section above.
- **`HF_TOKEN` errors** → harrier-oss is a public model; you do not need a Hugging Face account.
- **`poetry: command not found`** → restart your terminal after installing Poetry, or follow the [Poetry PATH setup docs](https://python-poetry.org/docs/#installation).
- **Wrong Python version** → run `python3 --version` to confirm 3.13.x.  If a different Python is found, run `poetry env use python3.13` from the repo directory before `poetry install`.
- **VSCode: no kernel available in a notebook** → see [Running the Notebooks in VSCode](#running-the-notebooks-in-vscode) — you need the `python -m ipykernel install` step once.  The stock kernels in the venv use a bare `python` argv that VSCode's launcher doesn't resolve.
