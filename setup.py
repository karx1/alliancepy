from setuptools import setup
import re

with open("README.rst") as f:
    readme = f.read()

with open("alliancepy/__init__.py") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)

extras_require = {
    "docs": ["sphinx", "sphinx-rtd-theme"],
    "async": ["aiohttp[speedups]", "nest_asyncio"],
}

setup(
    name="alliancepy",
    version=version,
    packages=["alliancepy", "alliancepy.ext.aio"],
    url="https://github.com/karx1/alliancepy",
    license="MIT",
    author="karx",
    author_email="nerdstep710@gmail.com",
    description="A library to access The Orange Alliance API",
    long_description=readme,
    python_requires=">=3.6",
    extras_require=extras_require,
    test_suite="nose.collector",
    tests_require=["nose"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
    ],
)
