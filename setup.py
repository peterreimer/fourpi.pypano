#!/usr/bin/env	python

from setuptools import setup, find_packages
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='fourpi.pypano',
      version='0.0.1',
      description="toolbox for creating, remapping and publishing panoramas",
      long_description=read('README.md'),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Peter Reimer',
      author_email='peter@4pi.org',
      url='https://github.com/peterreimer/fourpi.pypano',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['fourpi', 'fourpi.pypano'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Pillow'
          # -*- Extra requirements: -*-
      ],
      entry_points={
          'console_scripts':[
            'tile=fourpi.pypano.tile:main',
            'rawbracket=fourpi.pypano.rawbracket:main'
          ]  
      },
      )
