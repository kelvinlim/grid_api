#!/usr/bin/env python3
"""
Setup script for GridAPI Python package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="gridapi",
    version="1.0.0",
    author="Grid API Team",
    author_email="team@gridapi.com",
    description="Python client library for Grid API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gridapi/gridapi-python",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "async": ["aiohttp>=3.8.0"],
        "cli": ["click>=8.0.0", "rich>=12.0.0"],
        "dev": ["pytest>=7.0.0", "pytest-asyncio>=0.21.0", "black>=22.0.0", "isort>=5.10.0"],
    },
    entry_points={
        "console_scripts": [
            "gridapi=gridapi.cli:main",
        ],
    },
)
