from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from django.urls import reverse
from django.forms import ModelForm
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
import requests

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

@csrf_exempt
def history(request, query_id):
    query = Query.objects.get(pk=query_id)
    articles = Article.objects.filter(search=query)
    return JsonResponse([article.serialize() for article in articles], safe=False)


@csrf_exempt
def likes(request, article_id):
    article = Article.objects.get(pk=article_id)
    return JsonResponse(article.serialize(), safe=False)

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

    """ if request.method == 'GET':
        results = None """

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
            'articles': results
        })

def likes(request):
    likes = Likes.objects.filter(user_liked_id=request.user.id).values_list('article_id', flat=True).distinct()
    articles = Article.objects.filter(id__in=likes)

    return render(request, 'news/likes.html', {
        "articles": articles
    })

def log(request):
    scrapes = Query.objects.filter(user=request.user).order_by('-time') 

    return render(request, 'news/log.html', {
        'scrapes': scrapes
    })