from setuptools import setup, find_packages


setup(name='lambda-customresource',
      version='0.1',
      description='AWS Cloudformation Lambda-backed CustomResources in Python',
      author='Scott VanDenPlas',
      author_email='scott@elelsee.com',
      url='https://github.com/elelsee/lambda-customresource',
      packages=find_packages(),
      py_modules= ['customresource'],
      install_requires = ['requests==2.8.1']
     )
