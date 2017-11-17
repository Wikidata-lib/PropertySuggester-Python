import os

from setuptools import find_packages, setup


def requirements(fname):
    return [line.strip()
            for line in open(os.path.join(os.path.dirname(__file__), fname))]


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="propertysuggester",
    version="3.0.0",
    author="Wikidata team",
    description=("Contains scripts for PropertySuggester to preprocess the  "
                 "wikidata dumps"),
    url="https://github.com/Wikidata-lib/PropertySuggester-Python",
    packages=find_packages(),
    long_description=read('README.md'),
    install_requires=requirements("requirements.txt"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent"
    ],
)
