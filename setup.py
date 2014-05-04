from setuptools import setup

import os

# Put here required packages
packages = ['Django<=1.6','pysqlite',]

if 'REDISCLOUD_URL' in os.environ and 'REDISCLOUD_PORT' in os.environ and 'REDISCLOUD_PASSWORD' in os.environ:
     packages.append('django-redis-cache')
     packages.append('hiredis')

setup(name='meansweep',
      version='1.0',
      description='Minesweep clone',
      author='Dave Sewell',
      author_email='snocorp@gmail.com',
      url='http://snocorp.github.io/',
      install_requires=packages,
)

