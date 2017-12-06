from setuptools import setup, find_packages


setup(name='python-infoblox',
      version='0.4',
      author='Dylan F. Marquis',
      author_email='dylanfmarquis@dylanfmarquis.com',
      description='A wrapper around the Infoblox WAPI',
      url='https://github.com/dylanfmarquis/python-infoblox',
      download_url='https://github.com/dylanfmarquis/python-infoblox/archive/v0.4.0.tar.gz',
      license='MIT',
      packages=find_packages(),
      install_requires=['requests==2.18.4', 'future==0.16.0'],
      keywords=['infoblox', 'wapi']
      )
