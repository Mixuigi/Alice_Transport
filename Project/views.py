from django.shortcuts import render
from .models import Person
import json
import requests
from bs4 import BeautifulSoup
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['Post'])
def time_manager(request):
    request = request.data
    response = {
        'session': request['session'],
        'version': request['version'],
        'response': {
            'end_session': False
        }
    }
    if request['request']['original_utterance']:
        response['response']['text'] = 'Позже...'
    else:
        Person(alice_user_id=request['session']['user']['user_id'])
        if Person:
            times = get_time(Person.city, Person.type, Person.number, Person.direction, Person.stop)
            response['response']['text'] = f'Ближайший автобус будет в {times[0]}, а следующий в {times[1]}'
        else:
            print(request['session']['user']['user_id'])
            response['response']['text'] = 'Пользователь не зарегистрирован'
    return Response(response)

def get_time(city, type, number, direction, stop):
    url = f'https://kogda.by/routes/{city}/{type}/{number}/{direction}/{stop}'
    try:
        response = requests.get(url)
    except:
        raise Exception
    soup = BeautifulSoup(response.text, 'lxml')
    times = soup.find_all('span', class_='future')
    return list(map(lambda x: x.text.strip().replace(':', ' '), times))
