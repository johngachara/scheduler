"""Authenticated client for the Alltech API.

These jobs are machines, not people: they hold a shared API key, exchange it
for a short-lived token, and use that. They deliberately do not carry a user's
Supabase session -- a cron job is nobody, and giving it a person's identity
would make its actions indistinguishable from theirs in the logs.
"""
import logging
import os

import requests

logger = logging.getLogger('scheduler')

TIMEOUT = 150


class JobError(RuntimeError):
    """A job could not complete. Raised so the command exits non-zero and cron
    surfaces it, rather than a failure disappearing into a log nobody reads."""


def _base_url():
    url = os.getenv('ALLTECH_API_URL')
    if not url:
        raise JobError('ALLTECH_API_URL is not configured')
    return url.rstrip('/')


def machine_token():
    api_key = os.getenv('CELERY_KEY')
    if not api_key:
        raise JobError('CELERY_KEY is not configured')

    try:
        response = requests.post(
            f'{_base_url()}/api/celery-token/',
            json={'api_key': api_key},
            timeout=TIMEOUT,
        )
    except requests.RequestException as exc:
        raise JobError(f'Could not reach the API: {exc}') from exc

    if response.status_code != 200:
        raise JobError(f'Token request rejected ({response.status_code})')

    token = response.json().get('access')
    if not token:
        raise JobError('Token response contained no access token')
    return token


def call(path, method='GET'):
    """Call an endpoint with a freshly minted machine token.

    A token is minted per run rather than cached. Each run is a separate
    process that exists for seconds, so there is nothing to cache it in, and
    a short-lived token that never outlives the job is the safer default.
    """
    token = machine_token()
    try:
        response = requests.request(
            method,
            f'{_base_url()}{path}',
            headers={'Authorization': f'Bearer {token}'},
            timeout=TIMEOUT,
        )
    except requests.RequestException as exc:
        raise JobError(f'Request to {path} failed: {exc}') from exc

    # 404 is how these endpoints say "nothing to report today". That is a
    # normal outcome for a shop that was closed, not a failure.
    if response.status_code == 404:
        logger.info('%s: nothing to report', path)
        return None

    if response.status_code >= 400:
        raise JobError(f'{path} returned {response.status_code}: {response.text[:200]}')

    return response.json() if response.content else {}
