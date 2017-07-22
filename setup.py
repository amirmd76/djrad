from setuptools import setup, find_packages

readme = "Django-JSONRPC-REST-API-Decorators (DJRAD)"

setup(
    name='djrad',
    version='1.0.0',
    description='Decorators for JSONRPC and REST API on django',
    long_description=readme,
    author='Divar submit team',
    author_email='rteam@divar.ir',
    url='https://github.com/amirmd76/djrad.git',
    license='MIT',
    packages=find_packages(),
    install_requires=[
          'django', 'jsonschema==2.6.0'
      ]
)
