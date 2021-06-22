from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def sample_task():
    print("The sample task just ran.")

