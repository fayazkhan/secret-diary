from setuptools import find_packages, setup


setup(
    name="secret-diary",
    version="3.0",
    packages=find_packages(),
    entry_points={'console_scripts': ['diary = diary:main']},
    install_requires=["arrow",
                      "docopt",
                      "flask",
                      "flask-admin",
                      "pysqlcipher3",
                      "sqlalchemy-utils"],
    test_suite='nose.collector')
