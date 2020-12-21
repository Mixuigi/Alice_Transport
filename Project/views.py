from django.shortcuts import render
from .models import Person
import json
import requests
from bs4 import BeautifulSoup
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['Post'])
def time_manager(request):
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': True
        }
    }
    response['response']['text'] = '40'
    return json.dumps(response)

def get_time(city, type, number, direction, stop):
    url = f'https://kogda.by/routes/{city}/{type}/{number}/{direction}/{stop}'
    try:
        response = requests.get(url)
    except:
        raise Exception
    soup = BeautifulSoup(response.text, 'lxml')
    times = soup.find_all('span', class_='future')
    return list(map(lambda x: x.text.strip().replace(':', ' '), times))



