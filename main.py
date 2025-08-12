#!/usr/bin/env python3
import asyncio
from typing import Any
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from mcp.server import Server
from mcp.types import Tool, TextContent


app = Server("youtube-transcript")


def extract_video_id(url: str) -> str:
    parsed = urlparse(url)
    if parsed.hostname in ['www.youtube.com', 'youtube.com']:
        if parsed.path == '/watch':
            return parse_qs(parsed.query).get('v', [None])[0]
        elif parsed.path.startswith('/embed/'):
            return parsed.path.split('/')[2]
    elif parsed.hostname in ['youtu.be', 'www.youtu.be']:
        return parsed.path[1:]
    elif 'youtube.com' in url:
        if '/v/' in url:
            return url.split('/v/')[1].split('&')[0]
    raise ValueError(f"Could not extract video ID from URL: {url}")


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_transcript",
            description="Get the transcript of a YouTube video",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "YouTube video URL"
                    },
                    "languages": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Preferred languages (e.g., ['en', 'th']). Defaults to auto-detect"
                    }
                },
                "required": ["url"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    if name != "get_transcript":
        raise ValueError(f"Unknown tool: {name}")
    
    url = arguments.get("url")
    if not url:
        raise ValueError("URL is required")
    
    languages = arguments.get("languages", None)
    
    try:
        video_id = extract_video_id(url)
        
        # Get list of available transcripts - need to create an instance
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        
        # Find the transcript in the requested language(s) or auto-select
        if languages:
            transcript_obj = transcript_list.find_transcript(languages)
        else:
            # Get the first available transcript
            transcript_obj = next(iter(transcript_list))
        
        # Fetch the actual transcript data
        transcript_entries = transcript_obj.fetch()
        
        # Join all text entries with spaces for clean reading
        formatted_transcript = " ".join([
            entry.text
            for entry in transcript_entries
        ])
        
        return [TextContent(
            type="text",
            text=f"Transcript for video {video_id}:\n\n{formatted_transcript}"
        )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error getting transcript: {str(e)}"
        )]


async def main():
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())