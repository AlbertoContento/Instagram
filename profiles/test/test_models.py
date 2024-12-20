from django.test import TestCase

from django.contrib.auth.models import User
from profiles.models import UserProfile, Follow

class UserProfileModelTest(TestCase):
    def setUp(self):
        #Crear usuarios y sus perfiles
        self.user1 = User.objects.create_user(
            username="Alberto",
            email="Alberto@hotmail.com",
            password="123456password"
        )

        self.user2 = User.objects.create_user(
            username="Diego",
            email="diego@hotmail.com",
            password="123456password"
        )

        self.profile1 = UserProfile.objects.create(
            user=self.user1,
            bio="Soy informatico",
            birth_date="1993-10-21"
        )

        
        self.profile2 = UserProfile.objects.create(
            user=self.user2,
            bio="Soy camionero",
            birth_date="1992-01-25"
        )

    def test_user_profile_creation(self):
        self.assertEqual(self.profile1.bio, 'Soy informatico')
        self.assertEqual(self.user1, self.profile1.user)
        self.assertEqual(self.user1.username, "Alberto")

    def test_follow_user(self):
        created = self.profile1.follow(self.profile2)
        self.assertTrue(created)
        self.assertTrue(Follow.objects.filter(follower=self.profile1, following=self.profile2).exists())
        created = self.profile1.follow(self.profile2)
        self.assertFalse(created)
        self.assertTrue(Follow.objects.filter(follower=self.profile1, following=self.profile2).exists())

    def test_unfollow_user(self):
        created = self.profile1.follow(self.profile2)
        self.assertTrue(created)
        self.assertTrue(Follow.objects.filter(follower=self.profile1, following=self.profile2).exists())
        self.profile1.unfollow(self.profile2)
        self.assertFalse(Follow.objects.filter(follower=self.profile1, following=self.profile2).exists())

    def test_str_userprofile(self):
            self.assertEqual(str(self.profile1), self.profile1.user.username)


class FollowModelTest(TestCase):
    def setUp(self):
        #Crear usuarios y sus perfiles
        self.user1 = User.objects.create_user(
            username="Alberto",
            email="Alberto@hotmail.com",
            password="123456password"
        )

        self.user2 = User.objects.create_user(
            username="Diego",
            email="diego@hotmail.com",
            password="123456password"
        )

        self.profile1 = UserProfile.objects.create(
            user=self.user1,
            bio="Soy informatico",
            birth_date="1993-10-21"
        )

        
        self.profile2 = UserProfile.objects.create(
            user=self.user2,
            bio="Soy camionero",
            birth_date="1992-01-25"
        )
    
    def test_unique_follow_once_time(self):
        Follow.objects.get_or_create(follower = self.profile1, following = self.profile2)
        self.assertEqual(Follow.objects.filter(follower=self.profile1, following=self.profile2).count(), 1)
        Follow.objects.get_or_create(follower = self.profile1, following = self.profile2)
        self.assertEqual(Follow.objects.filter(follower=self.profile1, following=self.profile2).count(), 1)
