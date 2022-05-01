import time

from celery import shared_task
from django.core.mail import send_mail


from blog.celery import app
# @shared_task()


@app.task
def send_confirmation_email(code, email):
    time.sleep(10)
    full_link = f'http://localhost:8000/account/activate/{code}'
    send_mail(
        'Привет',
        full_link,
        'ademi.niiazbekkyzy@gmail.com',
        [email]
    )


