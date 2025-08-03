import os
import django
from relationship_app.models import Author, Book, Library, Librarian
# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()




#  Query all books by a specific author
def books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        print(f"Books by {author.name}:")
        for book in books:
            print(f"- {book.title}")
    except Author.DoesNotExist:
        print("Author not found.")


#  List all books in a library
def books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in {library.name}:")
        for book in books:
            print(f"- {book.title}")
    except Library.DoesNotExist:
        print("Library not found.")


# Retrieve the librarian for a library
def librarian_of_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        print(f"Librarian of {library.name}: {librarian.name}")
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        print("Library or Librarian not found.")