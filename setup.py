from setuptools import setup, find_packages

setup(name='samples',
      version='1.0',
      description='Simple sample class used for parsing',
      author='Eric Ulrich',
      packages=['samples'],
      package_data={'samples':['sample_sheet.csv']}
     )
