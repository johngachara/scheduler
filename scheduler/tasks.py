import os

import requests
from celery import shared_task


@shared_task
def helllo():
    print("Hello World")


@shared_task
def disable_customer():
    route = os.getenv('BACKEND_ROUTE')
    url = route + "/disable_customer"
    try:
        response = requests.get(url)
        print(response.json())
    except Exception as e:
        print(e)

@shared_task
def activate_subscription():
    route = os.getenv('BACKEND_ROUTE')
    url = route + "/enable_customer"
    try:
        response = requests.get(url)
        print(response.json())
    except Exception as e:
        print(e)

@shared_task
def ping_render_server():
    print("Task executed")
    server = os.getenv('RENDER_SERVER')
    try:
        response = requests.get(server)
        print(response.json())
    except Exception as e:
        print(e)