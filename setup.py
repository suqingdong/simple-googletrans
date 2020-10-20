# -*- encoding: utf8 -*-
import os
import json
import codecs
from setuptools import setup, find_packages


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
version_info = json.load(open(os.path.join(BASE_DIR, 'simple_googletrans', 'version.json')))

setup(
    name='simple-googletrans',
    version=version_info['version'],
    author=version_info['author'],
    author_email=version_info['author_email'],
    description='A simple wrapper of googletrans',
    long_description=codecs.open(os.path.join(BASE_DIR, 'README.md'), encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/suqingdong/simple-googletrans',
    project_urls={
        'Tracker': 'https://github.com/suqingdong/simple-googletrans/issues',
    },
    license='BSD License',
    install_requires=open(os.path.join(BASE_DIR, 'requirements.txt')).read().split('\n'),
    packages=find_packages(),
    include_package_data=True,
    entry_points={'console_scripts': [
        'gtranslate = simple_googletrans.__init__:main',
    ]},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ]
)