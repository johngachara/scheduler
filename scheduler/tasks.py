import requests
from celery import shared_task


@shared_task
def helllo():
    print("Hello World")


@shared_task
def disable_customer():
    url = "https://isp.phenom-ventures.com/disable_customer"
    try:
        response = requests.get(url)
        print(response.json())
    except Exception as e:
        print(e)

@shared_task
def activate_subscription():
    url = "https://isp.phenom-ventures.com/enable_customer"
    try:
        response = requests.get(url)
        print(response.json())
    except Exception as e:
        print(e)