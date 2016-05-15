from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    def initialize_options(self):
	TestCommand.initialize_options(self)
	self.test_args = []

    def run_tests(self):
        import pytest
        import sys
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
	name = "Destiny Lore Ebook Generator",
	description = "Destiny Lore ebook generation tool from API accessible info.",
	version = "0.1",
	license = "MIT",
	author_email = "antoniobmmrusso@users.noreply.github.com",
	author = "Antonio Russo",
	keywords = "destiny bungie lore ebook",
	packages = find_packages(),
	cmdclass={"test": PyTest},
	install_requires=[ 'requests' ],
	tests_require=[ 'pytest', 'mock', 'httpretty'],
)
