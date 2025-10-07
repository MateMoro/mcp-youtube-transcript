#  cli.py
#
#  Copyright (c) 2025 Junpei Kawamoto
#
#  This software is released under the MIT License.
#
#  http://opensource.org/licenses/mit-license.php
import logging
import os

import click

from mcp_youtube_transcript import server


@click.command()
@click.option(
    "--response-limit",
    type=int,
    help="Maximum number of characters each response contains. Set a negative value to disable pagination.",
    default=50000,
)
@click.option(
    "--webshare-proxy-username",
    metavar="NAME",
    envvar="WEBSHARE_PROXY_USERNAME",
    help="Webshare proxy service username.",
)
@click.option(
    "--webshare-proxy-password",
    metavar="PASSWORD",
    envvar="WEBSHARE_PROXY_PASSWORD",
    help="Webshare proxy service password.",
)
@click.option("--http-proxy", metavar="URL", envvar="HTTP_PROXY", help="HTTP proxy server URL.")
@click.option("--https-proxy", metavar="URL", envvar="HTTPS_PROXY", help="HTTPS proxy server URL.")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "http", "sse"], case_sensitive=False),
    default="stdio",
    help="Transport protocol to use: stdio (local), http (recommended for remote), or sse (legacy).",
)
@click.option(
    "--host",
    default="127.0.0.1",
    help="Host to bind the server (use 0.0.0.0 for Railway/cloud deployments).",
)
@click.option(
    "--port",
    type=int,
    envvar="PORT",
    default=8000,
    help="Port to bind the server (automatically uses $PORT env var if set).",
)
@click.version_option()
def main(
    response_limit: int | None,
    webshare_proxy_username: str | None,
    webshare_proxy_password: str | None,
    http_proxy: str | None,
    https_proxy: str | None,
    transport: str,
    host: str,
    port: int,
) -> None:
    """YouTube Transcript MCP server."""

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    mcp_server = server(response_limit, webshare_proxy_username, webshare_proxy_password, http_proxy, https_proxy)

    if transport == "stdio":
        logger.info("starting Youtube Transcript MCP server (stdio transport)")
        mcp_server.run()
    else:
        logger.info(f"starting Youtube Transcript MCP server ({transport} transport on {host}:{port})")
        # Try different parameter formats to support various mcp SDK versions
        try:
            # Try with host/port parameters (newer FastMCP)
            mcp_server.run(transport=transport, host=host, port=port)
        except TypeError:
            try:
                # Try with address parameter (some versions)
                mcp_server.run(transport=transport, address=f"{host}:{port}")
            except TypeError:
                # Fallback: just transport
                logger.warning(f"MCP SDK doesn't support host/port parameters, using defaults")
                mcp_server.run(transport=transport)

    logger.info("closed Youtube Transcript MCP server")
