#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name="mezzanine-cli",
    version="0.1",
    license='BSD',
    description="A command line interface for mezzanine.",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Mezzanine>=1.1.2',
    ],
)
