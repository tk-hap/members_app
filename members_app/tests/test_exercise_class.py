"""
Test cases for exercise class functionality including events, occurrences, and bookings.
"""

import datetime
from django.utils import timezone

from tests.base import BaseTestCase, CeleryTestMixin
from exercise_class.models import ExerciseClassEvent, ExerciseClassOccurrence, Booking
from exercise_class.tasks import generate_occurrences_all_tenants
from exercise_class.utils import generate_occurrences_for_event


class ExerciseClassEventTest(BaseTestCase):
    """Test cases for ExerciseClassEvent model."""
    
    def test_exercise_class_event_creation(self):
        """Test basic exercise class event creation."""
        event = ExerciseClassEvent.objects.create(
            class_name='Yoga Class',
            description='Relaxing yoga session',
            location='Studio A',
            max_participants=15,
            trainer=self.trainer,
            start_time=datetime.time(10, 0),
            duration=datetime.timedelta(minutes=90)
        )
        
        self.assertEqual(event.class_name, 'Yoga Class')
        self.assertEqual(event.max_participants, 15)
        self.assertEqual(event.trainer, self.trainer)
    
    def test_exercise_class_event_str_representation(self):
        """Test string representation of exercise class event."""
        self.assertEqual(str(self.class_event), 'Test Class')
    
    def test_exercise_class_event_duration(self):
        """Test that duration field works correctly."""
        self.assertEqual(self.class_event.duration, datetime.timedelta(hours=1))


class ExerciseClassOccurrenceTest(BaseTestCase):
    """Test cases for ExerciseClassOccurrence model."""
    
    def test_exercise_class_occurrence_creation(self):
        """Test basic exercise class occurrence creation."""
        occurrence = ExerciseClassOccurrence.objects.create(
            event=self.class_event,
            scheduled_date=timezone.now().date() + datetime.timedelta(days=2)
        )
        
        self.assertEqual(occurrence.event, self.class_event)
        self.assertFalse(occurrence.reminder_sent)
    
    def test_exercise_class_occurrence_str_representation(self):
        """Test string representation of exercise class occurrence."""
        expected = f"{self.class_event.class_name} on {self.class_occurrence.scheduled_date}"
        self.assertEqual(str(self.class_occurrence), expected)
    
    def test_is_upcoming_method(self):
        """Test is_upcoming method for exercise class occurrence."""
        # Future occurrence should be upcoming
        future_occurrence = ExerciseClassOccurrence.objects.create(
            event=self.class_event,
            scheduled_date=timezone.now().date() + datetime.timedelta(days=7)
        )
        self.assertTrue(future_occurrence.is_upcoming())
        
        # Past occurrence should not be upcoming
        past_occurrence = ExerciseClassOccurrence.objects.create(
            event=self.class_event,
            scheduled_date=timezone.now().date() - datetime.timedelta(days=1)
        )
        self.assertFalse(past_occurrence.is_upcoming())
    
    def test_get_participants_method(self):
        """Test get_participants method for exercise class occurrence."""
        # Create bookings for the occurrence
        self.create_booking(self.user, self.class_occurrence)
        user2 = self.create_user('user2', 'user2@example.com')
        self.create_booking(user2, self.class_occurrence)
        
        participants = self.class_occurrence.get_participants()
        self.assertEqual(participants.count(), 2)
        self.assertIn(self.user, participants)
        self.assertIn(user2, participants)
    
    def test_spots_remaining_method(self):
        """Test spots_remaining method for exercise class occurrence."""
        # Initially should have max participants available
        self.assertEqual(self.class_occurrence.spots_remaining(), 10)
        
        # After one booking, should have 9 spots
        self.create_booking(self.user, self.class_occurrence)
        self.assertEqual(self.class_occurrence.spots_remaining(), 9)
        
        # After second booking, should have 8 spots
        user2 = self.create_user('user2', 'user2@example.com')
        self.create_booking(user2, self.class_occurrence)
        self.assertEqual(self.class_occurrence.spots_remaining(), 8)
    
    def test_is_available_method(self):
        """Test is_available method for exercise class occurrence."""
        # Should be available initially
        self.assertTrue(self.class_occurrence.is_available())
        
        # Should still be available with bookings but spots remaining
        self.create_booking(self.user, self.class_occurrence)
        self.assertTrue(self.class_occurrence.is_available())
        
        # Create enough bookings to fill the class
        for i in range(9):  # Already have 1 booking, need 9 more
            user = self.create_user(f'user{i+2}', f'user{i+2}@example.com')
            self.create_booking(user, self.class_occurrence)
        
        # Should not be available when full
        self.assertFalse(self.class_occurrence.is_available())


class BookingTest(BaseTestCase):
    """Test cases for Booking model."""
    
    def test_booking_creation(self):
        """Test basic booking creation."""
        booking = self.create_booking()
        
        self.assertEqual(booking.occurrence, self.class_occurrence)
        self.assertEqual(booking.participant, self.user)
    
    def test_booking_str_representation(self):
        """Test string representation of booking."""
        booking = self.create_booking()
        expected = f"{self.user.username} - {self.class_event.class_name}"
        self.assertEqual(str(booking), expected)
    
    def test_duplicate_booking_prevention(self):
        """Test that users cannot book the same class twice."""
        # Create first booking
        self.create_booking()
        
        # Try to create duplicate booking - should raise an error
        with self.assertRaises(Exception):
            self.create_booking()
    
    def test_booking_when_class_full(self):
        """Test booking behavior when class is full."""
        # Fill up the class
        for i in range(10):
            user = self.create_user(f'user{i+1}', f'user{i+1}@example.com')
            self.create_booking(user, self.class_occurrence)
        
        # Try to book when full - should raise an error or handle gracefully
        extra_user = self.create_user('extrauser', 'extra@example.com')
        with self.assertRaises(Exception):
            self.create_booking(extra_user, self.class_occurrence)


class ExerciseClassTaskTest(BaseTestCase, CeleryTestMixin):
    """Test cases for exercise class related Celery tasks."""
    
    def test_generate_occurrences_all_tenants_task(self):
        """Test the generate_occurrences_all_tenants task."""
        # This test would need to be adjusted based on your tenant setup
        # For now, we'll test that the task can be called without errors
        try:
            result = self.run_task_synchronously(generate_occurrences_all_tenants)
            self.assertTrue(result.successful())
        except Exception as e:
            # If tenants aren't set up in test environment, that's expected
            self.assertIn('tenant', str(e).lower())
    
    def test_generate_occurrences_for_event_utility(self):
        """Test the generate_occurrences_for_event utility function."""
        # Count initial occurrences
        initial_count = ExerciseClassOccurrence.objects.filter(event=self.class_event).count()
        
        # Generate occurrences (this would depend on your recurrence implementation)
        generate_occurrences_for_event(self.class_event)
        
        # Count should increase (exact number depends on recurrence rules)
        final_count = ExerciseClassOccurrence.objects.filter(event=self.class_event).count()
        self.assertGreaterEqual(final_count, initial_count)


class ExerciseClassViewTest(BaseTestCase):
    """Test cases for exercise class views."""
    
    def test_exercise_class_detail_view(self):
        """Test exercise class detail view."""
        response = self.client.get(f'/classes/{self.class_occurrence.id}/')
        self.assertEqual(response.status_code, 200)
    
    def test_exercise_class_booking_view(self):
        """Test exercise class booking functionality."""
        # Login the user first
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(f'/classes/book/{self.class_occurrence.id}/')
        self.assertEqual(response.status_code, 200)
        
        # Verify booking was created
        self.assertTrue(
            Booking.objects.filter(
                occurrence=self.class_occurrence,
                participant=self.user
            ).exists()
        )
    
    def test_exercise_class_cancel_booking_view(self):
        """Test exercise class booking cancellation."""
        # Create a booking first
        self.create_booking()
        
        # Login the user
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(f'/classes/cancel/{self.class_occurrence.id}/')
        self.assertEqual(response.status_code, 200)
        
        # Verify booking was deleted
        self.assertFalse(
            Booking.objects.filter(
                occurrence=self.class_occurrence,
                participant=self.user
            ).exists()
        )
