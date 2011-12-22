import os
from setuptools import setup, find_packages

setup(
    name='django-treepages',
    description='Django app to create tree-structured pages',
    keywords='django, simple, page, webpage, cms',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    version="0.2",
    author="Matteo Scotuzzi",
    author_email="matteo.scotuzzi@gmail.com",
    classifiers = ['Framework :: Django',
                   'Intended Audience :: Developers',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python'
                   ],
    url="https://github.com/scotu/django-treepages",
    license="MIT",
    platforms=["all"]
)

