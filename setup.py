from setuptools import setup

setup(name='SlackAPI',
      version='0.1',
      description='An implementation of (some elements of) the Slack API.',
      url='https://github.com/spurll/slackapi',
      author='Gem Newman',
      author_email='spurll@gmail.com',
      license='CC BY-NC-SA 3.0',
      packages=['slackapi'],
      install_requires=['requests'],
      zip_safe=False)
