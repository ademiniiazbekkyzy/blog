import time

from django.core.mail import send_mail


def send_confirmation_email(code, email):
    time.sleep(10)
    full_link = f'http://localhost:8000/account/activate/{code}'
    send_mail(
        'Привет',
        full_link,
        'ademi.niiazbekkyzy@gmail.com',
        [email]
    )
