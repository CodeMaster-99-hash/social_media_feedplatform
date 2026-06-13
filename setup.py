"""
Setup configuration for social-media-platform package
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="social-media-platform",
    version="1.0.0",
    author="JOTHINDRA RAVURI",
    author_email="rjindra9848@gmail.com",
    description="Social Media Platform with Feed Algorithm & Graph Algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CodeMaster-99-hash/social_media_feedplatform.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies needed!
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.0.0",
            "mypy>=1.4.1",
        ]
    },
)