from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import api_view, permission_classes

@api_view(['POST'])
@permission_classes([AllowAny])
def user_registration(request):
    serializer = CustomUserSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({'status':'ok','message':'user created successfully','data':serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])

def user_detail(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)  # Retrieve user by ID
        serializer = CustomUserSerializer(user, context={'request': request})
        return Response({'status':'ok','message':'data retrieved successfully','data':serializer.data})
    except CustomUser.DoesNotExist:
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['PUT'])
def user_edit(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        serializer = CustomUserSerializer(user, data=request.data, partial=True, context={'request': request})  
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'ok','message':'user updated successfully','data':serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except CustomUser.DoesNotExist:
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['DELETE'])
def user_delete(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        user.delete()  # Delete the user
        return Response({'status':'ok','message': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except CustomUser.DoesNotExist:
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        
        # Serialize the user data with request context
        user_data = CustomUserSerializer(user, context={'request': request}).data
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': user_data,  # Include user details
        }, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    


@api_view(['POST'])
@permission_classes([AllowAny])
def company_create(request):
    serializer = CompanySerializer(data=request.data, context={'request': request})  # Pass request context
    if serializer.is_valid():
        serializer.save()
        return Response({'status':'ok','message':'company created successfully','data':serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def company_list(request):
    companies = Company.objects.all()  # Retrieve all companies
    serializer = CompanySerializer(companies, many=True, context={'request': request})  # Pass request context
    return Response({'status':'ok','message':'company retrieved successfully','data':serializer.data}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([AllowAny])
def company_edit(request, pk):
    try:
        company = Company.objects.get(pk=pk)  # Retrieve the company by ID
    except Company.DoesNotExist:
        return Response({'error': 'Company not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CompanySerializer(company, data=request.data, partial=True, context={'request': request})  # Allow partial updates
    if serializer.is_valid():
        serializer.save()
        return Response({'status':'ok','message':'company edit successfully','data':serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def company_detail(request, pk):
    try:
        company = Company.objects.get(pk=pk)  # Retrieve the company by ID
    except Company.DoesNotExist:
        return Response({'error': 'Company not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CompanySerializer(company, context={'request': request})  # Serialize the company data
    return Response({'status':'ok','message':'company detail retrieved successfully','data':serializer.data}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def company_delete(request, pk):
    try:
        company = Company.objects.get(pk=pk)  # Retrieve the company by ID
        company.delete()  # Delete the company
        return Response(status=status.HTTP_204_NO_CONTENT)  # Return a 204 No Content response
    except Company.DoesNotExist:
        return Response({'error': 'Company not found.'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['POST'])  # Only allow POST method
@permission_classes([AllowAny])
def category_create(request):
    serializer = CategorySerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({'status':'ok','message':'category created successfully','data':serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])  # Only allow GET method
@permission_classes([AllowAny])
def category_list(request):
    categories = Category.objects.all()  # Retrieve all categories
    serializer = CategorySerializer(categories, many=True, context={'request': request})  # Serialize the data
    return Response({'status':'ok','message':'data retrived successfully','data':serializer.data})  # Return serialized data

@api_view(['PUT'])  # Allow only PUT method
@permission_classes([AllowAny])
def category_edit(request, pk):
    try:
        category = Category.objects.get(pk=pk)  # Retrieve the category by primary key
    except Category.DoesNotExist:
        return Response({'status': 'error', 'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Deserialize the incoming data to update the category
    serializer = CategorySerializer(category, data=request.data, partial=True, context={'request': request})  # Pass request context
    if serializer.is_valid():  # Validate the data
        serializer.save()  # Save the updated category
        return Response({'status': 'ok', 'message': 'Category updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
    
    return Response({'status': 'error', 'message': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])  # Allow only GET method
@permission_classes([AllowAny])
def category_detail(request, pk):
    try:
        category = Category.objects.get(pk=pk)  # Retrieve the category by primary key
    except Category.DoesNotExist:
        return Response({'status': 'error', 'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CategorySerializer(category, context={'request': request})  # Pass request context
    return Response({'status': 'ok', 'message': 'Category retrieved successfully', 'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(['DELETE'])  # Allow only DELETE method
@permission_classes([AllowAny])
def category_delete(request, pk):
    try:
        category = Category.objects.get(pk=pk)  # Retrieve the category by primary key
        category.delete()  # Delete the category
        return Response({'status': 'ok', 'message': 'Category deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Category.DoesNotExist:
        return Response({'status': 'error', 'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])  # Only allow GET method
@permission_classes([AllowAny])
def list_categories_and_companies(request):
    # Retrieve all categories
    categories = Category.objects.all()
    category_serializer = CategorySerializer(categories, many=True, context={'request': request})
    
    # Retrieve all companies
    companies = Company.objects.all()
    company_serializer = CompanySerializer(companies, many=True, context={'request': request})
    
    # Combine both responses
    return Response({
        'status': 'ok',
        'message': 'Data retrieved successfully',
        'data': {
            'categories': category_serializer.data,
            'companies': company_serializer.data
        }
    }, status=status.HTTP_200_OK)




@api_view(['POST'])
@permission_classes([AllowAny])
def create_product(request, company_id):
    data = request.data.copy()  # Make a mutable copy of the request data

    try:
        # Ensure the company exists
        company = Company.objects.get(id=company_id)
        data['company_id'] = company.id  # Set the company_id for the product
    except Company.DoesNotExist:
        return Response({"error": "Invalid company ID."}, status=status.HTTP_400_BAD_REQUEST)

    # Pass request data to the serializer (request.FILES is automatically handled)
    serializer = ProductSerializer(data=data, context={'request': request})
    if serializer.is_valid():
        product = serializer.save()
        # Serialize the saved product instance
        product_data = ProductSerializer(product, context={'request': request}).data
        return Response({'status': 'ok', 'message': 'Product created successfully', 'data': product_data}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([AllowAny])
def list_products(request, company_id=None):
    if company_id:
        # Filter products by company_id if provided
        products = Product.objects.filter(company_id=company_id)
    else:
        # Get all products if no company_id is provided
        products = Product.objects.all()
    
    # Serialize the products
    serializer = ProductSerializer(products, many=True, context={'request': request})
    
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_products1(request):
    company_id = request.query_params.get('company_id')  # Get company_id from query parameters

    # Filter products by company_id if provided, otherwise retrieve all products
    products = Product.objects.filter(company_id=company_id) if company_id else Product.objects.all()
    
    # Serialize the products
    serializer = ProductSerializer(products, many=True, context={'request': request})
    
    # Return the response with status, message, and serialized data
    return Response({'status': 'ok', 'message': 'Product retrieved successfully', 'data': serializer.data}, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([AllowAny])
def companies_by_category(request, category_id):
    try:
        # Fetch the category details
        category = Category.objects.get(id=category_id)
        category_serializer = CategorySerializer(category, context={'request': request})
        
        # Retrieve all distinct companies with products in the specified category
        company_ids = Product.objects.filter(category_id=category_id).values_list('company_id', flat=True).distinct()
        companies = Company.objects.filter(id__in=company_ids)
        company_serializer = CompanySerializer(companies, many=True, context={'request': request})
        
        # Structure the response to include both category details and company list
        response_data = {
            'status':'ok',
            'message':'retrieved successfully',
            'category': category_serializer.data,
            'companies': company_serializer.data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
@permission_classes([AllowAny])
def products_by_company_and_category(request, category_id, company_id):
    # Filter products by the selected company and category
    products = Product.objects.filter(category_id=category_id, company_id=company_id)
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response({"status":"ok","message":"successfully retrieved","data":serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def product_detail(request, product_id):
    try:
        # Retrieve the product by ID
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    # Serialize the product instance
    serializer = ProductSerializer(product, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_favorite(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # Check if the product is already in the user's favorites
    favorite = Favorite.objects.filter(user=request.user, product=product).first()

    if favorite:
        # If it exists, remove it (unfavorite)
        favorite.delete()
        # Return the product data with favorites set to False
        product.favorites = False
    else:
        # If it doesn't exist, add it to favorites
        Favorite.objects.create(user=request.user, product=product)
        product.favorites = True

    # Serialize the product to return in the response
    product_serializer = ProductSerializer(product, context={'request': request})
    message = "Product removed from favorites" if not product.favorites else "Product added to favorites"
    return Response({"product": product_serializer.data, "message": message}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure only authenticated users can access
def favorite_list(request):
    # Get all favorite products for the authenticated user
    favorites = Favorite.objects.filter(user=request.user)
    
    # Get the corresponding product objects for these favorites
    products = [favorite.product for favorite in favorites]
    
    # Serialize the product data
    product_serializer = ProductSerializer(products, many=True, context={'request': request})
    
    return Response({"favorites": product_serializer.data}, status=status.HTTP_200_OK)
