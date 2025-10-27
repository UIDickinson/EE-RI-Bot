"""
Live agent test - requires server running
Run manually: python tests/test_live_agent.py
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app import EEResearchScout
from sentient_agent_framework import Session, Query


class MockResponseHandler:
    """Mock response handler for testing"""
    
    async def emit_text_block(self, title, content):
        print(f"[{title}] {content}")
    
    async def emit_json(self, title, data):
        print(f"[{title}] {data}")
    
    def create_text_stream(self, title):
        return MockTextStream(title)
    
    async def complete(self):
        print("[COMPLETE]")
    
    async def emit_error(self, title, error):
        print(f"[ERROR - {title}] {error}")


class MockTextStream:
    def __init__(self, title):
        self.title = title
    
    async def emit_chunk(self, chunk):
        print(chunk, end='', flush=True)
    
    async def complete(self):
        print(f"\n[{self.title} COMPLETE]")


async def test_agent_assist():
    """Test the assist method"""
    print("=" * 60)
    print("Testing EEResearchScout.assist() method")
    print("=" * 60)
    
    agent = EEResearchScout(name="test-agent")
    
    session = Session(
        user_id="test_user",
        session_id="test_session",
        processor_id="test",
        activity_id="test_activity",
        request_id="test_request",
        interactions=[]
    )
    
    query = Query(
        id="test_query",
        prompt="What are GaN transistors?"
    )
    
    response_handler = MockResponseHandler()
    
    try:
        await agent.assist(session, query, response_handler)
        print("\n✅ assist() method test PASSED")
        return True
    except Exception as e:
        print(f"\n❌ assist() method test FAILED: {e}")
        return False


if __name__ == "__main__":
    result = asyncio.run(test_agent_assist())
    sys.exit(0 if result else 1)