from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Adv
from django.db.models import Q


def get_random_advs(count=4):
    return Adv.objects.order_by('?')[:count]


def home_page(request):
    hot_posts = Post.objects.all().order_by('-created_at')[:4]
    random_posts = Post.objects.order_by('?')[:6]
    advs = get_random_advs(4)
    context = {
        'hot_posts': hot_posts,
        'posts': random_posts,
        'advs': advs
    }
    return render(request, "index.html", context)


def all_news_page(request):
    posts = Post.objects.all().order_by('-created_at')
    advs = get_random_advs(4)
    context = {
        'posts': posts,
        'advs': advs
    }
    return render(request, "all-news.html", context)


def news_by_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = Post.objects.filter(category=category).order_by('-created_at')
    advs = get_random_advs(4)
    context = {
        'category': category,
        'posts': posts,
        'advs': advs
    }
    return render(request, "news-by-category.html", context)


def search_page(request):
    return render(request, "search.html")


def search_results(request):
    query = request.GET.get('q')
    results = []
    if query:
        # Добавлено Q(category__name__icontains=query) для поиска по категории
        # Добавлено .distinct() чтобы избежать возможных дубликатов новостей
        results = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
        
    context = {
        'query': query,
        'results': results
    }
    return render(request, "search-results.html", context)


def read_news_page(request, pk):
    post = get_object_or_404(Post, pk=pk)

    related_posts = Post.objects.filter(
        category=post.category
    ).exclude(pk=pk).order_by('?')[:4]

    advs = get_random_advs(4)

    context = {
        'post': post,
        'related_posts': related_posts,
        'advs': advs
    }
    return render(request, "read-news.html", context)