#!/usr/bin/env python3
from setuptools import setup

import cmakedoc

with open('README.md') as f:
    long_description = f.read()

setup(
    name=cmakedoc.__appname__,
    version=cmakedoc.__version__,
    description=cmakedoc.DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Aurélien Gâteau',
    author_email='mail@agateau.com',
    license=cmakedoc.__license__,
    url='https://github.com/agateau/cmakedoc',
    py_modules=['cmakedoc'],
    entry_points={
        'console_scripts': [
            'cmakedoc = cmakedoc:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Build Tools',
    ],
    keywords='cmake doc development',
)
