from knox import views as knox_views
from .views import RegisterAPI 
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import LoginAPI , RegisterAPI , getprofile,updateprofile
urlpatterns = [
    path('register', RegisterAPI.as_view(), name='register'),
    path('login', LoginAPI.as_view(), name='login'),
    path('logout', knox_views.LogoutView.as_view(), name='logout'),
    path('profile', getprofile, name='getprofile'),
    path('profile/update', updateprofile, name='updateprofile'),

]
