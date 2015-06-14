from setuptools import find_packages, setup


setup(
    name="secret-diary",
    version="2.0",
    packages=find_packages(),
    entry_points={'console_scripts': ['diary = diary:main']},
    install_requires=["arrow", "docopt", "pysqlcipher3", "sqlalchemy-utils"],
    test_suite='nose.collector',
    setup_requires=['coverage', 'nose'])
