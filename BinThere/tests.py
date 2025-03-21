from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from BinThere.models import Bin, UserProfile, Vote, Location, BinType
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import get_template
from django.template import Engine

# Create your tests here.

# Ensure 'staticfiles' is registered
engine = Engine.get_default()
engine.template_libraries['staticfiles'] = engine.template_libraries['static']

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        user1 = User.objects.get_or_create(username="user1")[0]

    def test_registration_view(self):
        response = self.client.post(reverse('registration_register'), {
            'username': 'newuser', 'password1': 'securepass', 'password2': 'securepass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newuser').exists())

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


    def test_bin_edit_view(self):
        new_bin_type = BinType.objects.create(name="Glass")
        self.assertTrue(Bin.objects.filter(id=self.bin.id).exists())

        response = self.client.post(reverse('BinThere:edit_bin', args=[self.bin.id]), {
            'bin_types': [new_bin_type.id],  # Ensuring bin_types is included
            'location': self.location.id  # Ensure location is included
        })

        self.assertEqual(response.status_code, 200)  # Expecting redirect

        self.bin.refresh_from_db()
        self.assertIn(new_bin_type, self.bin.bin_types.all())  # Check update


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
        self.assertEqual(response.status_code, 200)
        self.profile.refresh_from_db()
        self.assertIsNotNone(self.profile.picture)
