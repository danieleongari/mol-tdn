#!/usr/bin/env python
from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(packages=find_packages(),
          long_description=open('README.md').read(),
          long_description_content_type='text/markdown',
          name="mol-tdn",
          author="Daniele Ongari",
          author_email="daniele.ongari@gmail.com",
          description="Tools for computing thermodynamic properties of molecular fluids",
          url="https://github.com/danieleongari/mol-tdn",
          license="Creative Commons",
          classifiers=["Programming Language :: Python"],
          version="0.0.1",
          install_requires=["numpy", "pandas"],
          extras_require={"pre-commit": [
              "pre-commit==1.11.0",
              "yapf==0.29.0",
              "prospector==1.2.0",
          ]})
