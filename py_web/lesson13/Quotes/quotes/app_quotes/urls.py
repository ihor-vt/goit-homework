from django.contrib import admin
from django.urls import path
from . import views
from .views import AuthorDetailView

app_name = "app_quotes"

urlpatterns = [
    path("", views.main, name="root"),
    path('author/', views.author, name='author'),
    path('quote/', views.quote, name='quote'),
    path('tag/', views.tag, name='tag'),
    path('author/<int:pk>/', AuthorDetailView.as_view(), name='author_detail'),
]
