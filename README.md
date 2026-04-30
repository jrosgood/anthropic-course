# Anthropic Course

Jupyter notebooks exploring the Claude API — covering API basics, prompt evaluation, prompt engineering, tool use, and RAG.

> New to Python or Jupyter? Jump to [Newbie Quickstart](#newbie-quickstart) at the bottom of this README.

## Prerequisites

- Python 3.13 (PyTorch does not yet ship 3.14 wheels)
- [Poetry](https://python-poetry.org/docs/#installation)
- An [Anthropic API key](https://console.anthropic.com/)
- ~3 GB free disk space (embedding model weights cache to `~/.cache/huggingface/`)
- Optional: NVIDIA GPU with CUDA 12.x, or Apple Silicon (auto-detected at runtime)

## Setup

```bash
# Install dependencies
poetry install

# Create a .env file with your API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env
```

## Local Embeddings (Notebook 05)

Notebook 05 uses [`microsoft/harrier-oss-v1-0.6b`](https://huggingface.co/microsoft/harrier-oss-v1-0.6b) to generate embeddings locally — no API key, no network calls after first download.

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
# Launch Jupyter
poetry run jupyter lab
```

Then open any notebook in your browser:

| Notebook | Topic |
|---|---|
| [01_api_intro.ipynb](01_api_intro.ipynb) | Claude API basics |
| [02_api_prompt_evaluation.ipynb](02_api_prompt_evaluation.ipynb) | Prompt evaluation techniques |
| [03_api_prompt_engineering.ipynb](03_api_prompt_engineering.ipynb) | Prompt engineering patterns |
| [04_api_tool_use.ipynb](04_api_tool_use.ipynb) | Tool use |
| [05_api_rag_and_agentic_search.ipynb](05_api_rag_and_agentic_search.ipynb) | RAG & hybrid search: chunking strategies, local embeddings, VectorIndex (cosine/euclidean), BM25 lexical search, Reciprocal Rank Fusion, end-to-end RAG pipeline |

Generated artifacts (datasets, outputs) are saved to the [artifacts/](artifacts/) directory.

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
7. **Open a notebook** — start with [01_api_intro.ipynb](01_api_intro.ipynb), then work your way down.
8. **For Notebook 05 (RAG):** the first time you run the embedding cell, it will appear paused for 1–3 minutes while it downloads the ~1.5 GB embedding model. This only happens once — subsequent runs are instant.

### Common issues

- **Out of memory** → in Jupyter Lab, click **Kernel → Restart Kernel**.
- **Notebook 05 is slow on CPU** → use the NVIDIA GPU upgrade command in the [Local Embeddings](#local-embeddings-notebook-05) section above.
- **`HF_TOKEN` errors** → harrier-oss is a public model; you do not need a Hugging Face account.
- **`poetry: command not found`** → restart your terminal after installing Poetry, or follow the [Poetry PATH setup docs](https://python-poetry.org/docs/#installation).
- **Wrong Python version** → run `python3 --version` to confirm 3.13.x. If a different Python is found, run `poetry env use python3.13` from the repo directory before `poetry install`.
