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

@shared_task
def send_alltech_sales():
    print("Sending Sales")
    url = os.getenv("ALLTECH_SERVER")
    route = url + "api/send_sale2"
    auth_url = url + "api/token/"
    username = os.getenv("ALLTECH_USERNAME")
    password = os.getenv("ALLTECH_PASSWORD")
    auth = requests.post(auth_url,json={"username":username,"password":password}).json()
    token = auth['access']
    try:
        send_sale = requests.get(route, headers={"Authorization": "Bearer " + token}).json()
        print(send_sale)
    except Exception as e:
        print(e)

@shared_task
def send_alltech_low_stock():
    print("Sending Low Stock")
    url = os.getenv("ALLTECH_SERVER")
    route = url + "api/send_low_stock"
    auth_url = url + "api/token/"
    username = os.getenv("ALLTECH_USERNAME")
    password = os.getenv("ALLTECH_PASSWORD")
    auth = requests.post(auth_url,json={"username":username,"password":password}).json()
    token = auth['access']
    try:
        send_sale = requests.get(route, headers={"Authorization": "Bearer " + token}).json()
        print(send_sale)
    except Exception as e:
        print(e)