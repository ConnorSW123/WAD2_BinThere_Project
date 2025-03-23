from django.test import TestCase, Client
from django.urls import reverse
from BinThere.models import Bin, UserProfile, Vote, Location, BinType
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.template import Engine
from BinThere.apps import BinthereConfig
from BinThere.forms import BinForm
from django.test import TestCase
from unittest.mock import patch
import manage  # Import the manage.py script
from population_script import populate  # Adjust import based on actual script name

# Create your tests here.
# All Files are fully Tested except from Reverse Rendering Statements and Javascript/HTML Reliant View Functionality.

# Ensure 'staticfiles' is registered
engine = Engine.get_default()
engine.template_libraries['staticfiles'] = engine.template_libraries['static']



class AppConfigTest(TestCase):
    def test_app_config(self):
        # Check if the name of the app is 'BinThere'
        self.assertEqual(BinthereConfig.name, 'BinThere') 




class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_view(self):
        response = self.client.post(reverse('auth_login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in self.client.session)

class BinManagementTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.location = Location.objects.create(name='Campus', latitude=55.86515, longitude=-4.25763)
        self.bin_type = BinType.objects.create(name="Plastic")  # Creating a bin type
   
        # Corrected Bin creation (without name)
        self.bin = Bin.objects.create(location=self.location, added_by=self.user)
        self.bin.bin_types.add(self.bin_type)  # Ensure bin_types are assigned


    def test_bin_list_view(self):
        response = self.client.get(reverse('BinThere:bin_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.location.name)  # Checks if the location name appears
    
    def test_bin_creation_view(self):
        response = self.client.post(reverse('BinThere:add_bin'), {
            'location': self.location.id,
            'bin_types': [self.bin_type.id],  
            'added_by': self.user.id,
        })

        # Ensure the view redirects upon successful form submission
        self.assertEqual(response.status_code, 200)

        # Ensure a new bin has been created
        self.assertTrue(Bin.objects.filter(location=self.location, added_by=self.user).exists())


    
            
    def test_bin_delete_view(self):
        response = self.client.post(reverse('BinThere:delete_bin', args=[self.bin.id]))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(ObjectDoesNotExist):
            Bin.objects.get(id=self.bin.id)

class VotingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.location = Location.objects.create(name='Library', latitude=55.8665, longitude=-4.2504)
        self.bin_type = BinType.objects.create(name="General")  # Creating a bin type
        self.bin = Bin.objects.create(location=self.location, added_by=self.user)
        self.bin.bin_types.add(self.bin_type)

    def test_upvote_bin(self):
        response = self.client.post(reverse('BinThere:vote_bin', args=[self.bin.id, 1]))  # 1 for upvote
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Vote.objects.filter(bin=self.bin, user=self.user, vote=1).count(), 1)

    def test_downvote_bin(self):
        response = self.client.post(reverse('BinThere:vote_bin', args=[self.bin.id, 0]))  # 0 for downvote
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Vote.objects.filter(bin=self.bin, user=self.user, vote=0).count(), 1)

class UserProfileTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = UserProfile.objects.create(user=self.user, website='https://example.com')
       

    def test_user_profile_view(self):
        self.client.login(username='testuser', password='testpassword')  # Ensure user is logged in
        response = self.client.get(reverse('BinThere:profile', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'https://example.com')

    def test_profile_picture_upload(self):
        url = reverse('BinThere:profile', args=[self.user.username])  # Corrected URL variable
        with open('media/profile_images/default1.jpg', 'rb') as img:
            self.client.post(url, {'profile_picture': img})
        response = self.client.get(reverse('BinThere:profile', args=[self.user.username]))
        self.assertEqual(response.status_code, 302)
        self.profile.refresh_from_db()
        self.assertIsNotNone(self.profile.picture)


class BinFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.location = Location.objects.create(name='Library', latitude=55.8665, longitude=-4.2504)
        self.bin_type = BinType.objects.create(name="Plastic")
        self.client.login(username='testuser', password='testpassword')


    def test_create_bin_without_location(self):
        # We expect this to raise a TypeError because the form cannot create a bin without a location.
        with self.assertRaises(TypeError):
            self.client.post(reverse('BinThere:add_bin'), {
                'existing_bin': '',  # No existing bin selected
                'location_name': '',  # No location provided
                'latitude': None,  # Missing latitude for a new bin
                'longitude': None,  # Missing longitude for a new bin
                'bin_types': [self.bin_type.id]
            })




class BinFormValidationTests(TestCase):
    def setUp(self):
        # Create user to assign 'added_by' field properly in tests
        self.user = User.objects.create_user(username="testuser", password="password")
        self.location = Location.objects.create(
            name="Campus", latitude=55.86515, longitude=-4.25763
        )
        self.bin_type = BinType.objects.create(name="Plastic")
        self.bin = Bin.objects.create(location=self.location, added_by=self.user)  # Ensure 'added_by' is set

    def test_existing_bin_with_location_should_fail(self):
        """Test if selecting an existing bin and providing a new location raises a ValidationError"""
        form_data = {
            'existing_bin': self.bin,  # Existing bin selected
            'location_name': "New Location",  # New location provided
            'latitude': 55.86515,
            'longitude': -4.25763,
            'bin_types': [self.bin_type.id]
        }
        form = BinForm(data=form_data)
        self.assertFalse(form.is_valid())  # Form should be invalid
       

    def test_no_existing_bin_and_no_location_should_fail(self):
        """Test if not selecting an existing bin and missing location raises a ValidationError"""
        form_data = {
            'existing_bin': None,  # No existing bin selected
            'location_name': "",  # No location name provided
            'latitude': None,  # No latitude provided
            'longitude': None,  # No longitude provided
            'bin_types': [self.bin_type.id]
        }
        form = BinForm(data=form_data)
        self.assertFalse(form.is_valid())  # Form should be invalid


    def test_posted_no_existing_bin(self):
        """Test if not selecting an existing bin and providing location details passes validation"""
        form_data = {
            'existing_bin': None,  # No existing bin selected
            'location_name': "New Location",  # Location name provided
            'latitude': 55.86515,
            'longitude': -4.25763,
            'bin_types': [self.bin_type.id]
        }
        form = BinForm(data=form_data)
        self.assertFalse(form.is_valid())  # Form should not be valid

    def test_existing_bin_posted_without_location(self):
        """Test if selecting an existing bin without location details passes validation"""
        form_data = {
            'existing_bin': self.bin,  # Existing bin selected
            'location_name': "",  # No new location provided
            'latitude': None,
            'longitude': None,
            'bin_types': [self.bin_type.id]
        }
        form = BinForm(data=form_data)
        self.assertFalse(form.is_valid())  # Form should not be valid

    def test_missing_added_by_field_should_fail(self):
        """Test if trying to create a bin without setting the 'added_by' field raises IntegrityError"""
        form_data = {
            'existing_bin': None,  # No existing bin selected
            'location_name': "New Location",  # Location name provided
            'latitude': 55.86515,
            'longitude': -4.25763,
            'bin_types': [self.bin_type.id]
        }
        form = BinForm(data=form_data)
        # The form should fail to save and raise the ValueError
        self.assertFalse(form.is_valid())  # This should not be valid.



    def test_existing_bin_with_location_validation_error(self):
        """Test that the validation error is raised when an existing bin and new location are selected together"""
        form_data = {
            'existing_bin': self.bin,  # Select an existing bin
            'location_name': "New Location",  # Provide a new location name
            'latitude': 55.86515,
            'longitude': -4.25763,
            'bin_types': [self.bin_type.id]  # Valid bin type
        }

        form = BinForm(data=form_data)






class ModelTests(TestCase):

    def test_user_profile_str(self):
        """Test the __str__ method of UserProfile"""
        # Create a user
        user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a UserProfile for the user
        profile = UserProfile.objects.create(user=user, website="https://example.com", picture="profile_pic.jpg")

        # Check if the __str__ method returns the correct username
        self.assertEqual(str(profile), 'testuser')

    def test_location_str(self):
        """Test the __str__ method of Location"""
        # Create a Location instance
        location = Location.objects.create(name="Campus", latitude=55.86515, longitude=-4.25763)

        # Check if the __str__ method returns the correct location name
        self.assertEqual(str(location), 'Campus')

    def test_vote_str(self):
        """Test the __str__ method of Vote"""
        # Create a user
        user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a bin 
        loc1 = Location.objects.get_or_create(name="Test Location", latitude="55.8780", longitude="-4.2900")[0]
        bin1 = Bin.objects.get_or_create(location=loc1, added_by=user, upvotes=5, downvotes=2)[0]


        # Create a Vote instance
        vote = Vote.objects.create(bin=bin1, user=user, vote=1)  # Upvote

        # Check if the __str__ method returns the correct string format - Spacing is Neccessary
        self.assertEqual(str(vote), 'testuser voted 1 on  Bin at Test Location')



class URLSTests(TestCase):

    def setUp(self):
        """Set up test user for registration"""
        self.user_data = {
            'username': 'testuser',
            'password1': 'securepassword',
            'password2': 'securepassword',
            'email': 'testuser@example.com',
            # If location is part of the registration form, add the following:
        }
        self.registration_url = reverse('BinThere:register')  # URL to the registration view

    def test_registration_and_redirect(self):
        """Test that after registration, the user is directed to the correct page"""

        # Simulate a POST request to register a user
        response = self.client.post(self.registration_url, self.user_data)

        # Check if the response status code is 200 (indicating the registration page)
        self.assertEqual(response.status_code, 200)

class AdminScriptTests(TestCase):

    @patch("django.core.management.execute_from_command_line", side_effect=ImportError("Couldn't import Django"))
    def test_import_error_when_django_not_installed(self, mock_execute):
        """Test that ImportError is raised if Django is not installed or virtual environment is not activated."""

        with self.assertRaises(ImportError) as context:
            manage.main()  # Call main() from manage.py

        self.assertIn("Couldn't import Django", str(context.exception))


class PopulationScriptTests(TestCase):

    def setUp(self):
        """Run the population script before each test"""
        populate()

    def test_users_created(self):
        """Test that users were created successfully"""
        self.assertTrue(User.objects.filter(username="user1").exists())
        self.assertTrue(User.objects.filter(username="user2").exists())
        self.assertTrue(User.objects.filter(username="user3").exists())


   
    def test_user_profiles_created(self):
        """Test that user profiles exist for created users"""
        for user in User.objects.all():
            self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_locations_created(self):
        """Test that expected locations are in the database"""
        expected_locations = [
            "University of Glasgow", "Kelvingrove Park", "Botanic Gardens",
            "Glasgow Cathedral", "The Hunterian", "Clyde Auditorium"
        ]
        for location_name in expected_locations:
            self.assertTrue(Location.objects.filter(name=location_name).exists())

    def test_bin_types_created(self):
        """Test that bin types were correctly created"""
        expected_bin_types = [
            "Batteries", "Cardboard", "Food and Drink Cans", "Food Waste",
            "General", "Metal", "Mixed Glass", "Paper", "Plastic Bottles",
            "Soft Plastic", "Textiles"
        ]
        for bin_type in expected_bin_types:
            self.assertTrue(BinType.objects.filter(name=bin_type).exists())

    def test_bins_created(self):
        """Test that bins were correctly created and linked to locations"""
        self.assertGreaterEqual(Bin.objects.count(), 6)  # Ensure at least 6 bins exist
        for bin in Bin.objects.all():
            self.assertIsNotNone(bin.location)
            self.assertGreaterEqual(bin.bin_types.count(), 1)  # Each bin should have at least one bin type

    def test_votes_created(self):
        """Test that votes were assigned correctly"""
        self.assertGreaterEqual(Vote.objects.count(), 5)  # Ensure at least 5 votes exist
        for vote in Vote.objects.all():
            self.assertIsNotNone(vote.user)
            self.assertIsNotNone(vote.bin)
            self.assertIn(vote.vote, [-1, 1])  # Ensure only valid vote values

    def test_no_duplicate_entries(self):
        """Test that the population script does not create duplicate entries"""
        populate()  # Run the script again
        self.assertEqual(User.objects.filter(username="user1").count(), 1)  # User should still be unique
        self.assertEqual(Location.objects.filter(name="University of Glasgow").count(), 1)  # Location should be unique



class HomeViewTest(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse('BinThere:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'BinThere/home.html')


class BinMapViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='password')

        # Create a bin and bin types for the context
        location = Location.objects.create(name='Test Location', latitude=12.34, longitude=56.78)
        bin_type = BinType.objects.create(name='Test Bin Type')
        Bin.objects.create(location=location, added_by = user, upvotes=0, downvotes=0)
    
    def test_bin_map_view(self):
        response = self.client.get(reverse('BinThere:bin_map'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'BinThere/map.html')
        self.assertIn('bin_data', response.context)
        self.assertIn('bin_types', response.context)


class VoteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='password')
        location = Location.objects.create(name='Test Location', latitude=12.34, longitude=56.78)
        bin_type = BinType.objects.create(name='Test Bin Type')
        cls.bin = Bin.objects.create(location=location, added_by=user, upvotes=0, downvotes=0)
        cls.user = user

    def test_vote_upvote(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('BinThere:vote_bin', kwargs={'bin_id': self.bin.id, 'vote_type': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'message': 'Vote recorded.', 'upvotes': 1, 'downvotes': 0})

    def test_vote_downvote(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('BinThere:vote_bin', kwargs={'bin_id': self.bin.id, 'vote_type': 0}))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'message': 'Vote recorded.', 'upvotes': 0, 'downvotes': 1})

    def test_toggle_vote(self):
        self.client.login(username='testuser', password='password')
        self.client.post(reverse('BinThere:vote_bin', kwargs={'bin_id': self.bin.id, 'vote_type': 1}))
        response = self.client.post(reverse('BinThere:vote_bin', kwargs={'bin_id': self.bin.id, 'vote_type': 0}))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'message': 'Vote recorded.', 'upvotes': 0, 'downvotes': 1})

    def test_invalid_vote_type(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('BinThere:vote_bin', kwargs={'bin_id': self.bin.id, 'vote_type': 999}))
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {"error": "Invalid vote type."})


class RegisterProfileViewTest(TestCase):
    def test_register_profile_view_get(self):
        response = self.client.get(reverse('BinThere:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'BinThere/profile_registration.html')

    def test_register_profile_view_post_valid(self):
        user_data = {'username': 'testuser', 'email': 'testuser@example.com', 'password1': 'password', 'password2': 'password'}
        profile_data = {'bio': 'Test bio'}
        response = self.client.post(reverse('BinThere:register'), data={**user_data, **profile_data})
        self.assertEqual(response.status_code, 200)  # successful registration

    def test_register_profile_view_post_invalid(self):
        user_data = {'username': 'testuser', 'email': 'testuser@example.com', 'password1': 'password', 'password2': 'wrongpassword'}
        profile_data = {'bio': 'Test bio'}
        response = self.client.post(reverse('BinThere:register'), data={**user_data, **profile_data})
        self.assertEqual(response.status_code, 200)


class ProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='password')
        UserProfile.objects.create(user=user)
        cls.user = user

    def test_profile_view_get(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('BinThere:profile', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'BinThere/profile.html')

    def test_profile_view_post_valid(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('BinThere:profile', kwargs={'username': 'testuser'}), {'bio': 'Updated bio'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('BinThere:profile', kwargs={'username': 'testuser'}))

    def test_profile_view_post_invalid(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('BinThere:profile', kwargs={'username': 'testuser'}), {'bio': ''})
        self.assertEqual(response.status_code, 302)


class BinCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='password')
        location = Location.objects.create(name='Test Location', latitude=12.34, longitude=56.78)
        cls.bin_type = BinType.objects.create(name='Test Bin Type')
        cls.user = user
        cls.location = location

    def test_bin_create_view_get(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('BinThere:add_bin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'BinThere/add_bin.html')

    def test_bin_create_view_post_valid(self):
        self.client.login(username='testuser', password='password')
        data = {'location_name': 'Test Location', 'latitude': 12.34, 'longitude': 56.78, 'bin_types': [self.bin_type.id]}
        response = self.client.post(reverse('BinThere:add_bin'), data)
        self.assertEqual(response.status_code, 200)  # Should Return 200 after successful creation

    def test_bin_create_view_post_invalid(self):
        self.client.login(username='testuser', password='password')
        data = {'location_name': '', 'latitude': '', 'longitude': '', 'bin_types': []}
        response = self.client.post(reverse('BinThere:add_bin'), data)
        self.assertEqual(response.status_code, 200)



class BinDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='password')
        location = Location.objects.create(name='Test Location', latitude=12.34, longitude=56.78)
        cls.bin_type = BinType.objects.create(name='Test Bin Type')
        cls.bin = Bin.objects.create(location=location, upvotes=0, downvotes=0, added_by=user)
        cls.user = user

    def test_bin_delete_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.delete(reverse('BinThere:delete_bin', kwargs={'pk': self.bin.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('BinThere:bin_list'))

    def test_bin_delete_view_permission_denied(self):
        # Create a new user with no permission to delete the bin
        user = User.objects.create_user(username='otheruser', password='password')
        self.client.login(username='otheruser', password='password')
        response = self.client.delete(reverse('BinThere:delete_bin', kwargs={'pk': self.bin.id}))
        self.assertEqual(response.status_code, 404)














    




