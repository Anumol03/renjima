from rest_framework import serializers
from .models import *

class CustomUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=False)  # Optional for updates

    class Meta:
        model = CustomUser
        fields = ['id','first_name', 'last_name', 'username', 'email', 'password', 'confirm_password', 'profile_pic']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        # Only validate password and confirm_password if password is provided
        if 'password' in data and 'confirm_password' in data:
            if data['password'] != data['confirm_password']:
                raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)  # Remove confirm_password before saving
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            profile_pic=validated_data.get('profile_pic', None)
        )
        return user

    def update(self, instance, validated_data):
        validated_data.pop('confirm_password', None)  # Remove confirm_password if it exists

        # Update password if it's provided
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])  # Hash the password
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.profile_pic and self.context.get('request'):
            representation['profile_pic'] = self.context['request'].build_absolute_uri(instance.profile_pic.url)
        return representation
    

class CompanySerializer(serializers.ModelSerializer):
    logo = serializers.ImageField()
    image = serializers.ImageField()

    class Meta:
        model = Company
        fields = ['id', 'company_name', 'logo', 'image', 'heading', 'description', 'rating', 'location', 'site', 'phone_number']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        
        # Construct the full URLs for the logo and image
        if representation['logo']:
            representation['logo'] = request.build_absolute_uri(representation['logo'])
        if representation['image']:
            representation['image'] = request.build_absolute_uri(representation['image'])
        
        return representation
    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image','description']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        
        # Build absolute URL for the image field
        if instance.image:
            representation['image'] = request.build_absolute_uri(instance.image.url)
        else:
            representation['image'] = None  # Return None if no image is available

        return representation
    
class ProductSerializer(serializers.ModelSerializer):
    # images = serializers.SerializerMethodField()
    # pdf = serializers.SerializerMethodField()
    company_name = serializers.SerializerMethodField()  # Add a field for company name

    class Meta:
        model = Product
        fields = ['id',
            'title', 'description', 'images','image1','image2','image3' ,'pdf', 'review', 
            'special_feature', 'control_unit', 'category', 'weight', 
            'amputation_level', 'price', 'company_id', 'company_name',  # Include company_name
            'favorites', 'add_to_cart'
        ]

    def get_images(self, obj):
        request = self.context.get('request')
        if obj.images and request:
            return request.build_absolute_uri(obj.images.url)
        return None
    def get_image1(self, obj):
        request = self.context.get('request')
        if obj.image1 and request:
            return request.build_absolute_uri(obj.image1.url)
        return None
    def get_image2(self, obj):
        request = self.context.get('request')
        if obj.image2 and request:
            return request.build_absolute_uri(obj.image2.url)
        return None
    def get_image3(self, obj):
        request = self.context.get('request')
        if obj.image3 and request:
            return request.build_absolute_uri(obj.image3.url)
        return None

    def get_pdf(self, obj):
        request = self.context.get('request')
        if obj.pdf and request:
            return request.build_absolute_uri(obj.pdf.url)
        return None

    def get_company_name(self, obj):
        if obj.company_id is not None:
            try:
                company = Company.objects.get(id=obj.company_id)
                return company.company_name  # Assuming the Company model has a 'name' field
            except Company.DoesNotExist:
                return None  # Return None if the company does not exist
        return None  # Return None if company_id is None
    


class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Favorite
        fields = ['product']

