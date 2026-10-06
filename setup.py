from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name = "Multi_agent_udemy",
    version = "0.1.0",
    author = "Baibhab",
    packages = find_packages(),
    install_requires = requirements
)