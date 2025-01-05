from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.UserRegister.as_view(), name="register"), #-> Register User
    path('verify/', views.UserVerification.as_view(), name="verify"), #-> Verify User
    path('login/', views.LoginUser.as_view(), name="login"), #-> Login User
    path('create_post/', views.CreatePost.as_view(), name="create_post"), #-> Create Post
    path('post_list/', views.GetAllPost.as_view(), name='all_post'), #-> Get all post
    path('post/', views.GetUniquePost.as_view(), name="post"), #-> Get unique post
    path('update/', views.UpdatePost.as_view(), name='update'), #-> Update post
    path('delete/', views.DeletePost.as_view(), name="delete"), #-> Delete post
    path('refresh/', views.RefreshAccessToken.as_view(), name="refresh"), #-> Refresh token
]
