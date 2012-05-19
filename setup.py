from setuptools import setup, find_packages
import os

version = '0.8.0dev'


def description():
    join = lambda *paths: os.path.join('plone', 'z3cform', *paths)
    return (open('README.txt').read() + '\n' +
            open(join('fieldsets', 'README.txt')).read() + '\n' +
            open(join('crud', 'README.txt')).read() + '\n' +
            open(os.path.join('docs', 'HISTORY.txt')).read() + '\n')

setup(name='plone.z3cform',
      version=version,
      description="plone.z3cform is a library that allows use of z3c.form "
      "with Zope 2 and the CMF.",
      long_description=description(),
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='zope cmf form widget',
      author='Daniel Nouri and contributors',
      author_email='daniel.nouri@gmail.com',
      url='http://pypi.python.org/pypi/plone.z3cform',
      license='ZPL 2.1',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.batching',
          'z3c.form',
          'zope.i18n>=3.4',
          'zope.browserpage',
          'zope.component',
          'collective.monkeypatcher',
      ],
      extras_require = {
        'test': ['lxml',
                 'zope.app.testing']
      }
      )
