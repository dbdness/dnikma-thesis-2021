from setuptools import setup

setup(
    name='dnikma_integrity_checker',
    version='0.1',
    packages=['dnikma_integrity_checker'],
    install_requires=[
        'python-nubia',
        'mysql-connector-python',
        'termcolor',
        'prettytable',
        'requests'
    ],
    author='dnikma',
    entry_points={
        'console_scripts': ['dic=dnikma_integrity_checker.shell.shell:entry_point']
    },
)
