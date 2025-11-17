"""Tests for subscription plans"""
import pytest
from fastapi import status


@pytest.mark.asyncio
class TestPlansEndpoints:
    """Test subscription plans endpoints"""
    
    async def test_list_plans(self, client):
        """Test listing all available plans"""
        response = await client.get("/api/v1/plans/")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert isinstance(data, list)
        # Should have 3 plans: Free, Pro, Enterprise
        assert len(data) >= 3
    
    async def test_plan_structure(self, client):
        """Test plan object structure"""
        response = await client.get("/api/v1/plans/")
        plans = response.json()
        
        if plans:
            plan = plans[0]
            assert "id" in plan
            assert "name" in plan
            assert "price" in plan
            assert "features" in plan
            assert "billing_interval" in plan
            assert "is_active" in plan
    
    async def test_plans_sorted_by_price(self, client):
        """Test plans are sorted by price"""
        response = await client.get("/api/v1/plans/")
        plans = response.json()
        
        if len(plans) >= 2:
            # Check if prices are in ascending order
            prices = [float(plan["price"]) for plan in plans if plan["is_active"]]
            assert prices == sorted(prices), "Plans should be sorted by price"
    
    async def test_free_plan_exists(self, client):
        """Test that Free plan exists"""
        response = await client.get("/api/v1/plans/")
        plans = response.json()
        
        free_plans = [p for p in plans if p["name"].lower() == "free"]
        assert len(free_plans) > 0, "Free plan should exist"
        assert float(free_plans[0]["price"]) == 0, "Free plan price should be 0"
    
    async def test_get_plan_by_id(self, client):
        """Test getting a single plan by ID"""
        # Get list of plans first
        list_response = await client.get("/api/v1/plans/")
        plans = list_response.json()
        
        if plans:
            plan_id = plans[0]["id"]
            response = await client.get(f"/api/v1/plans/{plan_id}")
            assert response.status_code == status.HTTP_200_OK
            
            data = response.json()
            assert data["id"] == plan_id
    
    async def test_get_nonexistent_plan(self, client):
        """Test getting a non-existent plan"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = await client.get(f"/api/v1/plans/{fake_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
