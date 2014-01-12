from django.db import models


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

    def __str__(self):
        return self.title

class Subject(models.Model):
    label = models.CharField(max_length = 50)
    def __str__(self):
        return self.label


class Comment(models.Model):
	#user = models.ForeignKey("User")
	comment = models.TextField()
	date = models.DateField()
	book = models.ForeignKey("Book")

	def __str__(self):
		return self.label

