from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.contrib.auth import get_user_model

from django.contrib.auth.models import Group, Permission
# Create your models here.

class Author(models.Model):
    lastname = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)


    def __str__(self):
        return self.firstname + " " + self.lastname

class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField("Author", related_name="books")
    subject = models.ForeignKey("Subject")
    comments = models.ManyToManyField("Comment", related_name="comments")

    def __str__(self):
        return self.title

class Subject(models.Model):
    label = models.CharField(max_length = 50)
    def __str__(self):
        return self.label


class Comment(models.Model):
    """
    Commentaire sur un livre posté par un MemberUser.
    """
    user = models.ForeignKey("MemberUser")
    comment = models.TextField()
    date = models.DateField()
    book = models.ForeignKey("Book")

    def __str__(self):
    	return self.comment


class Demander(models.Model):
    """
    Demande d'emprunt
    """
    demandeur = models.ForeignKey("MemberUser", related_name="demandeur")
    to = models.ForeignKey("MemberUser", related_name="cible")
    #c = en cours
    #d = en attente de réponse
    #n = refus
    statut = models.CharField(max_length = 1)
    book = models.ForeignKey("Book")



#-------------------CUSTOM USER-----------------------

class MemberUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        """
        Creates and saves a User with the given username and password.
        """

        if not username:
            raise ValueError('The given username must be set')
        user = MemberUser.objects.create(username=username, password=password)

        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        u = self.create_user(username, password, **extra_fields)
        return u


class MemberUser(User):
    #username = models.CharField(max_length=50, unique=True)
    books = models.ManyToManyField("Book", related_name="users")
    objects = MemberUserManager()

    USERNAME_FIELD = 'username'


    def __str__(self):
        return self.username






#User manager

