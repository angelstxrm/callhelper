from django.urls import path
from users.serializers.views import users

urlpatterns = [
    path('users/reg/', users.RegistrationView.as_view(), name='reg'),
    path('users/me/', users.MeView.as_view(), name='me'),
    path('users/change-passwd/', users.ChangePasswordView.as_view(), name='change_passwd'),
]