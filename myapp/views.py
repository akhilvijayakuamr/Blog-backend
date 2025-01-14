from django.shortcuts import render
from rest_framework.views import APIView
from .models import CustomUser, Post
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserSerializer, LoginUserSerializer, AllPostSerializer
from .email import send_otp_mail
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed
from datetime import datetime
from .auth import is_token_expired


# Create your views here.



# user register


class UserRegister(APIView):
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        first_name = request.data.get("firstname")
        last_name = request.data.get("lastname")
        password = request.data.get("password")
        confirmpassword = request.data.get("confirmpassword")
        
        if CustomUser.objects.filter(email=email).exists():
            return Response({"message":"Email already exist"},status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(username=username).exists():
            return Response({"message":"Email already exist"},status=status.HTTP_400_BAD_REQUEST)
        if (password!=confirmpassword):
            return Response({"message":"Passwords do not match"},status=status.HTTP_400_BAD_REQUEST)
            
        
        data ={
            'username':username,
            'password':password,
            'first_name':first_name,
            'last_name':last_name, 
            'email':email
            }
        serializer = CustomUserSerializer(data=data)
    
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()

            send_otp_mail(serializer.data['email'])

            return Response({"message":"Registration Successfully Plese check your email for conformation"}, status=status.HTTP_201_CREATED)
        except:
            return Response(
                {"message": "User is not created"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
            
# Verification

class UserVerification(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")
        if(email):
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({"message":"User not found"}, status=status.HTTP_400_BAD_REQUEST)
            if(otp):
                if(user.otp==otp):
                    user.is_verified = True
                    user.save()
                    return Response({"message":"Verification Successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message":"Verification Unsuccessfuly"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message":"Verification Unsuccessfuly"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"Verification Unsuccessfuly"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
# Login user


class LoginUser(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginUserSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            user = authenticate(email=email, password=password)
            if(user is None):
                return Response({"message":"User does not exist"}, status=status.HTTP_404_NOT_FOUND)
            refresh = RefreshToken.for_user(user)

            return Response( {
                'email':user.email,
                'userId':str(user.id),
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message':"Login Successfully"
            }, status=status.HTTP_201_CREATED)
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
        
# Create Post


class CreatePost(APIView):
    def post(self, request):
        if is_token_expired(request):
            return Response({"message":"User does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
        user_id = request.data.get('id')
        title = request.data.get('title')
        description = request.data.get('description')
        image = request.FILES.get('image')
        try:
            user = CustomUser.objects.get(id=int(user_id))
            post = Post(user=user,
                        title = title,
                        description = description,
                        image=image         
                        )
            post.save()
            return Response({"message":"Post created successfullly"}, status=status.HTTP_201_CREATED)
            
        except CustomUser.DoesNotExist:
            return Response({"message":"User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        
# Get all post
        
class GetAllPost(APIView):

    def post(self, request):
        print("is working")
        if is_token_expired(request):
            return Response({"message":"User does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
        id = request.data.get('userId')
        try:
            user = CustomUser.objects.get(id=int(id))
        except CustomUser.DoesNotExist:
             return Response({"message":"User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        try:
            posts = Post.objects.all()
            serializer = AllPostSerializer(posts, many=True)
            return Response({
            "posts": serializer.data
        }, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
             return Response({"message":"No posts"}, status=status.HTTP_404_NOT_FOUND)
        
            


# Get unique post

class GetUniquePost(APIView):
    def post(self, request):
        if is_token_expired(request):
            return Response({"message":"User does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
        postId = request.data.get('postId')
        try:
            post = Post.objects.filter(id=int(postId)).first()
            serializer = AllPostSerializer(post) 
            return Response({
            "posts": serializer.data
            }, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
             return Response({"message":"No posts"}, status=status.HTTP_404_NOT_FOUND)
         
         


# update Post


class UpdatePost(APIView):
    def post(self, request):
        if is_token_expired(request):
            return Response({"message":"User does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
        user_id = request.data.get('id')
        title = request.data.get('title')
        description = request.data.get('description')
        image = request.FILES.get('image')
        post_id = request.data.get('postId')
        
        try:
            post = Post.objects.filter(id=int(post_id)).first()
            if title:
                post.title = title
            if description:
                post.description = description
            if image:
                post.image = image
            post.save()
            return Response({"message":"Update successfullly",
                             "postId":str(post.id)
                             }, status=status.HTTP_201_CREATED)
        except CustomUser.DoesNotExist:
             return Response({"message":"No posts"}, status=status.HTTP_404_NOT_FOUND)
                        
        
        
# Delete Post

class DeletePost(APIView):
    
    def post(self, request):
        if is_token_expired(request):
            return Response({"message":"User does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
        postId = request.data.get('postId')
        try:
            post = Post.objects.get(id=int(postId))
            post.delete()
            return Response({"message":"Delete successfullly"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"message":"No posts"}, status=status.HTTP_404_NOT_FOUND)
        
      
# Refresh token      
        
class RefreshAccessToken(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({"message": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
            refresh = RefreshToken(refresh_token)
            exp_timestamp = refresh['exp']
            current_timestamp = datetime.utcnow().timestamp()
        
            if exp_timestamp < current_timestamp:
                return Response({"message": "Refresh token has expired."}, status=status.HTTP_401_UNAUTHORIZED)

            new_access_token = str(refresh.access_token)
            return Response({
                "access": new_access_token,
                "message": "Access token refreshed successfully."
            }, status=status.HTTP_200_OK)

        except TokenError as e:
            return Response({"message": f"Invalid refresh token: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        

                
                
        
        
        
