from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    def __str__(self):
        return self.username
    
class Company(models.Model):
    company_name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='company_logos/')  # Path where logo images will be stored
    image = models.ImageField(upload_to='company_images/')  # Path for additional images
    heading = models.CharField(max_length=255)
    description = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2)  # Allows ratings like 4.5
    location = models.CharField(max_length=255)
    site = models.URLField(max_length=255)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.company_name