from setuptools import setup, find_packages

__version__ = "0.1.0"

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="bumper",
    version=__version__,
    description="Version bumper for python projects across many files",
    long_description=long_description,
    author="BlakeJC94",
    author_email="blakejamescook@gmail.com",
    url="https://github.com/BlakeJC94/bumper",
    python_requires=">=3.9",
    packages=find_packages(),
    install_requires=[
        "gitpython",
    ],
    extras_require={
        "dev": [
            "black",
            "pip-tools",
            "pre-commit",
            "pylint",
            "pytest",
            "pytest-cov",
        ],
    },
    entry_points={
        "console_scripts": ["bumper=bumper.__main__:main"],
    },
)
