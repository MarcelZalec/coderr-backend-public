from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class UserProfile(models.Model):
    USER_TYPES = [
        ('customer', 'Customer'),
        ('business', 'Business'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")  # mit User verknüpft (ein user - ein profil)
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/profiles/', default="uploads/profiles/default.jpg")
    location = models.CharField(max_length=255)
    tel = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    working_hours = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=USER_TYPES, default='customer')
    email = models.EmailField(max_length=254)
    created_at = models.DateTimeField(default=now)

    
    def __str__(self):
        return f"{self.user.username} - {self.type}"