from django.urls import path
from .views import ArticleView, NewsView, CreateNewsView
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/news/')),
    path('news/<int:link>/', ArticleView.as_view(), name='news_article'),
    path('news/', NewsView.as_view(), name='news'),
    path('news/create/', CreateNewsView.as_view(), name='create_news'),
]