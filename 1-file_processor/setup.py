from setuptools import setup, find_packages

setup(
    name="src",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "src=src.main:main",
        ],
    },
    python_requires=">=3.9",
)
