import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings



def sendgrid_send_email(to_email, subject):

    message = Mail(
        from_email='anvarliorxan@gmail.com',
        to_emails=to_email,
        subject=subject
    )
    message.template_id = settings.TEMPLATE_ID

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent! Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")