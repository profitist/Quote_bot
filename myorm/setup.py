from setuptools import setup, find_packages

setup(
    name='myorm',
    version='0.1',
    packages=find_packages(),
    description='Мини ORM для SQLite (insert, select, where, delete)',
    author='profitist',
    python_requires='>=3.7',
)
