#!/usr/bin/env python

from distutils.core import setup

setup(name='lambda-customresource',
      version='0.1',
      description='AWS Cloudformation Lambda-backed CustomResources in Python',
      author='Scott VanDenPlas',
      author_email='scott@elelsee.com',
      url='https://github.com/elelsee/lambda-customresource',
      packages=['lambda-customresource'],
      install_requires = ['requests==2.8.1']
     )
