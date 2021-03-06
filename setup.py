#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Package setup."""
import os
import sys
from shutil import rmtree

from codecs import open

from setuptools import setup
from setuptools import Command
from setuptools.command.test import test as TestCommand
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
version_path = os.path.join(here, "pytan3", "version.py")


class PyTest(TestCommand):
    """Pass."""

    user_options = [("pytest-args=", "a", "Arguments to pass into py.test")]

    def initialize_options(self):
        """Pass."""
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        """Pass."""
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        """Pass."""
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


class Upload(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Print things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        """Pass."""
        pass

    def finalize_options(self):
        """Pass."""
        pass

    def run(self):
        """Pass."""
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system(  # nosec
            "{0} setup.py sdist bdist_wheel --universal".format(sys.executable)
        )

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")  # nosec

        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(about["__version__"]))  # nosec
        os.system("git push --tags")  # nosec

        sys.exit()


about = {}
with open(version_path, "r", "utf-8") as f:
    x = f.readlines()
    contents = "\n".join(a for a in x if not a.startswith("#"))
    exec(contents, about)  # nosec


with open("README.md", "r", "utf-8") as f:
    readme = f.read()

packages = find_packages()

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    packages=packages,
    package_data={"": ["LICENSE"]},
    package_dir={"pytan3": "pytan3"},
    scripts=[],  # TODO(!)
    include_package_data=True,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=[
        "cert_human",
        "colorama",
        "humanfriendly",
        "privy",
        "requests[security,socks]",
        "six>=1.12.0",
        "xmltodict",
        'pathlib2;python_version<"3.0"',
        "python-dotenv",
    ],
    tests_require=[
        "pytest-httpbin>=0.0.7",
        "pytest-cov",
        "pytest-mock",
        "pytest-xdist",
        "pytest-lazy-fixture",
        "pytest>=2.8.0",
        "httpretty",
        "input_mocker",
    ],
    license=about["__license__"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    cmdclass={"upload": Upload, "test": PyTest},
)
