from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import UserManager


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })

    USERNAME_FIELD = "email"

    STUDENT = 1
    INSTRUCTOR = 2
    COUNSELLOR =3
      
    ROLE_CHOICES = (
          (STUDENT, 'Student'),
          (INSTRUCTOR, 'Instructor'),
          (COUNSELLOR, 'Counsellor'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=1)
      
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    objects = UserManager()


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE ,related_name='profile')

    avatar = models.ImageField(default='avatar.png', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username