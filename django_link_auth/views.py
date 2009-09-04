import md5
import time

from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from django_link_auth.models import Hash
from django_link_auth.signals import hash_was_generated

@require_POST
def send_link(request):
    email = request.POST.get('email')
    hash = md5.md5(email + settings.SECRET_KEY + str(time.time())).hexdigest()
    Hash(email = email, hash = hash).save()

    hash_was_generated.send(sender = 'view', email = email, hash = hash)

    next = request.POST.get('next', '/')
    return redirect(next)

