from django.forms import ModelForm, Form, CharField, PasswordInput
from biblio.models import Author, Book, Subject



class AuthorForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(AuthorForm, self).__init__(*args, **kwargs)
		self.fields['lastname'].label = "Last name"
		self.fields['firstname'].label = "First name"
	class Meta:
		model = Author
		fields = ['lastname', 'firstname']

class BookForm(ModelForm):
		def __init__(self, *args, **kwargs):
			super(BookForm, self).__init__(*args, **kwargs)
			self.fields['title'].label = "Title"
			self.fields['authors'].label = "Authors"
			self.fields['subject'].label = "Subject"
		class Meta:
			model = Book
			fields = ['title', 'authors', 'subject']

class SubjectForm(ModelForm):
		def __init__(self, *args, **kwargs):
			super(SubjectForm, self).__init__(*args, **kwargs)
			self.fields['label'].label = "Label"
		class Meta:
			model = Subject
			fields = ['label']



class LoginForm(Form):
	username = CharField(max_length=100)
	password = CharField(max_length=100, widget=PasswordInput)
	

