#!/usr/bin/env python3
from setuptools import setup

import cmakehelp

setup(
    name=cmakehelp.__appname__,
    version=cmakehelp.__version__,
    description=cmakehelp.DESCRIPTION,
    author='Aurélien Gâteau',
    author_email='mail@agateau.com',
    license=cmakehelp.__license__,
    platforms=['Linux'],
    url='https://github.com/agateau/cmakehelp',
    py_modules=['cmakehelp'],
    entry_points={
        'console_scripts': [
            'cmakehelp = cmakehelp:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Build Tools',
    ]
)
