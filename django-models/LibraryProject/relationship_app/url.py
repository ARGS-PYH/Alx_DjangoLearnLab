from django.contrib import admin
from django.urls import path, include
from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.list_books, name='list_books'),  # FBV
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),  # CBV
]



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('relationship_app.urls')),
]
