from django.shortcuts import render
from .models import SearchHistory
import requests

API_KEY = "6167d84113e7bdbcd0a5ba7ae71b2711"
# Create your views here.
def index(request):
    weather = None
    error = None
    recent_searches = SearchHistory.objects.order_by("-searched_at")[:5]

    if request.method == "POST":
        city = request.POST.get('city').strip()
        if city:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            try:
                res = requests.get(url,timeout=5)
                data = res.json()
                if res.status_code == 200:
                     weather = {
                        'city': f"{data['name']}, {data['sys']['country']}",
                        'temperature': data['main']['temp'],
                        'humidity': data['main']['humidity'],
                        'pressure': data['main']['pressure'],
                        'description': data['weather'][0]['description'].title(),
                        'icon': data['weather'][0]['icon'],
                     }
                     SearchHistory.objects.create(
                         city_name=data['city'],
                         temperature=data['main']['temp'],
                         humidity=data['main']['humidity'],
                         pressure=data['main']['pressure'],
                         description=data['weather'][0]['description'].title()
                     )
                     recent_searches = SearchHistory.objects.order_by("-searched_at")[:5]
                else:
                    error = data.get("message" , "could not fetch weather data")     
            except requests.RequestException:
                error = "Network error . Please try again later"
        else:
            error = "Please enter a city name"        
    return render(request , "weather_dashboard/index.html" , context={
        'weather':weather,
        'error':error,
        'recent_serches':recent_searches
    })
