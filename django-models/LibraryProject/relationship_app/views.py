from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required


from .models import Book, Library


# Function-based view
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"


class Register(CreateView):
    form_class = UserCreationForm
    template_name = 'relationship_app/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return redirect('list_books')


@user_passes_test(lambda u: u.is_authenticated and u.userprofile.role == 'Admin')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


@user_passes_test(lambda u: u.is_authenticated and u.userprofile.role == 'Librarian')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')


@user_passes_test(lambda u: u.is_authenticated and u.userprofile.role == 'Member')
def member_view(request):
    return render(request, 'relationship_app/member_view.html')



@permission_required('relationship_app.can_add_book')
def add_book_view(request):
    return render(request, 'relationship_app/add_book.html')


@permission_required('relationship_app.can_change_book')
def change_book_view(request):
    return render(request, 'relationship_app/change_book.html')


@permission_required('relationship_app.can_delete_book')
def delete_book_view(request):
    return render(request, 'relationship_app/delete_book.html')
