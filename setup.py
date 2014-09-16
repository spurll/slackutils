#!/usr/bin/env python


from setuptools import setup


setup(name='SlackUtils',
      version='0.1',
      description='An implementation of many Slack API functions designed to '\
                  'maximize ease-of-use.',
      url='https://github.com/spurll/slackutils',
      author='Gem Newman',
      author_email='spurll@gmail.com',
      license='CC BY-NC-SA 3.0',
      packages=['slackutils'],
      install_requires=['requests'],
      zip_safe=False)
