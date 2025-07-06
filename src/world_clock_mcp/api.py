"""World Time API client module"""

import logging
from typing import Dict, Any
import aiohttp

logger = logging.getLogger(__name__)

# World Time API base URL
BASE_URL = "http://worldtimeapi.org/api"

class WorldTimeAPI:
    """World Time API client"""
    
    @staticmethod
    async def make_request(endpoint: str, timeout: int = 10) -> Dict[str, Any]:
        """Make HTTP request to World Time API"""
        url = f"{BASE_URL}/{endpoint}"
        
        try:
            timeout_config = aiohttp.ClientTimeout(total=timeout)
            async with aiohttp.ClientSession(timeout=timeout_config) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        raise Exception(f"API request failed with status {response.status}")
        except Exception as e:
            logger.error(f"Error fetching from {url}: {e}")
            raise
