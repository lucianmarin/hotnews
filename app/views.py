from django.shortcuts import get_object_or_404, render
from app.helpers import get_paragraphs
from app.models import Article


def index(request):
    distinct = Article.objects.order_by('domain', '-shares').distinct('domain').values('id')
    index = Article.objects.filter(id__in=distinct).order_by('-shares')
    count = Article.objects.count()

    return render(request, 'index.jinja', {
        'articles': index[:15],
        'count': count,
        'view': 'index'
    })


def recent(request):
    distinct = Article.objects.order_by('domain', '-pub').distinct('domain').values('id')
    index = Article.objects.filter(id__in=distinct).order_by('-pub')
    count = Article.objects.count()

    return render(request, 'index.jinja', {
        'articles': index[:15],
        'count': count,
        'view': 'recent'
    })


def text(request, id):
    article = get_object_or_404(Article, id=id)
    lines = get_paragraphs(article.url)
    count = Article.objects.count()

    return render(request, 'index.jinja', {
        'article': article,
        'count': count,
        'line': lines,
        'view': 'text'
    })