# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

YouTube Transcript MCP Server - An MCP (Model Context Protocol) server that fetches YouTube video transcripts using the `youtube-transcript-api` library.

## Development Commands

```bash
# Install dependencies (requires Python 3.10+, project uses 3.11)
python3.11 -m pip install mcp youtube-transcript-api

# Run tests to verify server functionality
python3.11 test_server.py

# Run the MCP server directly (for debugging)
python3.11 main.py
```

## Architecture

The server implements a single MCP tool `get_transcript` that:
1. Accepts YouTube URLs in multiple formats (youtube.com/watch, youtu.be, /embed/, /v/)
2. Extracts video ID via `extract_video_id()` function
3. Fetches transcript using `YouTubeTranscriptApi.get_transcript()`
4. Returns formatted transcript with timestamps: `[{timestamp}s] {text}`

Key components:
- `main.py`: Core server implementation using MCP's stdio transport
- Server instance: `app = Server("youtube-transcript")`
- Tool registration: `@app.list_tools()` decorator
- Tool execution: `@app.call_tool()` decorator with async handlers

## Claude Desktop Integration

To use with Claude Desktop, add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "youtube-transcript": {
      "command": "python3.11",
      "args": ["/Users/aram/src/youtube-transcript-mcp-py/main.py"]
    }
  }
}
```

## Tool Parameters

`get_transcript` tool accepts:
- `url` (required): YouTube video URL
- `languages` (optional): Array of language codes like `["en", "th"]`

## Testing Approach

The `test_server.py` verifies:
- Import availability for MCP and youtube-transcript-api
- Server instantiation and tool registration
- Outputs Claude Desktop configuration for easy setup