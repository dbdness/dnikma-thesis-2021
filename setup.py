from setuptools import setup

setup(
    name='dnikma_integrity_checker',
    version='0.1',
    packages=['dnikma_integrity_checker'],
    install_requires=[
        'Click',
    ],
    author='dnikma',
    entry_points={
        'console_scripts': ['dic=dnikma_integrity_checker.cli.cli:main']
    },
)
