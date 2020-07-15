from setuptools import setup, find_packages
#from distutils.core import setup, Extension

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["ipython>=6", "nbformat>=4", "nbconvert>=5", "requests>=2"]

setup(
    name="forecmodels",
    version="0.0.2",
    author="Kirill Mansurov",
    author_email="mantis1999@mail.ru",
    description="A package to building forecasting models",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/Kiri28/forecmodels",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
