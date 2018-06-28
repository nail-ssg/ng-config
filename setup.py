from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='ng-config',
    version='1.0',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'readme.md'), encoding='utf-8').read(),
)
