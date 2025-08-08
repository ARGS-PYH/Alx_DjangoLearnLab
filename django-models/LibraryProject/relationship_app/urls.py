from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

import relationship_app.views as views 


urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('login/',auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('register/', views.Register.as_view(), name='register' ),
    path('logout/',auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name ='logout')
]
