from setuptools import find_packages, setup


setup(
    name="secret-diary",
    version="2.0",
    packages=find_packages(),
    install_requires=["pysqlcipher"])