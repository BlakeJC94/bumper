from setuptools import setup, find_packages

__version__ = "0.0.0"

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="quaker",
    version=__version__,
    description="Lightweight python API to USGS earthquake dataset",
    long_description=long_description,
    author="BlakeJC94",
    author_email="blakejamescook@gmail.com",
    url="https://github.com/BlakeJC94/quaker",
    python_requires=">=3.9",
    packages=find_packages(),
    install_requires=[],
    extras_require={
        "dev": [
            "black",
            "pip-tools",
            "pylint",
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": ["bumper=bumper.__main__:main"],
    },
)
