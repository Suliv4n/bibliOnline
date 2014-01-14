# -*- coding: utf-8 -*-#

# Create your views here.
from biblio.models import Book, Author, Subject, Comment, MemberUser
from django.shortcuts import render_to_response, render

from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.template import RequestContext

from django.contrib.auth import authenticate, login, logout

from biblio.form import *

from tutoriel.shortcuts import render


from django.contrib.auth.decorators import permission_required

"""

class AddAuthorForm(forms.Form):
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField()
"""



def show_main(request):
    con = {}
    con.update(csrf(request))
    return render(
		request,
        "biblio/main.html",
        con)

def show_authors(request):
	return render(
		request,
		"biblio/authors.html",
		{"authors" : Author.objects.order_by("lastname")})

def show_books(request):
	return render(
		request,
		"biblio/books.html",
		{"books" : Book.objects.order_by("title")})

def show_author(request, idAuthor):
	con.update(csrf(request))
	return render(
		request,
		"biblio/author.html",
		{"author" : Author.objects.get(pk=idAuthor)})

def show_book(request, idBook):
	return render(
		request,
		"biblio/book.html",
		{"book" : Book.objects.get(pk=idBook),
		"comments": Comment.objects.get(book=idBook)})


def show_subjects(request):
	return render(
		request,
		"biblio/subjects.html",
		{ "subjects" : Subject.objects.order_by("label")} )


def delete_author(request, idAuthor):
	Author.objects.get(pk=idAuthor).delete()
	return HttpResponseRedirect("/authors/")

"""
def show_addAuthorForm(request):
	form = AddAuthorForm()
	con = {"addAuthor" : form}
	con.update(csrf(request))

	if request.method == 'POST':
			form = AddAuthorForm(request.POST)
			if form.is_valid():
				a = Author(firstname=form["firstname"].value(),lastname=form["lastname"].value())
				a.save()
			return HttpResponseRedirect(
				"authors/")


	return render_to_response(
			"biblio/addAuthor.html" , con , context_instance=RequestContext(request))
"""

@permission_required("biblio.can_edit_database")
def show_addAuthorForm(request):
    form = AuthorForm()
    con={'form':form}
    con.update(csrf(request))
    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES)
        con = {"form" : form}
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
				"authors/")
        else:
            return render_to_response("biblio/addAuthor.html", con, context_instance=RequestContext(request))
    return render_to_response("biblio/addAuthor.html", con, context_instance=RequestContext(request))

@permission_required("biblio.can_edit_database")
def show_addBookForm(request):
    form = BookForm()
    con={'form':form}
    con.update(csrf(request))
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        con = {"form" : form}
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
				"books/")
        else:
            return render_to_response("biblio/addBook.html", con, context_instance=RequestContext(request))
    return render_to_response("biblio/addBook.html", con, context_instance=RequestContext(request))

@permission_required("biblio.can_edit_database")
def show_addSubjectForm(request):
    form = SubjectForm()
    con={'form':form}
    con.update(csrf(request))
    if request.method == 'POST':
        form = SubjectForm(request.POST, request.FILES)
        con = {"form" : form}
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
				"subjects/")
        else:
            return render_to_response("biblio/addSubject.html", con, context_instance=RequestContext(request))
    return render_to_response("biblio/addSubject.html", con, context_instance=RequestContext(request))



def login_page(request):
	con = {}
	con.update(csrf(request))
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password"]
			user = authenticate(username=username,password=password)
			if user is None:
				con["message"] = "Echec de l'authentification."
			elif not user.is_active:
				con["message"] = "Le compte n'est plus actif."
			else:
				login(request, user)
				url = request.GET.get("next","/")
				return HttpResponseRedirect(url)
		else:
			con["message"] = "Paramètres non valides."

	else:
		form = LoginForm()
	con["form"] = form
	return render(request, "biblio/authentification.html", con)

def logout_action(request):
	if request.user.is_authenticated():
		logout(request)
	return HttpResponseRedirect("/authentification")



@permission_required("biblio.can_borrow")
def askfor_action(request, book, to):
    """
    Action qui permet à un utilisateur authentifié de faire une
    demande d'emprunt à un autre utilisateur.
    """
    book = Book.objects.get(pk=book)
    to = User.objects.get(pk=to)


def show_users(request):
    """
    Montrer les users.
    """
    return render(
		request,
		"biblio/users.html",
		{"users" : MemberUser.objects.all()})



def get_author_json(request, pk):
	author = Author.objects.get(pk=pk)
	data = {"firstname" : author.lastname,
			"lastname" : author.firstname}
	import json
	text = json.dumps(data, indent=2, ensure_ascii = False)

	response = HttpResponse(text, mimetype="application/json; charset=utf8")
	return response
