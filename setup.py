from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in pawnshop_management/__init__.py
from pawnshop_management import __version__ as version

setup(
	name="pawnshop_management",
	version=version,
	description="Pawnshop Management System",
	author="Rabie Moses Santillan",
	author_email="gprabiemosessantillan@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
