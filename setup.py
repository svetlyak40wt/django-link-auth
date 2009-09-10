import os
import sys
from setuptools import setup

sys.path.insert(0, '.')

setup(
    name = 'django-link-auth',
    version = '0.1.0',
    description = "Django's authentication backend to login by temporary URLs.",
    keywords = 'django apps authentication',
    license = 'New BSD License',
    author = 'Alexander Artemenko',
    author_email = 'svetlyak.40wt@gmail.com',
    url = 'http://github.com/svetlyak40wt/django-link-auth/',
    dependency_links = [],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages = ['django_link_auth'],
    include_package_data = True,
    zip_safe = False,
)


