from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.utils.html import strip_tags
import os


def detectUser(user):
    if user.role == 1:
        redirectUrl = 'vendorDashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'custDashboard'
        return redirectUrl
    elif user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl


def send_verification_email(request, user, mail_subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    mail_subject = mail_subject
    message = render_to_string(email_template,{
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    send_email = EmailMultiAlternatives(mail_subject, message, from_email, to=[to_email])
    send_email.content_subtype = "html"
    send_email.send()


def send_notification(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template,context)
    plain_text = strip_tags(message)
    to_email = context['user'].email
    send_email = EmailMessage(mail_subject, plain_text, from_email, to=[to_email])
    send_email.content_subtype = "html"
    send_email.send()

# def send_notification(mail_subject, mail_template, context, image_paths=None):
#     from_email = settings.DEFAULT_FROM_EMAIL
#     to_email = context['user'].email

#     # Render email template
#     message = render_to_string(mail_template, context)
#     plain_text = strip_tags(message)

#     # Create email message
#     email = EmailMessage(
#         mail_subject,
#         plain_text,
#         from_email,
#         to=[to_email]
#     )
#     email.content_subtype = "html"

#     # Attach static images
#     if image_paths:
#         for path in image_paths:
#             if os.path.isfile(path):
#                 with open(path, 'rb') as file:
#                     filename = os.path.basename(path)
#                     content_type = 'image/jpeg' if filename.endswith('.jpg') else 'image/png'
#                     email.attach(filename, file.read(), content_type)

#     # Send email
#     email.send()