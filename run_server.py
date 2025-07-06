#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from world_clock_mcp.server import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
