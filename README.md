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
| [1_api_intro.ipynb](1_api_intro.ipynb) | Claude API basics |
| [2_api_prompt_evaluation.ipynb](2_api_prompt_evaluation.ipynb) | Prompt evaluation techniques |
| [3_api_prompt_engineering.ipynb](3_api_prompt_engineering.ipynb) | Prompt engineering patterns |

Generated artifacts (datasets, outputs) are saved to the [artifacts/](artifacts/) directory.
