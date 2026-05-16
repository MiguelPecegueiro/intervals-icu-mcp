"""Middleware for Intervals.icu MCP server."""
from collections.abc import Callable
from pathlib import Path
from typing import Any
from fastmcp.exceptions import ToolError
from fastmcp.server.middleware import Middleware, MiddlewareContext
from .auth import ICUConfig, validate_credentials
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"

class ConfigMiddleware(Middleware):
    def __init__(self):
        load_dotenv(dotenv_path=ENV_PATH, override=True)
        self._config = ICUConfig()

    async def on_call_tool(self, context: MiddlewareContext, call_next: Callable[..., Any]):
        if not validate_credentials(self._config):
            raise ToolError(
                "Intervals.icu credentials not configured. "
                "Please run 'icu-mcp-auth' to set up authentication."
            )
        if context.fastmcp_context:
            await context.fastmcp_context.set_state("config", self._config.model_dump())
        return await call_next(context)