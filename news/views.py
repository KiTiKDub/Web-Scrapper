from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from django.urls import reverse
from django.forms import ModelForm
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from bs4 import BeautifulSoup
from itertools import islice
import requests
import json

from .models import Query, User, Article, Likes, Dislikes

# Create your views here.

WEBSITES = [
    ('Select', 'Select'),
    ('TechCrunch', 'TechCrunch'),
    ('Gizmodo', 'Gizmodo'),
    ('digitaltrends', 'digitaltrends')

]

class Search(ModelForm):
    website = forms.CharField(label='Website', widget=forms.Select(choices=WEBSITES))
    query = forms.CharField(label='Keywords', widget=forms.TextInput(attrs={'class': 'search form-control'}))

    website.widget.attrs.update({'class': 'form-select dropdown'})

    class Meta:
        model = Query
        fields = ['website', 'query']


def history(request, query_id):
    query = Query.objects.get(pk=query_id)
    articles = Article.objects.filter(search=query)
    return JsonResponse([article.serialize() for article in articles], safe=False)

@csrf_exempt
def liked(request):
    data = json.loads(request.body)
    article_id = data.get("article_id", "")
    article = Article.objects.get(pk=article_id)
    liked_id = data.get("user_liked_id", "")
    user = User.objects.get(pk=liked_id)

    try:
        check_dislike = Dislikes.objects.get(article_id=article, user_disliked_id=user)
    except:
        check_dislike = None

    if check_dislike is not None:
        check_dislike.delete()

    try:
        new_like = Likes.objects.create(article_id=article, user_liked_id=user)
        new_like.save()
    except:
        return JsonResponse({"message": "You've already liked this Article!"}, status = 400)

    return JsonResponse({"message": "Article Liked Successfully"}, status=201)

@csrf_exempt
def disliked(request):
    data = json.loads(request.body)
    article_id = data.get("article_id", "")
    article = Article.objects.get(pk=article_id)
    disliked_id = data.get("user_disliked_id", "")
    user = User.objects.get(pk=disliked_id)

    try:
        check_like = Likes.objects.get(article_id=article, user_liked_id=user)
    except:
        check_like = None

    if check_like is not None:
        check_like.delete()
        
    try:
        new_dislike = Dislikes.objects.create(article_id=article, user_disliked_id=user)
        new_dislike.save()
    except:
        return JsonResponse({"message": "You've already disliked this Article!"}, status = 400)

    return JsonResponse({"message": "Article Disliked Successfully"}, status=201)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "news/login.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "news/register.html")

def index(request):
    form = Search()
    last_search = Query.objects.filter(user=request.user).latest('time')
    results = Article.objects.filter(search=last_search)
    paginator = Paginator(results, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':

        website = request.POST['website']

        if website == 'Select':
            return HttpResponseRedirect(reverse("index"))

        query = request.POST['query']
        query_entry = Query.objects.create(user=request.user, website=website, search=query)
        query_entry.save()
        links = []

        if website == 'TechCrunch':
            url = 'https://search.techcrunch.com/search;?p={}'.format(query)
            html = requests.get(url)
            soup = BeautifulSoup(html.content, 'lxml')
            articles = soup.find_all('h4', 'pb-10') 

            for i in range(len(articles)):
                new_url = articles[i]
                atag = new_url.a
                links.append(atag.get('href'))
            
            for link in links:
                html = requests.get(link)
                soup = BeautifulSoup(html.content, 'lxml')
                headline = soup.find('h1', 'article__title').text.strip()
                body = soup.find('p', {'id':'speakable-summary'}).text.strip()
                category = soup.find('meta', attrs={'name':'parsely-section'})
                cat_strip = category['content']
                article_entry = Article.objects.create(headline=headline, body=body, category=cat_strip, url=link, search=query_entry)
                article_entry.save()
        
            return HttpResponseRedirect(reverse("index"))
        
        elif website == 'Gizmodo':
            url = 'https://gizmodo.com/search?blogId=4&q={}'.format(query)
            html = requests.get(url)
            soup = BeautifulSoup(html.content, 'lxml')
            articles = soup.find_all('div', 'cw4lnv-5')
             #need to put in code to catch it if it is a video 

            for i in range(len(articles)):
                article = articles[i]
                atag = article.a
                links.append(atag.get('href'))
            
            for link in links:
                html = requests.get(link)
                soup = BeautifulSoup(html.content, 'lxml')

                if soup.find('h1', 'sc-1efpnfq-0') is None:
                    donothing = 0
                else:
                    headline = soup.find('h1', 'sc-1efpnfq-0').text.strip()
                    body = soup.find('p', 'sc-77igqf-0').text.strip()
                    category = soup.find('div', 'fek4t4-1').text.strip()
                    article_entry = Article.objects.create(headline=headline, body=body, category=category, url=link, search=query_entry)
                    article_entry.save()

            return HttpResponseRedirect(reverse('index'))
        
        else:
            url = 'https://www.digitaltrends.com/?s={}'.format(query) # change to something that doesn't have a pay wall
            html = requests.get(url)
            soup = BeautifulSoup(html.content, 'lxml')
            articles = soup.find_all('div', 'b-meta__title')

            for i in range(len(articles)):
                article = articles[i]
                atag = article.a
                link = atag.get('href')
                links.append(link)
            
            for link in links:
                html = requests.get(link)
                soup = BeautifulSoup(html.content, 'lxml')
                headline = soup.find('h1', 'b-headline__title').text.strip()
                body = soup.find('article', 'b-content').p.text.strip()
                category = soup.find('meta', attrs={'content':'2'})
                cat_clean = category.parent.span.text.strip()
                article_entry = Article.objects.create(headline=headline, body=body, category=cat_clean, url=link, search=query_entry)
                article_entry.save()
        return HttpResponseRedirect(reverse("index"))
    
    else:  
        return render(request, 'news/index.html', {
            'form': form,
            'articles': page_obj,
        })
    
def likes(request):
    likes = Likes.objects.filter(user_liked_id=request.user.id).values_list('article_id', flat=True).distinct()
    dislikes = Dislikes.objects.filter(user_disliked_id=request.user.id).values_list('article_id', flat=True).distinct()
    articles = Article.objects.filter(id__in=likes).order_by("-Likes")
    dis_articles = Article.objects.filter(id__in=dislikes).order_by("-Dislikes")
    paginator = Paginator(articles, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    cat_counts = {}
    dis_cat_counts = {}

    for article in articles:
        if article.category not in cat_counts:
            cat_counts[article.category] = {
                'category': article.category,
                'count': 0
            }
        cat_counts[article.category]['count'] += 1

    sort_cat_count = dict(sorted(cat_counts.items(), key=lambda item:item[1]['count'], reverse=True))
    top_five = dict(islice(sort_cat_count.items(), 5))

    for article in dis_articles:
        if article.category not in dis_cat_counts:
            dis_cat_counts[article.category] = {
                'category': article.category,
                'count': 0
            }
        dis_cat_counts[article.category]['count'] += 1

    sort_dis_cat_count = dict(sorted(dis_cat_counts.items(), key=lambda item:item[1]['count'], reverse=True))
    dis_top_five = dict(islice(sort_dis_cat_count.items(), 5))

    return render(request, 'news/likes.html', {
        "articles": page_obj,
        "counts": top_five.values(),
        "dis_counts": dis_top_five.values()
    })

def log(request):
    scrapes = Query.objects.filter(user=request.user).order_by('-time') 

    return render(request, 'news/log.html', {
        'scrapes': scrapes
    })