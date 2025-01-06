from setuptools import setup, find_packages

setup(
    name="SearchForSimilarityWithTolerance",
    version="0.1.19",
    packages=find_packages(),
    install_requires=[
        # dependencies from requirements.txt
        'cdifflib >= 1.2.6'
    ],
)
