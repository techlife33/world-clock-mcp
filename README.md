# World Clock MCP

A Model Context Protocol (MCP) server for world clock and timezone operations.

## Features

- Get current time for any timezone
- List available timezones
- IP-based timezone detection
- Compare multiple timezones
- Convert time between timezones

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Run Server
```bash
python run_server.py
```

### Test
```bash
pytest tests/
```

### Debug in VS Code
Press F5 to run with debugger attached.

## API Endpoints

- `get_current_time(timezone)` - Current time for timezone
- `get_timezone_list(area?)` - List timezones
- `get_time_by_ip(ip?)` - Time by IP geolocation
- `compare_timezones(timezones[])` - Multi-zone comparison
- `convert_time(datetime, from_zone, to_zone)` - Time conversion

## MCP Installation (option 1)

1. Install required Python packages:
```bash
pip install mcp aiohttp
```

## Configuration

2. Add to Claude Desktop config:
```json
{
  "mcpServers": {
    "world-clock": {
      "command": "python",
      "args": ["path/to/run_server.py"]
    }
  }
}
```

3. Restart Claude Desktop

## MCP Installation (option 2)

1. Clone this repository:
```bash
git clone https://github.com/yourusername/world-clock-mcp.git
cd world-clock-mcp
```

2. Install the package:
```bash
pip install -e .
```

This will automatically install all required dependencies (`mcp`, `aiohttp`) and create the `world-clock-mcp` command.

## Configuration

Add to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "world-clock": {
      "command": "world-clock-mcp"
    }
  }
}
```

**Config file locations:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

Restart Claude Desktop after adding the configuration.

## Usage

Once configured, you can use the world clock tools directly in Claude Desktop:

- "What time is it in Tokyo?"
- "List all timezones in Europe"
- "Convert 3 PM EST to PST"
- "Compare times in New York, London, and Tokyo"
