from setuptools import setup, find_packages

setup(
    name="credit-card-fraud-detection",
    version="0.1",
    packages=find_packages(
        include=[
            "core",     
            "core.*",
            "steps",
            "steps.*",
            "pipelines",
            "pipelines.*"
        ]
    ),
    install_requires=[],
)