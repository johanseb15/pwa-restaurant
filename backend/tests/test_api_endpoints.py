import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from main import app
from services.auth import AuthService
from services.products import ProductService

class TestAPIEndpoints:
    """Test suite for API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    @pytest.fixture
    def mock_auth_service(self):
        """Mock authentication service"""
        with patch('main.get_auth_service') as mock_get_auth_service:
            mock_auth_service_instance = AsyncMock(spec=AuthService)
            mock_get_auth_service.return_value = mock_auth_service_instance
            yield mock_auth_service_instance

    @pytest.fixture
    def mock_product_service(self):
        """Mock product service"""
        with patch('main.get_product_service') as mock_get_product_service:
            mock_product_service_instance = AsyncMock(spec=ProductService)
            mock_get_product_service.return_value = mock_product_service_instance
            yield mock_product_service_instance

    @pytest.fixture(autouse=True)
    def mock_db_get_collection(self):
        """Mock db.mongo.get_collection to prevent actual DB calls"""
        with patch('db.mongo.get_collection') as mock_get_collection:
            mock_get_collection.return_value = AsyncMock()
            yield mock_get_collection
    
    
    
    @pytest.fixture
    def valid_token(self, mock_auth_service):
        """Generate a valid test token using the mocked AuthService"""
        return mock_auth_service.create_access_token({
            "sub": "testuser",
            "restaurant_slug": "test-restaurant",
            "role": "admin",
            "user_id": "user_123"
        })
    
    def test_login_success(self, client, mock_auth_service):
        """Test successful login"""
        # Mock successful authentication
        mock_auth_service.authenticate_user = AsyncMock(return_value={
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "token_type": "bearer",
            "expires_in": 1800,
            "user": {
                "id": "user_123",
                "username": "testuser",
                "role": "admin",
                "restaurant_slug": "test-restaurant"
            }
        })
        
        response = client.post("/auth/login", json={
            "username": "testuser",
            "password": "testpass",
            "restaurant_slug": "test-restaurant"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["access_token"] == "test_access_token"
        assert data["user"]["username"] == "testuser"
    
    def test_login_failure(self, client, mock_auth_service):
        """Test failed login"""
        # Mock failed authentication
        mock_auth_service.authenticate_user = AsyncMock(return_value=None)
        
        response = client.post("/auth/login", json={
            "username": "wronguser",
            "password": "wrongpass",
            "restaurant_slug": "test-restaurant"
        })
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
    
    def test_login_validation_error(self, client):
        """Test login with invalid data"""
        response = client.post("/auth/login", json={
            "username": "",  # Empty username
            "password": "pass"
            # Missing restaurant_slug
        })
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        assert "errors" not in data # FastAPI 0.100+ uses 'detail' for validation errors
    
    def test_refresh_token_success(self, client, mock_auth_service):
        """Test successful token refresh"""
        mock_auth_service.refresh_access_token = AsyncMock(return_value={
            "access_token": "new_access_token",
            "refresh_token": "new_refresh_token",
            "token_type": "bearer",
            "expires_in": 1800,
            "user": {
                "id": "user_123",
                "username": "testuser",
                "role": "admin",
                "restaurant_slug": "test-restaurant"
            }
        })
        
        response = client.post("/auth/refresh", json={
            "refresh_token": "valid_refresh_token"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["access_token"] == "new_access_token"
    
    def test_get_products(self, client, mock_product_service, valid_token):
        """Test get products endpoint"""
        mock_product_service.get_products_by_restaurant = AsyncMock(return_value=[
            {
                "id": "prod_1",
                "name": "Margherita Pizza",
                "description": "Classic pizza",
                "price": 15.99,
                "image": "",
                "category_id": "cat_1",
                "sizes": [],
                "toppings": [],
                "is_available": True,
                "is_popular": True,
                "is_vegetarian": True,
                "is_vegan": False,
                "allergens": [],
                "preparation_time": 20,
                "rating": 4.5,
                "rating_count": 100
            }
        ])
        
        headers = {"Authorization": f"Bearer {valid_token}"}
        response = client.get("/api/products", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Margherita Pizza"
        assert data[0]["price"] == 15.99
    
    def test_create_product(self, client, mock_product_service, valid_token):
        """Test create product endpoint"""
        mock_product_service.create_product = AsyncMock(return_value={
            "id": "new_prod_1",
            "name": "New Pizza",
            "description": "New delicious pizza",
            "price": 12.99,
            "image": "",
            "category_id": "cat_1",
            "sizes": [],
            "toppings": [],
            "is_available": True,
            "is_popular": False,
            "is_vegetarian": False,
            "is_vegan": False,
            "allergens": [],
            "preparation_time": 15,
            "rating": 0.0,
            "rating_count": 0
        })
        
        headers = {"Authorization": f"Bearer {valid_token}"}
        product_data = {
            "name": "New Pizza",
            "description": "New delicious pizza",
            "price": 12.99,
            "image": "",
            "category_id": "cat_1",
            "sizes": [],
            "toppings": [],
            "is_popular": False,
            "is_vegetarian": False,
            "is_vegan": False,
            "allergens": [],
            "preparation_time": 15
        }
        response = client.post("/api/products", json=product_data, headers=headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "New Pizza"
        assert data["price"] == 12.99

    def test_protected_endpoint_without_auth(self, client):
        """Test protected endpoint without authentication"""
        response = client.get("/protected-test")
        
        assert response.status_code == 401  # Unauthorized
    
    def test_protected_endpoint_with_invalid_token(self, client):
        """Test protected endpoint with invalid token"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/protected-test", headers=headers)
        
        assert response.status_code == 401  # Unauthorized
    
    def test_admin_protected_endpoint_without_admin_role(self, client, valid_token):
        """Test admin protected endpoint with non-admin role"""
        # Create a valid token for a non-admin user
        auth_service = AuthService()
        non_admin_token = auth_service.create_access_token({
            "sub": "testuser",
            "restaurant_slug": "test-restaurant",
            "role": "customer", # Non-admin role
            "user_id": "user_123"
        })
        headers = {"Authorization": f"Bearer {non_admin_token}"}
        response = client.get("/admin-test", headers=headers)
        
        assert response.status_code == 403  # Forbidden

    def test_admin_protected_endpoint_with_admin_role(self, client, valid_token):
        """Test admin protected endpoint with admin role"""
        headers = {"Authorization": f"Bearer {valid_token}"}
        response = client.get("/admin-test", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "Hello admin" in data["message"]

# Fixture for running async tests
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
    
    