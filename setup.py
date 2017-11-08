from setuptools import setup, find_packages


setup(name='infoblox',
      version='1.0.0',
      author='Dylan F. Marquis',
      url='https://github.com/dylanfmarquis/python-infoblox',
      license='MIT',
      packages=find_packages(),
      install_requires=['requests==2.18.4']
      )
