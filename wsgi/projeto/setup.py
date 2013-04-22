import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'plim',
    'deform',

    'repoze.tm2>=1.0b1', # default_commit_veto
    'WebError',
    ]

if sys.version_info[:3] < (2,5,0):
    requires.append('pysqlite')

setup(name='projeto',
      version='0.0',
      description='projeto',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require = requires,
      test_suite='projeto',
      entry_points="""\
      [paste.app_factory]
      main3 = projeto:main3
      """,
      paster_plugins=['pyramid'],
      )
