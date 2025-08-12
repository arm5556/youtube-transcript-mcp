# YouTube Transcript MCP Server

A simple MCP (Model Context Protocol) server that fetches YouTube video transcripts.

## Features

- Extract transcripts from YouTube videos
- Support for multiple languages
- Works with various YouTube URL formats

## Installation

Requires Python 3.10 or higher.

```bash
# Install dependencies
pip install mcp>=1.12.4 youtube-transcript-api>=1.2.2
```

**Tested with:**
- Python 3.11
- mcp 1.12.4
- youtube-transcript-api 1.2.2

## Usage

### Claude Code

Add to `.claude.json` in your project:

```json
{
  "mcpServers": {
    "youtube-transcript": {
      "command": "python3.11",
      "args": ["/absolute/path/to/youtube-transcript-mcp-py/main.py"]
    }
  }
}
```

### Available Tools

#### `get_transcript`
Fetches the transcript of a YouTube video.

**Parameters:**
- `url` (required): YouTube video URL
- `languages` (optional): Array of preferred language codes (e.g., `["en", "th"]`)

**Example:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "languages": ["en"]
}
```

## Tips & Tricks

### Custom Command Example

You can create a custom command that uses this MCP server. Add to your `CLAUDE.md`:

```markdown
#### Custom Commands
### yt - YouTube Blog Converter
Custom command to convert YouTube videos into blog format with maximum 5-minute read time:
1. Use mcp__YouTube__get_transcript tool to fetch transcript from provided URL
2. Transform content into professional blog format optimized for 3-minute read (approximately 600-750 words)
3. Structure as comprehensive blog with clear sections and subheadings
4. Focus on technical insights, implementation details, and practical applications
5. Format with structured sections:
   - **Introduction** (hook and context setting)
   - **Core Concepts** (main technical topics covered)
   - **Implementation Details** (how-to information, code examples, best practices)
   - **Key Insights** (important takeaways and lessons learned)
   - **Practical Applications** (real-world usage and examples)
   - **Bottom Line** (concise summary and final thoughts - REQUIRED section)
6. Use professional writing style with clear explanations and smooth transitions
7. Include relevant technical terminology and maintain accuracy while ensuring accessibility
8. Optimize reading flow with proper paragraph breaks and logical content organization
9. Automatically detect video language and write summary in same language for maximum effectiveness:
   - Thai videos → Thai summaries (preserves technical terminology, cultural context, serves target audience)
   - English videos → English summaries
   - Other languages → English summaries
```

Then use: `yt https://www.youtube.com/watch?v=VIDEO_ID`

**Example result:**

![YouTube Blog Conversion Example](./assets/example-result.png)


## Supported URL Formats

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`
- `https://www.youtube.com/v/VIDEO_ID`

## License

MIT