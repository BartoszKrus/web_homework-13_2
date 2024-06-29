from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.views.generic import TemplateView, ListView, DetailView
from django.views import View
from django.urls import reverse_lazy

from .models import Author, Quote, Tag

from .forms import AuthorForm, QuoteForm

import requests

from bs4 import BeautifulSoup


class HomeView(TemplateView):
    template_name = 'hw10_app/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = Author.objects.all()
        context['quotes'] = Quote.objects.all()
        return context


class AddAuthorView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = AuthorForm()
        return render(request, 'hw10_app/add_author.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hw10_app:home')
        return render(request, 'hw10_app/add_author.html', {'form': form})


class AddQuoteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = QuoteForm()
        return render(request, 'hw10_app/add_quote.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hw10_app:home')
        return render(request, 'hw10_app/add_quote.html', {'form': form})


class ScrapeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'hw10_app/scrape.html')

    def post(self, request, *args, **kwargs):
        base_url = 'http://quotes.toscrape.com'
        page_number = 1

        while True:
            url = f'{base_url}/page/{page_number}/'
            response = requests.get(url)
            
            if response.status_code != 200:
                break
            
            soup = BeautifulSoup(response.text, 'html.parser')
            quotes_to_scrape = soup.find_all('div', class_='quote')
            for quote in quotes_to_scrape:
                quote_text = quote.find('span', class_='text').get_text()
                author_name = quote.find('small', class_='author').get_text()
                
                tags_meta = quote.find('meta', itemprop='keywords')
                if tags_meta:
                    tags = tags_meta['content'].split(',')
                else:
                    tags = []

                author, created = Author.objects.get_or_create(name=author_name)
                quote_obj, created = Quote.objects.get_or_create(text=quote_text, author=author)

                for tag_name in tags:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    quote_obj.tags.add(tag)

            next_page = soup.find('li', class_='next')
            if next_page:
                page_number += 1
            else:
                break
        
        return render(request, 'hw10_app/scrape.html')


class AuthorListView(ListView):
    model = Author
    template_name = 'hw10_app/author_list.html'
    context_object_name = 'authors'
    paginate_by = 10


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'hw10_app/author_detail.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quotes'] = Quote.objects.filter(author=self.object)
        return context
    

class QuoteListView(ListView):
    model = Quote
    template_name = 'hw10_app/quote_list.html'
    context_object_name = 'quotes'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_tags'] = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
        return context
    

class QuotesByTagView(ListView):
    model = Quote
    template_name = 'hw10_app/quotes_by_tag.html'
    context_object_name = 'quotes'
    paginate_by = 10

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, name=self.kwargs['tag_name'])
        return Quote.objects.filter(tags=self.tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context