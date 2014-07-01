import glob

from setuptools import setup, find_packages

setup(
      name='sunpy-ginga',
      version='0.1dev',
      packages=find_packages(),
      scripts=glob.glob('./scripts/*')
     )
