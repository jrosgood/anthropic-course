import asyncio
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from contextlib import AsyncExitStack

PROJECT_DIR = Path(__file__).resolve().parent
MCP_SERVER = str(PROJECT_DIR / "mcp_server.py")

from mcp_client import MCPClient
from core.claude import Claude

from core.cli_chat import CliChat
from core.cli import CliApp

load_dotenv()

claude_model = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")

assert anthropic_api_key, (
    "Error: ANTHROPIC_API_KEY not set. Add it to the .env file at the repo root."
)


async def main():
    claude_service = Claude(model=claude_model)

    server_scripts = sys.argv[1:]
    clients = {}

    command, args = sys.executable, [MCP_SERVER]

    async with AsyncExitStack() as stack:
        doc_client = await stack.enter_async_context(
            MCPClient(command=command, args=args)
        )
        clients["doc_client"] = doc_client

        for i, server_script in enumerate(server_scripts):
            client_id = f"client_{i}_{server_script}"
            script_path = str(Path(server_script).resolve())
            client = await stack.enter_async_context(
                MCPClient(command=sys.executable, args=[script_path])
            )
            clients[client_id] = client

        chat = CliChat(
            doc_client=doc_client,
            clients=clients,
            claude_service=claude_service,
        )

        cli = CliApp(chat)
        await cli.initialize()
        await cli.run()


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
