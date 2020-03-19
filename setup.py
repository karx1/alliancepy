from setuptools import setup
import alliancepy

setup(
    name="alliancepy",
    version=alliancepy.__version__,
    packages=["alliancepy"],
    author="karx",
    author_email="nerdstep710@gmail.com",
    description="A library to access The Orange Alliance API",
    python_requires=">=3.6"
)
