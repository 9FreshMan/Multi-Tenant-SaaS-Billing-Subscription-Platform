"""Tests for authentication endpoints"""
import pytest


@pytest.mark.asyncio
class TestAuthEndpoints:
    """Test authentication and authorization"""
    
    async def test_health_check(self, client):
        """Test health check endpoint"""
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
    
    async def test_register_new_tenant(self, client, test_user_data):
        """Test successful tenant registration"""
        response = await client.post("/api/v1/auth/register", json=test_user_data)
        assert response.status_code == 201
        
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
    
    async def test_register_duplicate_email(self, client, test_user_data):
        """Test registration with existing email fails"""
        # First registration
        await client.post("/api/v1/auth/register", json=test_user_data)
        
        # Duplicate registration
        response = await client.post("/api/v1/auth/register", json=test_user_data)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()
    
    async def test_register_invalid_email(self, client, test_user_data):
        """Test registration with invalid email"""
        test_user_data["email"] = "invalid-email"
        response = await client.post("/api/v1/auth/register", json=test_user_data)
        assert response.status_code == 422
    
    async def test_register_short_password(self, client, test_user_data):
        """Test registration with short password"""
        test_user_data["password"] = "123"
        response = await client.post("/api/v1/auth/register", json=test_user_data)
        assert response.status_code == 422
    
    async def test_login_success(self, client, test_user_data):
        """Test successful login"""
        # Register first
        await client.post("/api/v1/auth/register", json=test_user_data)
        
        # Login
        login_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
        response = await client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
    
    async def test_login_wrong_password(self, client, test_user_data):
        """Test login with wrong password"""
        # Register first
        await client.post("/api/v1/auth/register", json=test_user_data)
        
        # Login with wrong password
        login_data = {
            "email": test_user_data["email"],
            "password": "WrongPassword123!"
        }
        response = await client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 401
    
    async def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "SomePassword123!"
        }
        response = await client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 401
    
    async def test_get_current_user(self, client, test_user_data):
        """Test getting current user info"""
        # Register and login
        response = await client.post("/api/v1/auth/register", json=test_user_data)
        token = response.json()["access_token"]
        
        # Get current user
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get("/api/v1/users/me", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["email"] == test_user_data["email"]
    
    async def test_unauthorized_access(self, client):
        """Test accessing protected endpoint without token"""
        response = await client.get("/api/v1/users/me")
        # Expecting 401 but tenant middleware might return 403
        assert response.status_code in [401, 403]
    
    async def test_invalid_token(self, client):
        """Test accessing protected endpoint with invalid token"""
        headers = {"Authorization": "Bearer invalid_token_here"}
        response = await client.get("/api/v1/users/me", headers=headers)
        assert response.status_code in [401, 403]
