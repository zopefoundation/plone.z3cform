from setuptools import setup, find_packages
import os

version = '0.3'


def description():
    join = lambda *paths: os.path.join('plone', 'z3cform', *paths)
    return (open('README.txt').read() + '\n' +
            open(join('wysiwyg', 'README.txt')).read() + '\n' +
            open(join('queryselect', 'README.txt')).read() + '\n' +
            open(join('crud', 'README.txt')).read() + '\n' +
            open(os.path.join('docs', 'HISTORY.txt')).read() + '\n')

setup(name='plone.z3cform',
      version=version,
      description="A library that allows use of z3c.form with Zope 2 (and Plone)",
      long_description=description(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='zope plone forms',
      author='Daniel Nouri and contributors',
      author_email='daniel.nouri@gmail.com',
      url='http://pypi.python.org/pypi/plone.z3cform',
      license='ZPL 2.1',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone'],
      include_package_data=True,
      zip_safe=False,

      # If the dependency to z3c.form gives you trouble within a Zope
      # 2 environment, try the `fakezope2eggs` recipe
      install_requires=[
          'setuptools',
          'z3c.form',
          'z3c.formwidget.query',
          'zope.i18n>=3.4'
      ],
      )
