from setuptools import setup, find_packages
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

__version__ = read('version.txt').strip()
__author__ = "Peter Reimer"

setup(name='fourpi.pypano',
      version=__version__,
      description="toolbox for creating, remapping and publishing panoramas",
      long_description=read('README'),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author=__author__,
      author_email='peter@4pi.org',
      url='http://svn.4pi.org/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['fourpi', 'fourpi.pypano'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
