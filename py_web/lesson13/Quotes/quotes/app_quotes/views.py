from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from .forms import AuthorForm, QuoteForm, TagForm
from .models import Author, Quote, Tag


# Create your views here.


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'app_quotes/author_detail.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quotes = Quote.objects.filter(author=self.object).all()
        context['quotes'] = quotes
        return context


def main(request):
    quotes = Quote.objects.all()
    return render(request, 'app_quotes/index.html', {"quotes": quotes,
                                                     "title": "Quotes:",
                                                     })


@login_required
def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            new_author = form.save(commit=False)
            new_author.user = request.user
            new_author.save()
            return redirect(to='app_quotes:root')
        else:
            return render(request, 'app_quotes/author.html', {'form': form})

    return render(request, 'app_quotes/author.html', {'form': AuthorForm()})


@login_required
def quote(request):
    authors = Author.objects.all()
    tags = Tag.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.user = request.user
            choice_aut = Author.objects.filter(fullname__in=request.POST.getlist('authors'))
            new_quote.author = choice_aut.first()
            new_quote.save()
            choice_tag = Tag.objects.filter(tag__in=request.POST.getlist('tags'))
            for tag_ in choice_tag.iterator():
                new_quote.tag.add(tag_)
            new_quote.save()

            return redirect(to='app_quotes:root')
        else:
            return render(request, 'app_quotes/quote.html', {"authors": authors, 'form': form, "tags": tags})

    return render(request, 'app_quotes/quote.html', {"authors": authors, 'form': QuoteForm(), "tags": tags})


@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag_ = form.save(commit=False)
            tag_.user = request.user
            tag_.save()
            return redirect(to='app_quotes:root')
        else:
            return render(request, 'app_quotes/tag.html', {'form': form})

    return render(request, 'app_quotes/tag.html', {'form': TagForm()})
