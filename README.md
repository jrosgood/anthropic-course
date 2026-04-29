# Anthropic Course

Jupyter notebooks exploring the Claude API — covering API basics, prompt evaluation, and prompt engineering.

## Prerequisites

- Python 3.14+
- [Poetry](https://python-poetry.org/docs/#installation)
- An [Anthropic API key](https://console.anthropic.com/)

## Setup

```bash
# Install dependencies
poetry install

# Create a .env file with your API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env
```

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

Generated artifacts (datasets, outputs) are saved to the [artifacts/](artifacts/) directory.
