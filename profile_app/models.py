from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class UserProfile(models.Model):
    """
    Model representing a user profile.

    Attributes:
    - USER_TYPES (list): Defines available user types ('customer' or 'business').
    - user (OneToOneField): Links the profile to a unique user.
    - username (CharField): Stores the user's username.
    - first_name (CharField): First name of the user.
    - last_name (CharField): Last name of the user.
    - file (FileField): Profile picture or file upload, defaults to a default image.
    - location (CharField): User's location, defaults to 'nicht angegeben' (not specified).
    - tel (CharField): Contact telephone number, defaults to 'nicht angegeben'.
    - description (CharField): User description, defaults to 'nicht angegeben'.
    - working_hours (CharField): Business working hours, defaults to 'nicht angegeben'.
    - type (CharField): Defines the user's role, either 'customer' or 'business'.
    - email (EmailField): Stores the user's email address.
    - created_at (DateTimeField): Timestamp when the profile was created.

    Choices:
    - USER_TYPES: Defines user types ('customer' or 'business').

    Methods:
    - __str__(): Returns a formatted string representation of the user profile.
    """
    USER_TYPES = [
        ('customer', 'Customer'),
        ('business', 'Business'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")  # mit User verknüpft (ein user - ein profil)
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/profiles/', default="uploads/profiles/default.jpg")
    location = models.CharField(max_length=255, default='nicht angegeben')
    tel = models.CharField(max_length=255, default='nicht angegeben')
    description = models.CharField(max_length=255, default='nicht angegeben')
    working_hours = models.CharField(max_length=255, default='nicht angegeben')
    type = models.CharField(max_length=10, choices=USER_TYPES, default='customer')
    email = models.EmailField(max_length=254)
    created_at = models.DateTimeField(default=now)

    
    def __str__(self):
        return f"{self.user.username} - {self.type}"