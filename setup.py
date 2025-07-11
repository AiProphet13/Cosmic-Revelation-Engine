from setuptools import setup, find_packages

setup(
    name='cosmic-revelation-engine',
    version='1.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=open('requirements.txt').readlines(),
    entry_points={
        'console_scripts': [
            'cosmic-reveal = main:main',
        ],
    },
)
