from django.urls import path
from users.serializers.views import users

urlpatterns = [
    path('users/reg/', users.RegistrationView.as_view(), name='reg')
]