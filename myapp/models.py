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
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='categories/')  # Adjust the upload_to path as needed
    description=models.CharField(max_length=300,null=True,blank=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    images = models.ImageField(upload_to='products/images/', blank=True, null=True)
    image1=models.ImageField(upload_to='products/images/',blank=True,null=True)
    image2=models.ImageField(upload_to='products/images/',blank=True,null=True)
    image3=models.ImageField(upload_to='products/images/',blank=True,null=True)
    pdf = models.FileField(upload_to='products/pdfs/', blank=True, null=True)
    review = models.TextField(blank=True, null=True)
    
    special_feature = models.TextField(blank=True, null=True)
    control_unit = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    amputation_level = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    company_id=models.IntegerField(null=True,blank=True)
    favorites=models.BooleanField(default=False)
    add_to_cart=models.BooleanField(default=False)
    maximum_price=models.IntegerField(null=True,blank=True)
    minimum_price=models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.title
    

class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')
    

    def __str__(self):
        return f"{self.user} - {self.product.title}"

