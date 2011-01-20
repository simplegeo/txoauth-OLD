#!/usr/bin/env python
# coding: utf-8

import os, re
from setuptools import setup, find_packages

PKG='txoauth'
VERSIONFILE = os.path.join('txoauth', '_version.py')
verstr = "unknown"
try:
    verstrline = open(VERSIONFILE, "rt").read()
except EnvironmentError:
    pass # Okay, there is no version file.
else:
    MVSRE = r"^manual_verstr *= *['\"]([^'\"]*)['\"]"
    mo = re.search(MVSRE, verstrline, re.M)
    if mo:
        mverstr = mo.group(1)
    else:
        print "unable to find version in %s" % (VERSIONFILE,)
        raise RuntimeError("if %s.py exists, it must be well-formed" % (VERSIONFILE,))
    AVSRE = r"^auto_build_num *= *['\"]([^'\"]*)['\"]"
    mo = re.search(AVSRE, verstrline, re.M)
    if mo:
        averstr = mo.group(1)
    else:
        averstr = ''
    verstr = '.'.join([mverstr, averstr])

trove_classifiers=[
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: BSD License",
    "License :: DFSG approved",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Natural Language :: English",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.5",
    "Programming Language :: Python :: 2.6",
    "Topic :: Utilities",
    "Topic :: Software Development :: Libraries",
    ]

setup(
    name="txoauth",
    version=verstr,
    description="provides OAuth 2.0 support for Twisted.",
    author="Zooko Ofsimplegeo", # original author: Laurens Van Houtven
    author_email="zooko@simplegeo.com",
    url="https://github.com/simplegeo/txoauth",
    packages = find_packages(),
    test_suite="txoauth.test",
    install_requires=["Twisted >= 9.0.0"],
    setup_requires=['setuptools_trial'],
    tests_require=['mock'],
    license = "BSD",
    classifiers=trove_classifiers,
    zip_safe = False, # We prefer unzipped for easier access.
)
