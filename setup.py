#!/usr/bin/env python

from distutils.core import setup

README = open('README.md').read()
try:
	VERSION = open('VERSION').read().strip()
except IOError:
	VERSION = 'dev'

setup(
	name='kdbxpasswordpwned',
    version=VERSION,
    description='Check KeePass passwords against https://haveibeenpwned.com/Passwords',
    long_description_content_type='text/markdown',
    long_description=README,
    author='Filipe Pina',
    author_email='fopina@skmobi.com',
    url='https://github.com/fopina/kdbxpasswordpwned',
    py_modules=['kdbxpasswordpwned'],
    install_requires=[
    	'requests',
    	'libkeepass',
    ],
    entry_points={
		'console_scripts': ['kdbxpasswordpwned=kdbxpasswordpwned:main']
	},
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords=['keepass', 'hibp', 'password', 'data', 'breach', 'leak']
)
