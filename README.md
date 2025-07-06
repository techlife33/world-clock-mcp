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

## Installation

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