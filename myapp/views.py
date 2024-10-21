from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
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
def company_create(request):
    serializer = CompanySerializer(data=request.data, context={'request': request})  # Pass request context
    if serializer.is_valid():
        serializer.save()
        return Response({'status':'ok','message':'company created successfully','data':serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def company_list(request):
    companies = Company.objects.all()  # Retrieve all companies
    serializer = CompanySerializer(companies, many=True, context={'request': request})  # Pass request context
    return Response({'status':'ok','message':'company retrieved successfully','data':serializer.data}, status=status.HTTP_200_OK)

@api_view(['PUT'])
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
def company_detail(request, pk):
    try:
        company = Company.objects.get(pk=pk)  # Retrieve the company by ID
    except Company.DoesNotExist:
        return Response({'error': 'Company not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CompanySerializer(company, context={'request': request})  # Serialize the company data
    return Response({'status':'ok','message':'company detail retrieved successfully','data':serializer.data}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def company_delete(request, pk):
    try:
        company = Company.objects.get(pk=pk)  # Retrieve the company by ID
        company.delete()  # Delete the company
        return Response(status=status.HTTP_204_NO_CONTENT)  # Return a 204 No Content response
    except Company.DoesNotExist:
        return Response({'error': 'Company not found.'}, status=status.HTTP_404_NOT_FOUND)
