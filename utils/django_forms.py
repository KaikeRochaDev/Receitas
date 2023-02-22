import re
from django.core.exceptions import ValidationError

def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    
    if not regex.match(password):
        raise ValidationError((
            'A senha deve ter pelo menos uma letra maiúscula, uma letra minúscula e um número. ' 
            'A senha deve ser de pelo menos 8 caracteres'
        ),
            code='invalid')