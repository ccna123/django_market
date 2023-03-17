from django.contrib.auth.backends import ModelBackend
from main.models import CustomUser

class CustomUserModelBackend(ModelBackend):
    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None