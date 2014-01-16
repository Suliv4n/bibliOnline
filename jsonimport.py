#from django.conf.settings import configure
from tutoriel import settings



from biblio.models import Author, Book, Subject, MemberUser
import json


books = json.load(open("biblio/bibliodata/books.json", encoding="utf-8"))
authors = json.load(open("biblio/bibliodata/authors.json", encoding="utf-8"))

author_table = {}

for a in authors:
	author = Author(lastname=a["lastname"], firstname=a["firstname"])
	author.save()
	author_table[str(author)] = author



#cle : libelle subject
#valeur : objet Subject
subjects = {}

for b in books:
	#recuperation du sujet
    s = b["subject"]

    #hydratation du dictionaire de subjects
    if s not in subjects:
        subject = Subject(label = s)
        subject.save()
        subjects[s] = subject

for b in books:
    book = Book(title=b["title"], subject=subjects[s])
    book.save()
    for a in b["authors"]:
        author = author_table[a]
        book.authors.add(author)
    book.save()


#charger les permissions
from django.contrib.auth.models import Permission, User,Group
from django.contrib.contenttypes.models import ContentType


author_content_type = ContentType.objects.get_for_model(Author)

perms = json.load(open("biblio/bibliodata/perms.json", encoding="utf-8"))

dicPerms = {}

for p in perms:
	perm = Permission.objects.create(
		codename = p["codename"],
		name = p["name"],
		content_type=author_content_type)
	perm.save()
	dicPerms[p["codename"]] = perm

groups = json.load(open("biblio/bibliodata/groups.json", encoding="utf-8"))
dicGroups = {}

for g in groups:
	group = Group.objects.create(name=g["name"])
	group.save()
	for p in g["permissions"]:
		group.permissions.add(dicPerms[p])
	group.save()
	dicGroups[g["name"]] = group

users = json.load(open("biblio/bibliodata/users.json", encoding="utf-8"))



for u in users:
	user = MemberUser.objects.create_user(
		username = u["username"],
		password = u["password"])
	user.save()
	for g in u["groups"]:
		user.groups.add(dicGroups[g])
	user.save()

