
#!/usr/bin/env python3

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

from .api import WorldTimeAPI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the MCP server
app = Server("world-clock")

@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools"""
    return [
        Tool(
            name="get_current_time",
            description="Get current time for a specific timezone",
            inputSchema={
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "Timezone in format 'Area/Location' (e.g., 'America/New_York', 'Europe/London')"
                    }
                },
                "required": ["timezone"]
            }
        ),
        Tool(
            name="get_timezone_list",
            description="Get list of available timezones, optionally filtered by area",
            inputSchema={
                "type": "object",
                "properties": {
                    "area": {
                        "type": "string",
                        "description": "Optional area filter (e.g., 'America', 'Europe', 'Asia')"
                    }
                }
            }
        ),
        Tool(
            name="get_time_by_ip",
            description="Get current time based on IP address geolocation",
            inputSchema={
                "type": "object",
                "properties": {
                    "ip": {
                        "type": "string",
                        "description": "Optional IP address. If not provided, uses requester's IP"
                    }
                }
            }
        ),
        Tool(
            name="compare_timezones",
            description="Compare current time across multiple timezones",
            inputSchema={
                "type": "object",
                "properties": {
                    "timezones": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of timezones to compare"
                    }
                },
                "required": ["timezones"]
            }
        ),
        Tool(
            name="convert_time",
            description="Convert a specific datetime from one timezone to another",
            inputSchema={
                "type": "object",
                "properties": {
                    "datetime": {
                        "type": "string",
                        "description": "DateTime string in ISO format or 'YYYY-MM-DD HH:MM:SS'"
                    },
                    "from_timezone": {
                        "type": "string",
                        "description": "Source timezone"
                    },
                    "to_timezone": {
                        "type": "string",
                        "description": "Target timezone"
                    }
                },
                "required": ["datetime", "from_timezone", "to_timezone"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls"""
    
    try:
        if name == "get_current_time":
            return await get_current_time(arguments["timezone"])
        
        elif name == "get_timezone_list":
            area = arguments.get("area")
            return await get_timezone_list(area)
        
        elif name == "get_time_by_ip":
            ip = arguments.get("ip")
            return await get_time_by_ip(ip)
        
        elif name == "compare_timezones":
            return await compare_timezones(arguments["timezones"])
        
        elif name == "convert_time":
            return await convert_time(
                arguments["datetime"],
                arguments["from_timezone"],
                arguments["to_timezone"]
            )
        
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        logger.error(f"Error in {name}: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

async def get_current_time(timezone: str) -> List[TextContent]:
    """Get current time for a specific timezone"""
    try:
        data = await WorldTimeAPI.make_request(f"timezone/{timezone}")
        
        result = {
            "timezone": data["timezone"],
            "datetime": data["datetime"],
            "utc_datetime": data["utc_datetime"],
            "utc_offset": data["utc_offset"],
            "timezone_abbreviation": data["abbreviation"],
            "day_of_week": data["day_of_week"],
            "day_of_year": data["day_of_year"],
            "week_number": data["week_number"],
            "dst": data["dst"],
            "unix_timestamp": data["unixtime"]
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error getting time for {timezone}: {str(e)}"
        )]

async def get_timezone_list(area: Optional[str] = None) -> List[TextContent]:
    """Get list of available timezones"""
    try:
        endpoint = "timezone"
        if area:
            endpoint += f"/{area}"
        
        timezones = await WorldTimeAPI.make_request(endpoint)
        
        if isinstance(timezones, list):
            result = {
                "count": len(timezones),
                "timezones": sorted(timezones)
            }
        else:
            result = timezones
            
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error getting timezone list: {str(e)}"
        )]

async def get_time_by_ip(ip: Optional[str] = None) -> List[TextContent]:
    """Get current time based on IP geolocation"""
    try:
        endpoint = "ip"
        if ip:
            endpoint += f"/{ip}"
        
        data = await WorldTimeAPI.make_request(endpoint)
        
        result = {
            "timezone": data["timezone"],
            "datetime": data["datetime"],
            "utc_datetime": data["utc_datetime"],
            "utc_offset": data["utc_offset"],
            "timezone_abbreviation": data["abbreviation"],
            "client_ip": data.get("client_ip", "N/A"),
            "dst": data["dst"],
            "unix_timestamp": data["unixtime"]
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error getting time by IP: {str(e)}"
        )]

async def compare_timezones(timezones: List[str]) -> List[TextContent]:
    """Compare current time across multiple timezones"""
    try:
        results = []
        
        for tz in timezones:
            try:
                data = await WorldTimeAPI.make_request(f"timezone/{tz}")
                results.append({
                    "timezone": data["timezone"],
                    "datetime": data["datetime"],
                    "utc_offset": data["utc_offset"],
                    "abbreviation": data["abbreviation"],
                    "dst": data["dst"]
                })
            except Exception as e:
                results.append({
                    "timezone": tz,
                    "error": str(e)
                })
        
        comparison = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "zones_compared": len(timezones),
            "results": results
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(comparison, indent=2)
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error comparing timezones: {str(e)}"
        )]

async def convert_time(datetime_str: str, from_timezone: str, to_timezone: str) -> List[TextContent]:
    """Convert a specific datetime from one timezone to another"""
    try:
        # Get timezone data for both zones
        from_data = await WorldTimeAPI.make_request(f"timezone/{from_timezone}")
        to_data = await WorldTimeAPI.make_request(f"timezone/{to_timezone}")
        
        # Parse input datetime
        try:
            if 'T' in datetime_str:
                # ISO format
                dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
            else:
                # Assume format: YYYY-MM-DD HH:MM:SS
                dt = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise ValueError(f"Invalid datetime format: {datetime_str}")
        
        # Calculate conversion
        from_offset_hours = int(from_data["utc_offset"][:3])
        from_offset_minutes = int(from_data["utc_offset"][4:6])
        from_offset_seconds = from_offset_hours * 3600 + from_offset_minutes * 60
        
        to_offset_hours = int(to_data["utc_offset"][:3])
        to_offset_minutes = int(to_data["utc_offset"][4:6])
        to_offset_seconds = to_offset_hours * 3600 + to_offset_minutes * 60
        
        # Convert to UTC first, then to target timezone
        utc_dt = dt.replace(tzinfo=timezone.utc) - timezone.utc.utcoffset(dt)
        utc_timestamp = utc_dt.timestamp() - from_offset_seconds
        target_dt = datetime.fromtimestamp(utc_timestamp + to_offset_seconds)
        
        result = {
            "original_datetime": datetime_str,
            "from_timezone": from_timezone,
            "to_timezone": to_timezone,
            "converted_datetime": target_dt.strftime('%Y-%m-%d %H:%M:%S'),
            "from_utc_offset": from_data["utc_offset"],
            "to_utc_offset": to_data["utc_offset"],
            "from_abbreviation": from_data["abbreviation"],
            "to_abbreviation": to_data["abbreviation"]
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error converting time: {str(e)}"
        )]

async def main():
    """Main function to run the MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
