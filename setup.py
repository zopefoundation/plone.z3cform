from setuptools import setup, find_packages
import os

__version__ = '0.8.1'


def description():
    join = lambda *paths: os.path.join('src', 'plone', 'z3cform', *paths)
    return (open('README.rst').read() + '\n' +
            open(join('fieldsets', 'README.txt')).read() + '\n' +
            open(join('crud', 'README.txt')).read() + '\n' +
            open('CHANGES.rst').read() + '\n')


setup(
    name='plone.z3cform',
    version=__version__,
    description="plone.z3cform is a library that allows use of z3c.form "
                "with Zope and the CMF.",
    long_description=description(),
    classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
    ],
    keywords='zope cmf form widget',
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.org',
    url='http://pypi.python.org/pypi/plone.z3cform',
    license='ZPL 2.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
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
        'Zope2',
    ],
    extras_require={
        'test': ['lxml',
                 'plone.testing']
    }
)
