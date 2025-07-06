"""Tests for WorldTimeAPI client module"""

import pytest
import asyncio
from unittest.mock import patch, AsyncMock
from world_clock_mcp.api import WorldTimeAPI

@pytest.mark.asyncio
async def test_make_request_success():
    """Test WorldTimeAPI.make_request returns data on success"""
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value={"test": "ok"})
    class MockContextManager:
        async def __aenter__(self):
            return mock_response
        async def __aexit__(self, exc_type, exc, tb):
            return None
    def mock_get(*args, **kwargs):
        return MockContextManager()
    mock_session = AsyncMock()
    mock_session.get = mock_get
    mock_session.__aenter__.return_value = mock_session
    mock_session.__aexit__.return_value = None
    with patch('aiohttp.ClientSession', return_value=mock_session):
        result = await WorldTimeAPI.make_request("test/endpoint")
        assert result == {"test": "ok"}

@pytest.mark.asyncio
async def test_make_request_failure():
    """Test WorldTimeAPI.make_request raises on non-200 status"""
    mock_response = AsyncMock()
    mock_response.status = 404
    mock_response.json = AsyncMock(return_value={"error": "not found"})
    class MockContextManager:
        async def __aenter__(self):
            return mock_response
        async def __aexit__(self, exc_type, exc, tb):
            return None
    def mock_get(*args, **kwargs):
        return MockContextManager()
    mock_session = AsyncMock()
    mock_session.get = mock_get
    mock_session.__aenter__.return_value = mock_session
    mock_session.__aexit__.return_value = None
    with patch('aiohttp.ClientSession', return_value=mock_session):
        with pytest.raises(Exception):
            await WorldTimeAPI.make_request("bad/endpoint")

@pytest.mark.asyncio
async def test_make_request_exception():
    """Test WorldTimeAPI.make_request logs and raises on exception"""
    with patch('aiohttp.ClientSession', side_effect=Exception("network error")):
        with pytest.raises(Exception):
            await WorldTimeAPI.make_request("test/endpoint")
