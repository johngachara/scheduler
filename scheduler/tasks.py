import logging
import os

import requests
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def hello():
    print("Hello World")


def get_sequelizer_token():
    try:
        print("Getting sequelizer token")
        url = os.getenv('SEQUELIZER_AUTH')
        response = requests.post(url,json={'api_key': os.getenv('CELERY_API_KEY')}).json()
        token = response['token']
        return token
    except requests.exceptions.RequestException as e:
        print(e)


def get_shop2_token():
    try:
        print("Getting shop2 token")
        url = os.getenv('ALLTECH_AUTH')
        response = requests.post(url, json={'api_key': os.getenv('CELERY_API_KEY')}).json()
        token = response['access']
        return token
    except requests.exceptions.RequestException as e:
        print(e)


@shared_task
def send_shop2_accessories():
    try:
        logger.info("Sending shop2 accessories")
        token = get_sequelizer_token()
        url = os.getenv('SHOP2_ACCESSORIES_URL')
        headers = {'celery-auth-token':token}

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        logger.info('Accessories response: %s', response.json())
        return "Task completed successfully"
    except requests.exceptions.HTTPError as http_err:
        logger.error('HTTP error occurred: %s', http_err)
    except requests.exceptions.RequestException as req_err:
        logger.error('Request exception occurred: %s', req_err)
    except Exception as e:
        logger.error('General error occurred: %s', str(e))

    return "Task failed"


@shared_task
def send_shop2_lcd():
    try:
        logger.info("Sending shop2 LCD")
        token = get_shop2_token()
        url = os.getenv('SHOP2_LCD_URL')
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logger.info('LCD response: %s', response.json())
        return "Task completed successfully"
    except requests.exceptions.HTTPError as http_err:
        logger.error('HTTP error occurred: %s', http_err)
    except requests.exceptions.RequestException as req_err:
        logger.error('Request exception occurred: %s', req_err)
    except Exception as e:
        logger.error('General error occurred: %s', str(e))
    return "Task failed"


@shared_task
def send_shop1_accessories():
    try:
        logger.info("Sending shop1 accessories")
        url = os.getenv('SHOP1_ACCESSORIES_URL')
        token = get_shop2_token()
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logger.info('Accessories response: %s', response.json())
        return "Task completed successfully"
    except requests.exceptions.HTTPError as http_err:
        logger.error('HTTP error occurred: %s', http_err)
    except requests.exceptions.RequestException as req_err:
        logger.error('Request exception occurred: %s', req_err)
    except Exception as e:
        logger.error('General error occurred: %s', str(e))


@shared_task
def send_shop1_lcd():
    try:
        logger.info("Sending shop1 LCD")
        token = get_shop2_token()
        url = os.getenv('SHOP1_LCD_URL')
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logger.info('LCD response: %s', response.json())
        return "Task completed successfully"
    except requests.exceptions.HTTPError as http_err:
        logger.error('HTTP error occurred: %s', http_err)
    except requests.exceptions.RequestException as req_err:
        logger.error('Request exception occurred: %s', req_err)
    except Exception as e:
        logger.error('General error occurred: %s', str(e))

    return "Task failed"


