#!/usr/bin/env python3
from setuptools import setup, find_packages

packages=find_packages('hackedcode_scanner')

setup(
    name='hackedcode-scanner',
    description='python pluggable application to scan a project code \
        to find posible hints of hacking',
    author='Alex Left',
    author_email='aizquierdo@mrmilu.com',
    url='https://github.com/mrmilu/hackedcode-scanner',
    version=hackedcode_scanner.main.__version__,
    packages=find_packages(),
    install_requires=["pyyaml"],
    entry_points={
        'console_scripts': [
            'hackedcode-scanner=hackedcode_scanner.main:main',
        ],
    },
    include_package_data=True,
    license='GPL-v3',
    long_description=open('readme.md').read(),
)
