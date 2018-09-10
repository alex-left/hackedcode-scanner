#!/usr/bin/env python3
from distutils.core import setup

setup(
    name='codehacked-scanner',
    description='python pluggable application to scan a project code to find posible hints of hacking',
    author='Alex Left',
    author_email='aizquierdo@mrmilu.com',
    url='https://github.com/mrmilu/codehacked-scanner',
    version='0.1',
    packages=['codehacked-scanner'],
    entry_points={
        'console_scripts': [
            'codehacked-scanner=codehacked-scanner:main',
        ],
    },
    license='GPL-v3',
    long_description=open('readme.md').read(),
)
