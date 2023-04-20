from django import forms
from django.forms import ModelForm, CharField, TextInput
from .models import Author, Quote, Tag


class AuthorForm(ModelForm):

    fullname = CharField(min_length=5, max_length=50, required=True, widget=TextInput())

    class Meta:
        model = Author
        fields = ['fullname']


class QuoteForm(ModelForm):
    description = CharField(min_length=10, max_length=500, required=True, widget=TextInput())

    class Meta:
        model = Quote
        fields = ['description']
        exclude = ['authors', 'tags']


class TagForm(ModelForm):
    tag = CharField(min_length=3, max_length=25, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['tag']
