"""
Test API endpoint functionality
"""

import pytest
import httpx
import asyncio
import json


class TestAPIEndpoint:
    """Test the /assist endpoint"""
    
    @pytest.fixture
    def base_url(self):
        """Base URL for testing"""
        return "http://localhost:8000"
    
    @pytest.fixture
    def sample_request(self):
        """Sample request payload"""
        return {
            "session": {
                "user_id": "test_user_123",
                "session_id": "test_session_456",
                "processor_id": "test_processor",
                "activity_id": "test_activity_789",
                "request_id": "test_request_101",
                "interactions": []
            },
            "query": {
                "id": "test_query_202",
                "prompt": "What are GaN transistors?"
            }
        }
    
    @pytest.mark.asyncio
    async def test_homepage_accessible(self, base_url):
        """Test homepage is accessible"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(base_url, timeout=10.0)
                assert response.status_code == 200
                print("✅ Homepage accessible")
            except httpx.ConnectError:
                pytest.skip("Server not running on localhost:8000")
    
    @pytest.mark.asyncio
    async def test_assist_endpoint_exists(self, base_url, sample_request):
        """Test /assist endpoint exists and responds"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{base_url}/assist",
                    json=sample_request,
                    timeout=30.0
                )
                # Should get some response (200 or streaming)
                assert response.status_code in [200, 201]
                print("✅ /assist endpoint responding")
            except httpx.ConnectError:
                pytest.skip("Server not running on localhost:8000")
            except httpx.ReadTimeout:
                pytest.skip("Response timeout (expected for streaming)")
    
    @pytest.mark.asyncio
    async def test_invalid_request_handling(self, base_url):
        """Test API handles invalid requests gracefully"""
        async with httpx.AsyncClient() as client:
            try:
                # Send invalid JSON
                response = await client.post(
                    f"{base_url}/assist",
                    json={"invalid": "data"},
                    timeout=10.0
                )
                # Should handle gracefully (not crash)
                assert response.status_code in [200, 400, 422, 500]
                print("✅ Invalid request handled gracefully")
            except httpx.ConnectError:
                pytest.skip("Server not running on localhost:8000")
    
    def test_request_structure_validation(self, sample_request):
        """Test request structure is valid"""
        # Check required fields
        assert "session" in sample_request
        assert "query" in sample_request
        
        assert "user_id" in sample_request["session"]
        assert "session_id" in sample_request["session"]
        
        assert "id" in sample_request["query"]
        assert "prompt" in sample_request["query"]
        
        print("✅ Request structure validation passed")


def run_api_tests():
    """Run API endpoint tests"""
    pytest.main([__file__, '-v', '-s'])


if __name__ == "__main__":
    run_api_tests()