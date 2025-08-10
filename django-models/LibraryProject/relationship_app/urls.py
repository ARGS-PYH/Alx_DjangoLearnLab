from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

import relationship_app.views as views 



urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('register/', views.Register.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    path('admin-page/', views.admin_view, name='admin_view'),
    path('librarian-page/', views.librarian_view, name='librarian_view'),
    path('member-page/', views.member_view, name='member_view'),
]


