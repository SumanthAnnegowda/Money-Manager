from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import RegisterUser, Login, Logout


urlpatterns = [
    path('students/register/', RegisterUser.as_view(),name='register-user'),
    path('students/login/', Login.as_view(), name='login'),
    path('students/logout/', Logout.as_view(),name='logout'),
]

urlpatterns = format_suffix_patterns(urlpatterns)