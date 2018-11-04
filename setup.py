from setuptools import setup, find_packages
import os

__version__ = '1.0.0'


def description():
    join = lambda *paths: os.path.join('src', 'plone', 'z3cform', *paths)
    return (
        open('README.rst').read()
        + '\n'
        + open(join('fieldsets', 'README.rst')).read()
        + '\n'
        + open(join('crud', 'README.txt')).read()
        + '\n'
        + open('CHANGES.rst').read()
        + '\n'
    )


setup(
    name='plone.z3cform',
    version=__version__,
    description="plone.z3cform is a library that allows use of z3c.form "
    "with Zope and the CMF.",
    long_description=description(),
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 5.2",
        "Framework :: Zope :: 4",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords='zope cmf form widget',
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.org',
    url='https://pypi.org/project/plone.z3cform',
    license='ZPL 2.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['plone'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'plone.batching',
        'six',
        'z3c.form',
        'zope.i18n>=3.4',
        'zope.browserpage',
        'zope.component',
        'Zope',
    ],
    extras_require={'test': ['lxml', 'plone.testing[z2]']},
)
