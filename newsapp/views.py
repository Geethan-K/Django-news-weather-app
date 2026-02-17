from django.shortcuts import render
from newsapi import NewsApiClient

# Create your views here.
def index(request):
    newsapi = NewsApiClient(api_key="b9e6ff9f043f477c960a33a7284821a7")
    top_headlines = newsapi.get_top_headlines(
                                          category='business',
                                          language='en',
                                          country='us')
    articles = top_headlines['articles']
        
    return render(request , 'index.html' , context={"articles":articles})

