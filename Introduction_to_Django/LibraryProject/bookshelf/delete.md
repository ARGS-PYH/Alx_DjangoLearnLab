Get the book
book = Book.objects.get(title="Nineteen Eighty-Four")

Delete the book
book.delete()

Try retrieving books again
from bookshelf.models import Book Book.objects.all()

Output: <QuerySet []>