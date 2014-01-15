from django.conf import settings
from biblio.models import MemberUser
from django.contrib.auth.models import User

class MyBackend(object):
    def authenticate(self, username=None, password=None):
        u = MemberUser.objects.get(username=username, password=password)
        if u is None:
            u = user.objects.get(username=username, password=password)
        return u


    def get_user(self, user_id):
        try:
            return MemberUser.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None