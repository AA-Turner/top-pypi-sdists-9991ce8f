#!/usr/bin/env python

import sys
from setuptools import setup

if sys.version_info < (2, 7):
    raise NotImplementedError("Sorry, you need at least Python 2.7 or Python 3.6+ to use bottle.")

import bottle

setup(name='bottle',
      version=bottle.__version__,
      description='Fast and simple WSGI-framework for small web-applications.',
      long_description=bottle.__doc__,
      long_description_content_type="text/markdown",
      author=bottle.__author__,
      author_email='marc@gsites.de',
      url='http://bottlepy.org/',
      project_urls={
          'Source': 'https://github.com/bottlepy/bottle',
      },
      py_modules=['bottle'],
      scripts=['bottle.py'],
      entry_points={
        'console_scripts': [
          'bottle = bottle:main',
        ]
      },
      license='MIT',
      platforms='any',
      classifiers=['Development Status :: 4 - Beta',
                   "Operating System :: OS Independent",
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
                   'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
                   'Topic :: Internet :: WWW/HTTP :: WSGI',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
                   'Topic :: Software Development :: Libraries :: Application Frameworks',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.8',
                   'Programming Language :: Python :: 3.9',
                   'Programming Language :: Python :: 3.10',
                   'Programming Language :: Python :: 3.11',
                   'Programming Language :: Python :: 3.12',
                   'Programming Language :: Python :: 3.13',
                   ],
      )
