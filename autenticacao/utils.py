import re
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def usuario_ja_existe(request, username):
    if len(username.strip()) == 0:
        messages.add_message(request,constants.ERROR, 'Prencha o campo "Nome de Usuário".')
        return False

    user = User.objects.filter(username=username)
    if user.exists():
        messages.add_message(request, constants.ERROR, 'Esse usuário já  existe.')
        return False
    
    return True


def password_is_valid(request, password, confirm_password):
    if len(password.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha a senha.')
        return False

    if len(password) < 8:
        messages.add_message(request, constants.ERROR, 'Sua senha deve conter 8 ou mais caracteres.')
        return False
    
    if not password == confirm_password:
        messages.add_message(request, constants.ERROR, 'As senhas não coincidem.')
        return False

    if not re.search('[A-Z]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não contém letras maiúsculas.')
        return False
    
    if not re.search('[a-z]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não tem letras minúsculas.')
        return False

    if not re.search('[0-9]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não tem nenhum número.')
        return False
    
    return True


def email_html(path_template: str, assunto: str, para: list, **kwargs) -> dict:

    html_content = render_to_string(path_template, kwargs)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(assunto, text_content, settings.EMAIL_HOST_USER, para)

    email.attach_alternative(html_content, 'text/html')
    email.send()
    return {'status': 1}