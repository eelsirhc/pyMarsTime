#!/usr/bin/env python

from setuptools import setup

setup(name="marstime",
      version='0.4.2',
      description='marstime library, implements the Mars24 algorithm [Allison and McEwan, 2000]',
      author="Christopher Lee",
      url="http://code.foldmountain.com/marstime",
      download_url="https://bitbucket.org/eelsirhc/marstime/downloads",
      author_email="lee@foldmountain.com",
      packages=["marstime"],
      license="LICENSE.txt",
      setup_requires=["setuptools"],
      long_description=open("README.txt").read(),
      classifiers=["License :: OSI Approved :: BSD License",
                  "Intended Audience :: Science/Research",
                  "Programming Language :: Python :: 2.7",
                  "Topic :: Scientific/Engineering :: Astronomy"],
      zip_safe=True,
)
