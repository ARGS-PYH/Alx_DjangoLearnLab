Get the book
book = Book.objects.get(title="1984")

Update the title
book.title = "Nineteen Eighty-Four" book.save()

Confirm the update
book.title

Output: 'Nineteen Eighty-Four'