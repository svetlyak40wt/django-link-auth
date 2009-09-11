import md5
import time

from pdb import set_trace
from django.conf import settings
from django.http import Http404

from django.shortcuts import \
    redirect

from django.views.decorators.http import \
    require_POST, \
    require_GET

from django.views.decorators.cache import never_cache

from django_link_auth.models import Hash
from django_link_auth.signals import hash_was_generated


@require_POST
@never_cache
def send_login_link(request):
    email = request.POST.get('email')
    hash = md5.md5(email + settings.SECRET_KEY + str(time.time())).hexdigest()
    referer = request.META.get('HTTP_REFERER', '/')
    Hash(email = email, hash = hash, next = referer).save()

    hash_was_generated.send(sender = 'view', email = email, hash = hash)

    next = request.POST.get('next', '/')
    return redirect(next)


@require_GET
@never_cache
def login(request):
    from django.contrib.auth import \
        login, \
        authenticate

    hash = request.GET.get('hash')

    try:
        obj = Hash.valid.get(hash = hash)
    except Hash.DoesNotExist:
        raise Http404

    user = authenticate(hash = hash)
    login(request, user)

    return redirect(obj.next)

