from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='djrad',
    version='0.0.5',
    description='Decorators for JSONRPC and REST API on django',
    long_description=readme,
    author='Divar submit team',
    author_email='rteam@divar.ir',
    url='https://github.com/amirmd76/djrad.git',
    license=license,
    packages=find_packages()
)
