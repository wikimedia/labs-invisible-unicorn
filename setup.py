"""
Invisible-Unicorn
----------------

Invisible Unicorn is the API for the 'dynamicproxy' written by yuvipanda.

The dynamicproxy code lives in the WMF puppet repo, and nowhere else at
the moment.

https://github.com/wikimedia/labs-invisible-unicorn

"""
from setuptools import setup


setup(
    name='invisible-unicorn',
    version='1.0',
    url='http://github.com/mitsuhiko/flask-sqlalchemy',
    license='Apache',
    author='Yuvi Panda',
    author_email='yuvipanda@gmail.com',
    description='Adds REST API for dynamic proxy',
    packages=['invisible_unicorn'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'setuptools',
        'Flask>=0.10',
        'redis',
        'sqlalchemy',
        'Flask-SQLAlchemy',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    entry_points = {
        'console_scripts': [ 'dynamic-proxy-api = invisible_unicorn.api:main' ]
    }
)
