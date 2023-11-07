from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    age = models.FloatField('age', blank=False)


    # Register is simple: They provide user name and password. 

    # Login : Users will provide user name and password. The app will return Bearer token. Verify using that.


    # Integrate User registeration using Console or 