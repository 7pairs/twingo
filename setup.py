# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

from twingo import __version__


setup(
    name='twingo',
    version=__version__,
    description='Authentication application for Django on Python 2.x',
    author='Jun-ya HASEBA',
    author_email='7pairs@gmail.com',
    url='http://seven-pairs.hatenablog.jp/',
    packages=find_packages(exclude=['tests']),
    install_requires=['tweepy'],
)