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
        user = request['session'].get('user', False)
        if user:
            try:
                person = Person.objects.get(alice_user_id=request['session']['user']['user_id'])
                times = get_time(person.city, person.type, person.number, person.direction, person.stop)
                response['response']['text'] = f'Ближайший автобус будет в {times[0]}, а следующий в {times[1]}'
            except:
                response['response'][
                    'text'] = f'Пользователь не зарегистрирован ваш id {request["session"]["user"]["user_id"]}'
        else:
            response['response']['text'] = 'Нету id пользователя'
    else:
        response['response']['text'] = 'Позже...'
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
