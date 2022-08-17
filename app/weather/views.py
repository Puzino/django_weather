import requests
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import CityForm
from .models import City


@csrf_exempt
def index(request):
    appid = '1db7e42ae10bc79cb600082f07e9a0c5'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    cities = City.objects.all()

    if request.method == 'POST':
        if str(request.POST['name']).isdigit():
            return render(request, 'weather/error.html', context={'error': 'Не верные данные'})
        else:
            form = CityForm(request.POST)
            form.save()

    form = CityForm()

    all_cities = []

    for city in cities:
        try:
            res = requests.get(url.format(city.name)).json()
            city_info = {
                'city': city.name,
                'temp': res['main']['temp'],
                'icon': res['weather'][0]['icon'],
            }
            all_cities.append(city_info)
        except:
            pass

    context = {"all_info": all_cities, 'form': form}

    return render(request, 'weather/weather_list.html', context=context)
