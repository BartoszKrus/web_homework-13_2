from django.urls import path

from .views import HomeView, AddAuthorView, AddQuoteView, ScrapeView, AuthorListView, AuthorDetailView, QuoteListView, QuotesByTagView

app_name = 'hw10_app'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('add_author/', AddAuthorView.as_view(), name='add_author'),
    path('add_quote/', AddQuoteView.as_view(), name='add_quote'),
    path('scrape/', ScrapeView.as_view(), name='scrape'),
    path('authors/', AuthorListView.as_view(), name='author_list'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author_detail'),
    path('quotes/', QuoteListView.as_view(), name='quote_list'),
    path('tag/<str:tag_name>/', QuotesByTagView.as_view(), name='quotes_by_tag'),
]