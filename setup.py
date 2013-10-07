#! /usr/bin/env python
import os
from setuptools import setup, find_packages

def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

setup(
    name='djpl-container-management',
    version='0.1',
    description='provides basic management tasks for django-productline',
    long_description=read('README.rst'),
    license='The MIT License',
    keywords='django-productline, spl-container, product-line, web-application',
    author='Hendrik Speidel',
    author_email='hendrik@schnapptack.de',
    url="https://github.com/henzk/djpl-container-management",
    packages=find_packages(),
    package_dir={'djpl_container_management': 'djpl_container_management'},
    package_data={'djpl_container_management': []},
    include_package_data=True,
    scripts=[],
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent'
    ],
    install_requires=[
        'ape>=0.2.0',
        #'cookiecutter' FIXME add this when cookiecutter 0.6.5 is out
    ],
)
