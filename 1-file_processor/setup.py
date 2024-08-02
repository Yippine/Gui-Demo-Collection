from setuptools import setup, find_packages

setup(
    name="file_processor",
    version="2.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "PyQt5==5.15.6",
    ],
    entry_points={
        "console_scripts": [
            "file_processor=src.main:main",
        ],
    },
    python_requires=">=3.7",
)
