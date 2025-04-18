# -*- encoding: utf-8 -*-
# @File: setup.py
"""
biomdadbapi setup

To run: python3 setup.py install

"""


from setuptools import setup
 
setup(
    name='biomdadbapi',
    version='0.9.9',
    packages=['biomdadbapi'],
    description='The API for the BioMDA database',
    author='Zhan Li',
    author_email='smu18575877413@gmail.com',
    url='https://github.com/zimlik/biomdadbapi',
    license="MIT",
    install_requires=[
        'uvicorn>=0.34.0',
        'pydantic>=2.10.6, <2.11.0',
        'fastapi>=0.115.11',
        'sqlmodel>=0.0.23',
        'modules>=1.0.0',
        'python-multipart>=0.0.20',
        'configparser',
    ],
    exclude_package_data={'':['.gitignore',]},
    package_data={'': ['*.cfg', '*.rds']},
    entry_points={
        'console_scripts': ['biomdadb-api=biomdadbapi.main:main',
                            'biomdadb-add-config=biomdadbapi.config:add_config',
                            'biomdadb-show-config=biomdadbapi.config:show_config',]
    },
)