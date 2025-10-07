# YouTube Transcript MCP Server
[![Python Application](https://github.com/jkawamoto/mcp-youtube-transcript/actions/workflows/python-app.yaml/badge.svg)](https://github.com/jkawamoto/mcp-youtube-transcript/actions/workflows/python-app.yaml)
[![GitHub License](https://img.shields.io/github/license/jkawamoto/mcp-youtube-transcript)](https://github.com/jkawamoto/mcp-youtube-transcript/blob/main/LICENSE)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![smithery badge](https://smithery.ai/badge/@jkawamoto/mcp-youtube-transcript)](https://smithery.ai/server/@jkawamoto/mcp-youtube-transcript)
[![Dockerhub](https://img.shields.io/badge/Docker-mcp%2Fyoutube--transcript-blue.svg)](https://hub.docker.com/mcp/server/youtube_transcript)

This MCP server retrieves transcripts for given YouTube video URLs.

<a href="https://glama.ai/mcp/servers/of3kwtmlqp"><img width="380" height="200" src="https://glama.ai/mcp/servers/of3kwtmlqp/badge" alt="YouTube Transcript Server MCP server" /></a>

## Tools
This MCP server provides the following tools:

### `get_transcript`
Fetches the transcript of a specified YouTube video.

#### Parameters
- **url** *(string)*: The full URL of the YouTube video. This field is required.
- **lang** *(string, optional)*: The desired language for the transcript. Defaults to `en` if not specified.
- **next_cursor** *(string, optional)*: Cursor to retrieve the next page of the transcript.

### `get_video_info`
Fetches the metadata of a specified YouTube video.

#### Parameters
- **url** *(string)*: The full URL of the YouTube video. This field is required.

## Installation
> [!NOTE]
> You'll need [`uv`](https://docs.astral.sh/uv) installed on your system to use `uvx` command.

### For codename goose
Please refer to this tutorial for detailed installation instructions:
[YouTube Transcript Extension](https://block.github.io/goose/docs/mcp/youtube-transcript-mcp).

### For Claude Desktop
To configure this server for Claude Desktop, edit the `claude_desktop_config.json` file with the following entry under
`mcpServers`:

```json
{
  "mcpServers": {
    "youtube-transcript": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/jkawamoto/mcp-youtube-transcript",
        "mcp-youtube-transcript"
      ]
    }
  }
}
```
After editing, restart the application.
For more information,
see: [For Claude Desktop Users - Model Context Protocol](https://modelcontextprotocol.io/quickstart/user).

### For LM Studio
To configure this server for LM Studio, click the button below.

[![Add MCP Server youtube-transcript to LM Studio](https://files.lmstudio.ai/deeplink/mcp-install-light.svg)](https://lmstudio.ai/install-mcp?name=youtube-transcript&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyItLWZyb20iLCJnaXQraHR0cHM6Ly9naXRodWIuY29tL2prYXdhbW90by9tY3AteW91dHViZS10cmFuc2NyaXB0IiwibWNwLXlvdXR1YmUtdHJhbnNjcmlwdCJdfQ%3D%3D)


### Installing via Smithery
> [!NOTE]
> When using this method, you will be utilizing servers hosted by Smithery.
> Requests and responses will be routed through their servers.
> Please refer to the [Smithery Privacy Notice](https://smithery.ai/privacy) for information
> about their data handling practices.

The [Smithery CLI](https://github.com/smithery-ai/cli) enables the installation of MCP servers on various clients.

For instance, to install this server for Claude Desktop, execute the following command:

```bash
npx -y @smithery/cli install @jkawamoto/mcp-youtube-transcript --client claude
```

To view the list of clients supported by the Smithery CLI, use this command:

```bash
npx -y @smithery/cli list clients
```

Refer to the [Smithery CLI documentation](https://github.com/smithery-ai/cli) for additional details.

## Response Pagination
When retrieving transcripts for longer videos, the content may exceed the token size limits of the LLM.
To avoid this issue, this server splits transcripts that exceed 50,000 characters.
If a transcript is split, the response will include a `next_cursor`.
To retrieve the next part, include this `next_cursor` value in your request.

The token size limits vary depending on the LLM and language you are using.
If you need to split responses into smaller chunks,
you can adjust this using the `--response-limit` command line argument.
For example, the configuration below splits responses to contain no more than 15,000 characters each:

```json
{
  "mcpServers": {
    "youtube-transcript": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/jkawamoto/mcp-youtube-transcript",
        "mcp-youtube-transcript",
        "--response-limit",
        "15000"
      ]
    }
  }
}
```

## Using Proxy Servers
In environments where access to YouTube is restricted, you can use proxy servers.

When using [Webshare](https://www.webshare.io/), set the username and password for the Residential Proxy using either
the environment variables `WEBSHARE_PROXY_USERNAME` and `WEBSHARE_PROXY_PASSWORD`,
or the command line arguments `--webshare-proxy-username` and `--webshare-proxy-password`.

When using other proxy servers, set the proxy server URL using either the environment variables `HTTP_PROXY` or
`HTTPS_PROXY`, or the command line arguments `--http-proxy` or `--https-proxy`.

For more details, please visit:
[Working around IP bans - YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception).

## Remote Deployment

### Deploying to Railway

This MCP server can be deployed to [Railway](https://railway.app) for remote access via HTTP transport.

#### Prerequisites
- A Railway account (sign up at [railway.app](https://railway.app))
- GitHub repository connected to Railway

#### Deployment Steps

1. **Fork or clone this repository** to your GitHub account

2. **Create a new project on Railway**:
   - Go to [railway.app](https://railway.app) and click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure the deployment**:
   - Railway will automatically detect the `railway.toml` configuration
   - The service will use `Dockerfile.railway` for the build
   - Railway automatically sets the `PORT` environment variable

4. **Set optional environment variables** (if needed):
   - `RESPONSE_LIMIT`: Maximum characters per response (default: 50000)
   - `WEBSHARE_PROXY_USERNAME`: Webshare proxy username
   - `WEBSHARE_PROXY_PASSWORD`: Webshare proxy password
   - `HTTP_PROXY`: HTTP proxy server URL
   - `HTTPS_PROXY`: HTTPS proxy server URL

5. **Deploy**: Railway will automatically build and deploy your server

6. **Get your deployment URL**: After deployment, Railway will provide a URL like `https://your-service.railway.app`

#### Connecting to Remote Server

> [!IMPORTANT]
> Claude Desktop **Free** version does **NOT** support remote MCP servers.
> You need Claude Desktop **Pro** or use **Cursor** to connect to remote MCP servers.

**For Claude Desktop Pro**, add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "youtube-transcript": {
      "url": "https://your-service.railway.app"
    }
  }
}
```

**For Cursor**, add to your MCP settings:
```json
{
  "mcpServers": {
    "youtube-transcript": {
      "url": "https://your-service.railway.app"
    }
  }
}
```

### Deploying to VPS with Docker Compose

For deployment to a traditional VPS or any server with Docker installed:

1. **Copy the repository** to your server

2. **Run with Docker Compose**:
   ```bash
   # Start the service
   docker-compose up -d

   # View logs
   docker-compose logs -f

   # Stop the service
   docker-compose down

   # Rebuild after code changes
   docker-compose up -d --build
   ```

3. **Configure your firewall** to allow access to port 8000

4. **Connect using your server's IP or domain**:
   ```json
   {
     "mcpServers": {
       "youtube-transcript": {
         "url": "http://your-server-ip:8000"
       }
     }
   }
   ```

### Local Testing with HTTP Transport

To test the HTTP transport locally before deploying:

```bash
# Run with HTTP transport
uv run mcp-youtube-transcript --transport http --host 127.0.0.1 --port 8000

# Or use Docker Compose
docker-compose up
```

The server will be available at `http://localhost:8000`.

## Integration with n8n

> [!IMPORTANT]
> n8n's MCP Client Tool **only supports SSE transport** (not HTTP Streamable).
> You must deploy the server with `--transport sse` for n8n compatibility.

### Deploying for n8n

#### Option 1: Railway with SSE

Modify `railway.toml` to use the n8n-compatible Dockerfile:

```toml
[build]
builder = "dockerfile"
dockerfilePath = "Dockerfile.n8n"  # Changed from Dockerfile.railway
```

Then deploy to Railway as described above.

#### Option 2: VPS with Docker Compose

```bash
# Use the n8n-specific docker-compose file
docker-compose -f docker-compose.n8n.yml up -d
```

#### Option 3: Manual Command

```bash
# Run with SSE transport
uv run mcp-youtube-transcript --transport sse --host 0.0.0.0 --port 8000
```

### Configuring n8n MCP Client Tool

1. **Add MCP Client Tool node** to your n8n workflow

2. **Configure the SSE Endpoint**:
   - **SSE Endpoint**: `http://your-server-ip:8000` (or your Railway URL)
   - **Authentication**: Select "None" (unless you add auth to the server)

3. **Select Tools**:
   - Choose "All" to expose all tools (`get_transcript` and `get_video_info`)
   - Or select specific tools manually

4. **Connect to AI Agent**: Link the MCP Client Tool to your AI Agent node

### Example n8n Workflow

```
Trigger → AI Agent → MCP Client Tool (YouTube Transcript)
                  ↓
            Process transcript
                  ↓
            Send to output
```

The MCP Client Tool will provide access to:
- `get_transcript`: Fetch YouTube video transcripts
- `get_video_info`: Get video metadata (title, description, uploader)

## License

This application is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
