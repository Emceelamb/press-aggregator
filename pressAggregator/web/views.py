from django.shortcuts import render
from web.models import Article
from taggit.models import Tag


# Create your views here.
def home(request):
    articles = Article.objects.all()
    context = {"articles": articles}
    return render(request, "web/home.html", context)


def tag(request, slug):
    tags = Tag.objects.filter(slug=slug).values_list("name", flat=True)
    articles = Article.objects.filter(tags__name__in=tags)
    context = {"articles": articles, "tag": slug}
    return render(request, "web/tag.html", context)
