from celery import shared_task


@shared_task
def helllo():
    print("Hello World")