import django.dispatch

hash_was_generated = django.dispatch.Signal(providing_args = ['email', 'hash'])

