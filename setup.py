from setuptools import setup
import alliancepy

with open("README.rst") as f:
    readme = f.read()

setup(
    name="alliancepy",
    version=alliancepy.__version__,
    packages=["alliancepy"],
    url="https://github.com/karx1/alliancepy",
    license="MIT",
    author="karx",
    author_email="nerdstep710@gmail.com",
    description="A library to access The Orange Alliance API",
    long_description=readme,
    python_requires=">=3.6",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
    ]
)
