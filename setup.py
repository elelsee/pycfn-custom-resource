from setuptools import setup, find_packages


setup(name='pycfn-customresource',
      version='0.1',
      description='AWS Cloudformation Lambda-backed CustomResources in Python',
      author='Scott VanDenPlas',
      author_email='scott@elelsee.com',
      url='https://github.com/elelsee/lambda-customresource',
      packages=find_packages(),
      py_modules= ['pycfn_custom_resource.lambda_backed', 'pycfn_custom_resource.util'],
      install_requires = ['requests']
     )
