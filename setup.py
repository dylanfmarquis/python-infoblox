from setuptools import setup, find_packages


setup(name='python-infoblox',
      version="0.3",
      author="Dylan F. Marquis",
      url='https://github.com/dylanfmarquis/python-infoblox',
      license='MIT',
      packages=find_packages(),
      install_requires=['requests==2.18.4', 'future==0.16.0']
      )
