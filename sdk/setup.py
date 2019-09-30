# -*- coding: utf-8 -*-
"""
Copyright 2018 David Amrani Hernandez - ElevenPaths, Telefonica

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from setuptools import setup, find_packages

def read_file(filename):
    with open(filename) as f:
        return f.read()

setup(
    name='dome9',
    version=read_file('VERSION').strip(),
    install_requires=read_file('requirements.txt').splitlines(),
    packages=find_packages(),
    author='David Amrani Hernandez',
    author_email='davidmorenomad@gmail.com',
    url='https://github.com/davidmoremad',
    project_urls={
        "Documentation": "https://dome9.readthedocs.io",
        "Source Code": "https://github.com/davidmoremad/dome9",
    },
    description='Dome9 SDK for Python',
    long_description_content_type="text/markdown",
    long_description=read_file('README.md'),
    keywords="dome9 sdk cloudsecurity cspm",
    license='Apache 2.0',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Security',
        'Environment :: Console',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Natural Language :: English'
    ],
)
