"""
Base test classes and utilities for the members_app test suite.
These provide common functionality and fixtures for all test cases.
"""

import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from tenant_manager.models import Tenant, Domain
from trainers.models import Trainer
from exercise_class.models import ExerciseClassEvent, ExerciseClassOccurrence, Booking
from workouts.models import Workout, Exercise
from notifications.models import Notification

User = get_user_model()


class BaseTestCase(TestCase):
    """Base test case with common fixtures and helper methods."""
    
    @classmethod
    def setUpTestData(cls):
        """Set up test data that can be reused across test methods."""
        # Create test users
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        cls.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        # Create test trainer
        cls.trainer = Trainer.objects.create(
            name='Test Trainer',
            bio='Test trainer bio',
            specialization='Fitness'
        )
        
        # Create test exercise
        cls.exercise = Exercise.objects.create(
            name='Push Up',
            description='Basic push up exercise',
            muscle_group='Chest'
        )
        
        # Create test workout
        cls.workout = Workout.objects.create(
            name='Test Workout',
            description='A test workout',
            difficulty=Workout.BEGINNER,
            duration=datetime.timedelta(minutes=30),
            created_by=cls.user,
            featured=True
        )
        
        # Create test exercise class event
        cls.class_event = ExerciseClassEvent.objects.create(
            class_name='Test Class',
            description='A test exercise class',
            location='Test Gym',
            max_participants=10,
            trainer=cls.trainer,
            start_time=datetime.time(9, 0),
            duration=datetime.timedelta(hours=1)
        )
        
        # Create test exercise class occurrence
        cls.class_occurrence = ExerciseClassOccurrence.objects.create(
            event=cls.class_event,
            scheduled_date=timezone.now().date() + datetime.timedelta(days=1)
        )
    
    def create_user(self, username='testuser2', email='test2@example.com', **kwargs):
        """Helper method to create additional test users."""
        defaults = {
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        defaults.update(kwargs)
        return User.objects.create_user(username=username, email=email, **defaults)
    
    def create_booking(self, user=None, occurrence=None):
        """Helper method to create test bookings."""
        if user is None:
            user = self.user
        if occurrence is None:
            occurrence = self.class_occurrence
        
        return Booking.objects.create(
            occurrence=occurrence,
            participant=user
        )
    
    def create_notification(self, recipient=None, **kwargs):
        """Helper method to create test notifications."""
        if recipient is None:
            recipient = self.user
        
        defaults = {
            'verb': 'test',
            'description': 'Test notification',
            'level': 'info'
        }
        defaults.update(kwargs)
        
        return Notification.objects.create(recipient=recipient, **defaults)


class BaseTenantTestCase(TenantTestCase):
    """Base test case for multi-tenant functionality."""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create tenant
        cls.tenant = Tenant.objects.create(
            schema_name='test_tenant',
            name='Test Tenant'
        )
        
        # Create domain
        cls.domain = Domain.objects.create(
            tenant=cls.tenant,
            domain='test.localhost',
            is_primary=True
        )
        
        # Set up tenant client
        cls.client = TenantClient(cls.tenant)
    
    def setUp(self):
        super().setUp()
        # Set up test data for tenant
        self.user = User.objects.create_user(
            username='tenant_user',
            email='tenant@example.com',
            password='testpass123'
        )
        
        self.trainer = Trainer.objects.create(
            name='Tenant Trainer',
            bio='Tenant trainer bio'
        )


class APITestMixin:
    """Mixin for API testing functionality."""
    
    def authenticate_user(self, user=None):
        """Authenticate a user for API testing."""
        if user is None:
            user = self.user
        
        from rest_framework.authtoken.models import Token
        token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        return token
    
    def assert_api_response(self, response, status_code=200, has_data=True):
        """Assert common API response conditions."""
        self.assertEqual(response.status_code, status_code)
        if has_data and status_code == 200:
            self.assertIsNotNone(response.content)


class CeleryTestMixin:
    """Mixin for testing Celery tasks."""
    
    def run_task_synchronously(self, task_func, *args, **kwargs):
        """Run a Celery task synchronously for testing."""
        from celery import current_app
        current_app.conf.task_always_eager = True
        current_app.conf.task_eager_propagates = True
        
        return task_func.apply(args=args, kwargs=kwargs)


class FormTestMixin:
    """Mixin for testing Django forms."""
    
    def assert_form_valid(self, form, should_be_valid=True):
        """Assert form validity and print errors if invalid."""
        if should_be_valid:
            if not form.is_valid():
                self.fail(f"Form should be valid. Errors: {form.errors}")
        else:
            self.assertFalse(form.is_valid(), "Form should be invalid")
    
    def get_form_data(self, **overrides):
        """Get basic form data with optional overrides."""
        data = {
            'name': 'Test Item',
            'description': 'Test description'
        }
        data.update(overrides)
        return data
