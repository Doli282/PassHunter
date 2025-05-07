from setuptools import setup, find_packages

setup(
    name="models",
    version="1.0",
    author='LD',
    packages=find_packages(),
    install_requires=[
        "Flask-SQLAlchemy>=3.1.1",
        "Flask-Login>=0.6.3",
        "typing_extensions>=4.13.2"
    ]
)