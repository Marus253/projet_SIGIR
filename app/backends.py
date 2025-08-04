# backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from .models import Usager

UserModel = get_user_model()

class TelephoneBackend(BaseBackend):
    def authenticate(self, request, telephone=None, password=None, **kwargs):
        try:
            usager = Usager.objects.select_related('user').get(telephone=telephone)
            user = usager.user
            if user.check_password(password):
                return user
        except Usager.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
