"""
Test cases for workout functionality including workouts and exercises.
"""

import datetime
from django.utils import timezone

from tests.base import BaseTestCase, FormTestMixin
from workouts.models import Workout, Exercise, WorkoutExercise
from workouts.forms import WorkoutForm


class WorkoutModelTest(BaseTestCase):
    """Test cases for Workout model."""
    
    def test_workout_creation(self):
        """Test basic workout creation."""
        workout = Workout.objects.create(
            name='HIIT Workout',
            description='High intensity interval training',
            difficulty=Workout.INTERMEDIATE,
            duration=datetime.timedelta(minutes=45),
            created_by=self.user,
            featured=False
        )
        
        self.assertEqual(workout.name, 'HIIT Workout')
        self.assertEqual(workout.difficulty, Workout.INTERMEDIATE)
        self.assertEqual(workout.created_by, self.user)
        self.assertFalse(workout.featured)
    
    def test_workout_str_representation(self):
        """Test string representation of workout."""
        self.assertEqual(str(self.workout), 'Test Workout')
    
    def test_workout_difficulty_choices(self):
        """Test workout difficulty choices."""
        beginner_workout = Workout.objects.create(
            name='Beginner Workout',
            difficulty=Workout.BEGINNER,
            duration=datetime.timedelta(minutes=20),
            created_by=self.user
        )
        
        intermediate_workout = Workout.objects.create(
            name='Intermediate Workout',
            difficulty=Workout.INTERMEDIATE,
            duration=datetime.timedelta(minutes=30),
            created_by=self.user
        )
        
        advanced_workout = Workout.objects.create(
            name='Advanced Workout',
            difficulty=Workout.ADVANCED,
            duration=datetime.timedelta(minutes=60),
            created_by=self.user
        )
        
        self.assertEqual(beginner_workout.difficulty, 'Beginner')
        self.assertEqual(intermediate_workout.difficulty, 'Intermediate')
        self.assertEqual(advanced_workout.difficulty, 'Advanced')
    
    def test_workout_duration_field(self):
        """Test workout duration field functionality."""
        self.assertEqual(self.workout.duration, datetime.timedelta(minutes=30))
        
        # Test with different duration
        long_workout = Workout.objects.create(
            name='Long Workout',
            duration=datetime.timedelta(hours=1, minutes=30),
            difficulty=Workout.BEGINNER,
            created_by=self.user
        )
        
        self.assertEqual(long_workout.duration, datetime.timedelta(hours=1, minutes=30))
    
    def test_featured_workout_filtering(self):
        """Test filtering featured workouts."""
        # Create additional workouts
        Workout.objects.create(
            name='Featured Workout 1',
            duration=datetime.timedelta(minutes=25),
            difficulty=Workout.BEGINNER,
            created_by=self.user,
            featured=True
        )
        
        Workout.objects.create(
            name='Regular Workout',
            duration=datetime.timedelta(minutes=35),
            difficulty=Workout.INTERMEDIATE,
            created_by=self.user,
            featured=False
        )
        
        featured_workouts = Workout.objects.filter(featured=True)
        self.assertEqual(featured_workouts.count(), 2)  # self.workout + Featured Workout 1


class ExerciseModelTest(BaseTestCase):
    """Test cases for Exercise model."""
    
    def test_exercise_creation(self):
        """Test basic exercise creation."""
        exercise = Exercise.objects.create(
            name='Squats',
            description='Basic squat exercise',
            muscle_group='Legs'
        )
        
        self.assertEqual(exercise.name, 'Squats')
        self.assertEqual(exercise.description, 'Basic squat exercise')
        self.assertEqual(exercise.muscle_group, 'Legs')
    
    def test_exercise_str_representation(self):
        """Test string representation of exercise."""
        self.assertEqual(str(self.exercise), 'Push Up')


class WorkoutExerciseModelTest(BaseTestCase):
    """Test cases for WorkoutExercise model."""
    
    def test_workout_exercise_creation(self):
        """Test basic workout exercise creation."""
        workout_exercise = WorkoutExercise.objects.create(
            workout=self.workout,
            exercise=self.exercise,
            sets=3,
            reps=15,
            weight=50.0,
            unit=WorkoutExercise.KG
        )
        
        self.assertEqual(workout_exercise.workout, self.workout)
        self.assertEqual(workout_exercise.exercise, self.exercise)
        self.assertEqual(workout_exercise.sets, 3)
        self.assertEqual(workout_exercise.reps, 15)
        self.assertEqual(workout_exercise.weight, 50.0)
        self.assertEqual(workout_exercise.unit, WorkoutExercise.KG)
    
    def test_workout_exercise_without_weight(self):
        """Test workout exercise creation without weight (bodyweight exercise)."""
        workout_exercise = WorkoutExercise.objects.create(
            workout=self.workout,
            exercise=self.exercise,
            sets=3,
            reps=10
        )
        
        self.assertIsNone(workout_exercise.weight)
        self.assertEqual(workout_exercise.unit, WorkoutExercise.KG)  # Default unit
    
    def test_workout_exercise_unit_choices(self):
        """Test workout exercise unit choices."""
        kg_exercise = WorkoutExercise.objects.create(
            workout=self.workout,
            exercise=self.exercise,
            sets=3,
            reps=10,
            weight=20.0,
            unit=WorkoutExercise.KG
        )
        
        lbs_exercise = WorkoutExercise.objects.create(
            workout=self.workout,
            exercise=self.exercise,
            sets=3,
            reps=10,
            weight=45.0,
            unit=WorkoutExercise.LBS
        )
        
        self.assertEqual(kg_exercise.unit, 'kg')
        self.assertEqual(lbs_exercise.unit, 'lbs')


class WorkoutViewTest(BaseTestCase):
    """Test cases for workout views."""
    
    def test_workout_list_view(self):
        """Test workout list view."""
        response = self.client.get('/workouts/')
        self.assertEqual(response.status_code, 200)
    
    def test_workout_detail_view(self):
        """Test workout detail view."""
        response = self.client.get(f'/workouts/{self.workout.id}/')
        self.assertEqual(response.status_code, 200)
    
    def test_featured_workouts_in_home_view(self):
        """Test that featured workouts appear in home view."""
        # Login user first
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        # Featured workout should be in context
        self.assertIn('featured_workouts', response.context or {})
    
    def test_workout_save_functionality(self):
        """Test workout save/unsave functionality."""
        # Login user first
        self.client.login(username='testuser', password='testpass123')
        
        # Test saving a workout
        response = self.client.post(f'/workouts/save/{self.workout.id}/')
        self.assertEqual(response.status_code, 200)
        
        # Test unsaving a workout
        response = self.client.post(f'/workouts/unsave/{self.workout.id}/')
        self.assertEqual(response.status_code, 200)


class WorkoutFormTest(BaseTestCase, FormTestMixin):
    """Test cases for workout forms."""
    
    def test_valid_workout_form(self):
        """Test valid workout form submission."""
        form_data = {
            'name': 'New Workout',
            'description': 'A new workout routine',
            'difficulty': Workout.INTERMEDIATE,
            'duration': datetime.timedelta(minutes=40),
            'featured': True
        }
        
        form = WorkoutForm(data=form_data)
        self.assert_form_valid(form, should_be_valid=True)
    
    def test_invalid_workout_form(self):
        """Test invalid workout form submission."""
        form_data = {
            'name': '',  # Required field missing
            'description': 'A workout without a name',
            'difficulty': Workout.BEGINNER
        }
        
        form = WorkoutForm(data=form_data)
        self.assert_form_valid(form, should_be_valid=False)
    
    def test_workout_form_duration_validation(self):
        """Test workout form duration validation."""
        form_data = {
            'name': 'Quick Workout',
            'description': 'Very short workout',
            'difficulty': Workout.BEGINNER,
            'duration': datetime.timedelta(seconds=30)  # Very short duration
        }
        
        form = WorkoutForm(data=form_data)
        # This should be valid unless you have custom validation
        self.assert_form_valid(form, should_be_valid=True)
