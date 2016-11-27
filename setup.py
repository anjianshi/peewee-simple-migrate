from setuptools import find_packages
from setuptools import setup

setup(
    name='peewee-simple-migrate',
    version='0.0.5',
    url='https://github.com/anjianshi/peewee-simple-migrate',
    license='MIT',
    author='anjianshi',
    author_email='anjianshi@gmail.com',
    description="a simple migrations manager for peewee",
    py_modules=["peewee_simple_migrate"],
    install_requires=['peewee'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
