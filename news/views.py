from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from django.http import Http404
import json
from itertools import groupby
from .forms import CreateNewsForm, QueryForm
import datetime

# Create your views here.
class ComingSoonView(View):
    def get(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, 'r') as f:
            news = json.load(f)

        return render(request, 'news/coming_soon.html', context={'news': news})


class ArticleView(View):
    def get(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, 'r') as f:
            data = json.load(f)

        article = None
        for item in data:
            if item['link'] == kwargs['link']:
                article = item
                break

        if article is None:
            raise Http404('No such article')

        return render(request, 'news/article.html', context={'article': article})


class NewsView(View):
    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('q')

        with open(settings.NEWS_JSON_PATH, 'r') as f:
            articles = json.load(f)

            articles = sorted(articles, key=lambda x: x['created'], reverse=True)

            if search_query:
                filtered_articles = [article for article in articles if search_query in article['title']]
                grouped_articles = groupby(filtered_articles, key=lambda x: x['created'].split(' ')[0])
                articles_by_date = [{'date': date, 'articles': list(articles)} for date, articles in grouped_articles]
            else:
                # turns 2020-02-22 14:00:00 into 2020-02-22
                grouped_articles = groupby(articles, key=lambda x: x['created'].split(' ')[0])
                # [{'date': '2020-02-22', 'articles': [article1, article2, ...]}, ...]
                articles_by_date = [{'date': date, 'articles': list(articles)} for date, articles in grouped_articles]
        return render(request, 'news/news.html', context={'articles_by_date': articles_by_date, 'search_query': search_query})


class CreateNewsView(View):
    def get(self, request, *args, **kwargs):
        form = CreateNewsForm()
        return render(request, 'news/create_news.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = CreateNewsForm(request.POST)
        if form.is_valid():
            with open(settings.NEWS_JSON_PATH, 'r') as f:
                data = json.load(f)
                max_link = max([item['link'] for item in data])
                date_format = '%Y-%m-%d'
                data.append({
                    'created': datetime.datetime.now().strftime(date_format),
                    'text': form.cleaned_data['text'],
                    'title': form.cleaned_data['title'],
                    'link': max_link + 1
                })
            with open(settings.NEWS_JSON_PATH, 'w') as f:
                json.dump(data, f)
            return redirect('news')
        return render(request, 'news/create_news.html', context={'form': form})