"""
Test cases for user authentication and user model functionality.
"""

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from tests.base import BaseTestCase, APITestMixin
from users.models import User


class UserModelTest(BaseTestCase):
    """Test cases for the User model."""
    
    def test_user_creation(self):
        """Test basic user creation."""
        user = User.objects.create_user(
            username='newuser',
            email='newuser@example.com',
            password='newpass123'
        )
        
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertTrue(user.check_password('newpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_superuser_creation(self):
        """Test superuser creation."""
        admin = User.objects.create_superuser(
            username='superuser',
            email='super@example.com',
            password='superpass123'
        )
        
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
    
    def test_user_str_representation(self):
        """Test user string representation."""
        self.assertEqual(str(self.user), 'testuser')
    
    def test_user_push_token(self):
        """Test user push token functionality."""
        self.user.push_token = 'test_push_token_123'
        self.user.save()
        
        self.assertEqual(self.user.push_token, 'test_push_token_123')


class AuthenticationTest(BaseTestCase, APITestMixin):
    """Test cases for user authentication."""
    
    def test_user_authentication(self):
        """Test user can authenticate with correct credentials."""
        user = authenticate(username='testuser', password='testpass123')
        self.assertEqual(user, self.user)
    
    def test_user_authentication_failure(self):
        """Test authentication fails with incorrect credentials."""
        user = authenticate(username='testuser', password='wrongpassword')
        self.assertIsNone(user)
    
    def test_token_creation(self):
        """Test that tokens are created for users."""
        token, created = Token.objects.get_or_create(user=self.user)
        self.assertIsNotNone(token.key)
        self.assertTrue(created)
        
        # Test that getting the same token doesn't create a new one
        token2, created2 = Token.objects.get_or_create(user=self.user)
        self.assertEqual(token.key, token2.key)
        self.assertFalse(created2)


class AuthenticationViewTest(BaseTestCase):
    """Test cases for authentication views."""
    
    def test_login_view_get(self):
        """Test login view returns correct template on GET."""
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
    
    def test_login_view_post_success(self):
        """Test successful login via POST."""
        response = self.client.post('/auth/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        # Should return success response
        self.assertEqual(response.status_code, 200)
        self.assertIn('Auth-Token', response)
    
    def test_login_view_post_failure(self):
        """Test failed login via POST."""
        response = self.client.post('/auth/login/', {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        
        # Should return failure response
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Auth-Token', response)
    
    def test_login_view_missing_credentials(self):
        """Test login with missing credentials."""
        response = self.client.post('/auth/login/', {
            'username': 'testuser'
            # missing password
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Auth-Token', response)


class UserAPITest(APITestCase, BaseTestCase, APITestMixin):
    """Test cases for user-related API endpoints."""
    
    def test_authenticated_api_access(self):
        """Test that authenticated users can access protected endpoints."""
        self.authenticate_user()
        
        response = self.client.get('/home/')
        self.assert_api_response(response, status_code=200)
    
    def test_unauthenticated_api_access(self):
        """Test that unauthenticated users are redirected to login."""
        response = self.client.get('/home/')
        # Should redirect to login or return login template
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_token(self):
        """Test API access with invalid token."""
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid_token_123')
        
        response = self.client.get('/home/')
        # Should redirect to login or return login template
        self.assertEqual(response.status_code, 200)
