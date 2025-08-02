from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.PositiveIntegerField()
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

class Library(models.Model):
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book, related_name="library")

    def __str__(self):
        return self.name
    
class Librarian(models.Model):
    name = models.CharField(max_length=200)
    liabrary = models.OneToOneField(
        Library, on_delete=models.CASCADE, related_name="librarians"
    )