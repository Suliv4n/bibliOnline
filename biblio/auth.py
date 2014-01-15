from django.conf import settings
from biblio.models import MemberUser
from django.contrib.auth.models import User

class MyBackend(object):
    def authenticate(self, username=None, password=None):
        try:
            u = MemberUser.objects.get(username=username, password=password)
            return u
        except:
            return None


    def get_user(self, user_id):
        try:
            return MemberUser.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None