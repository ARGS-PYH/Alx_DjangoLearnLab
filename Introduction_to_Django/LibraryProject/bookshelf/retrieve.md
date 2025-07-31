Retrieve the book
book = Book.objects.get(title="1984")

Display book attributes
book.title # Output: '1984' book.author # Output: 'George Orwell' book.publication_year # Output: 1949 ß