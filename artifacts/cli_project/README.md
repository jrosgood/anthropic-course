# MCP Chat

MCP Chat is a command-line interface application that enables interactive chat capabilities with AI models through the Anthropic API.  It supports document retrieval, command-based prompts, and extensible tool integrations via the MCP (Model Control Protocol) architecture.

## Setup

This project is installed as an editable Poetry dependency of the parent repo.  Run `poetry install` from the repo root and the CLI's dependencies come along with it.  API key configuration lives in the parent repo's `.env` — see the [parent README](../../README.md#setup).

## Run

From the repo root:

```bash
poetry run python artifacts/cli_project/main.py
```

### Running MCP commands

The course instructions show bare `mcp dev mcp_server.py`.  The `mcp` CLI installs into the parent repo's Poetry venv (via the `mcp[cli]` extra on cli_project), so it isn't on your shell PATH directly.  Two ways to invoke it:

- From the cli_project folder, point Poetry at the parent project:
  ```bash
  poetry -P ../.. run mcp dev mcp_server.py
  ```
- Or from the repo root:
  ```bash
  poetry run mcp dev artifacts/cli_project/mcp_server.py
  ```

`poetry -P` (`--project`) tells Poetry which `pyproject.toml` to resolve against.  Without it, Poetry walks up from cwd, finds cli_project's own pyproject, and spins up an empty venv with whatever Python it can find — including the wrong Python version.  Same pattern applies to `mcp run`, `mcp install`, and any other `mcp` subcommand.

If you went with the standalone uv setup below, use `uv run` instead:

```bash
uv run mcp dev mcp_server.py
```

**First-run gotcha:** the MCP Inspector may show *"Connection Error — Check if your MCP server is running and proxy token is correct"* on the initial Connect attempt.  Click **Connect** again after a few seconds — it's a startup-timing race between the inspector UI and the server process, not a real configuration error.

**Running the client:** `mcp_client.py` is a plain Python script, not an `mcp` CLI subcommand, so use `python` directly:

```bash
# From cli_project
poetry -P ../.. run python mcp_client.py

# Or from the repo root
poetry run python artifacts/cli_project/mcp_client.py
```

The standalone uv equivalent is `uv run mcp_client.py` — note the absence of an `mcp` prefix.  Course materials occasionally show `mcp uv run mcp_client.py`, which fails with *"No such command 'uv'"*: `mcp` has no `uv` subcommand, and the client doesn't go through the `mcp` CLI at all.

### Standalone with uv (optional)

If you want to develop `cli_project` outside the Poetry world:

```bash
cd artifacts/cli_project
uv sync
uv run main.py
```

uv reads this project's own `pyproject.toml` and `uv.lock`.  The API key still loads from the repo-root `.env` via dotenv's directory-walking search.

## Optional environment overrides

| Variable | Default | Purpose |
|---|---|---|
| `CLAUDE_MODEL` | `claude-sonnet-4-6` | Override the model used by the CLI. |

Set in the repo-root `.env` if you want to change it.

## Usage

### Basic interaction

Type a message and press Enter to chat with the model.

### Document retrieval

Use `@` followed by a document ID to include document content in your query:

```
> Tell me about @deposition.md
```

### Commands

Use `/` to invoke commands defined by the MCP server.  Press Tab for completion:

```
> /summarize deposition.md
```

## Development

### Adding new documents

Edit `mcp_server.py` and add to the `docs` dictionary.

### Implementing MCP features

1. Complete the TODOs in `mcp_server.py`.
2. Implement the missing functionality in `mcp_client.py`.

### Linting and typing

None implemented.
