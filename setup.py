from setuptools import setup, find_packages
from infoblox.infoblox import __version__, __author__


setup(name='python-infoblox',
      version=__version__,
      author=__author__,
      url='https://github.com/dylanfmarquis/python-infoblox',
      license='MIT',
      packages=find_packages(),
      install_requires=['requests==2.18.4']
      )
