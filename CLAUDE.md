# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server that retrieves YouTube video transcripts and metadata. The project is built using Python 3.10+ with `uv` as the package manager and uses the FastMCP framework.

## Core Architecture

### Main Components

- **`src/mcp_youtube_transcript/__init__.py`**: Core server implementation
  - `server()` function: Initializes the FastMCP server with optional proxy configuration
  - `AppContext`: Dataclass holding shared resources (HTTP client, YouTube Transcript API, yt-dlp)
  - `_app_lifespan()`: Context manager for resource lifecycle management
  - Two MCP tools: `get_transcript` and `get_video_info`

- **`src/mcp_youtube_transcript/cli.py`**: CLI entry point with Click framework
  - Exposes command-line options for response limits and proxy configuration
  - Entry point: `mcp-youtube-transcript` command

### Key Design Patterns

- **LRU Caching**: Both `_get_transcript()` and `_get_video_info()` use `@lru_cache` to avoid redundant API calls
- **Pagination**: Transcripts are split into chunks based on `response_limit` (default 50,000 characters) using cursor-based pagination
- **URL Parsing**: Handles both standard (`youtube.com/watch?v=`) and short (`youtu.be/`) YouTube URLs
- **Proxy Support**: Two proxy types supported:
  - Webshare proxy (username/password)
  - Generic HTTP/HTTPS proxy (URL-based)

## Development Commands

### Setup
```bash
# Install dependencies (requires uv)
uv sync --all-extras --dev
```

### Running Tests
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_server.py

# Run specific test
uv run pytest tests/test_mcp.py::test_list_tools -v
```

**Note**: Many integration tests in `test_mcp.py` skip on CI (`@pytest.mark.skipif(os.getenv("CI") == "true")`). They use `pytest-recording` for VCR cassettes.

### Code Quality
```bash
# Run all pre-commit hooks (ruff, mypy, pytest, formatting)
uv run pre-commit run -a

# Run ruff linting and formatting
uv run ruff check --fix .
uv run ruff format .

# Run mypy type checking
uv run mypy .
```

### Running the Server Locally
```bash
# Run with default settings
uv run mcp-youtube-transcript

# Run with custom response limit
uv run mcp-youtube-transcript --response-limit 15000

# Run with proxy
uv run mcp-youtube-transcript --http-proxy http://localhost:8080
```

### Version Bumping
```bash
# Uses bump-my-version (configured in pyproject.toml)
uv run bump-my-version bump patch  # 0.5.0 -> 0.5.1
uv run bump-my-version bump minor  # 0.5.0 -> 0.6.0
uv run bump-my-version bump major  # 0.5.0 -> 1.0.0
```

## Testing Strategy

### Test Files
- **`tests/test_server.py`**: Unit tests for proxy configuration and server initialization
- **`tests/test_mcp.py`**: Integration tests calling MCP tools via stdio client
  - Uses `pytest-recording` for HTTP request mocking
  - Most tests skip on CI to avoid YouTube API rate limits

### Test Fixtures
- `mcp_client_session`: Module-scoped MCP client with unlimited response size
- `mcp_client_session_with_response_limit`: Client with 3000-character limit for pagination testing

## Important Implementation Details

### Transcript Retrieval Flow
1. Parse video ID from URL (supports both `youtube.com` and `youtu.be`)
2. Fetch video title from YouTube HTML page (respects language preference)
3. Retrieve transcript using `YouTubeTranscriptApi`
4. If `response_limit` is set, paginate results using cursor (line index)

### Video Info Retrieval
- Uses `yt-dlp` to extract metadata (title, description, uploader)
- Returns `VideoInfo` Pydantic model

### Error Handling
- Invalid URLs raise `ValueError` with descriptive message
- Missing video IDs are caught during URL parsing
- YouTube API errors propagate to MCP error responses

## Code Style

- **Line length**: 120 characters (configured in `pyproject.toml`)
- **Type hints**: Required (`disallow_untyped_defs = true` in mypy config)
- **Python version**: 3.10+ (uses `|` union syntax, not `Optional[]`)
- **Formatting**: Enforced by ruff and pre-commit hooks
