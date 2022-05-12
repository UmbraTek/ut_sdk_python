#!/usr/bin/env python3
#
# Copyright (C) 2022 UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================

from setuptools import setup, find_packages
import os

long_description = "long description for ut_sdk_python"

with open(os.path.join(os.getcwd(), 'requirements.txt')) as f:
    requirements = f.read().splitlines()

setup(
    name="ut_sdk_python",
    version="1.10",

    description="umbratek sdk for python",
    url="https://github.com/UmbraTek/ut_sdk_python",
    author="Jimy",
    author_email="jimy.zhang@umbratek.com",

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="umbratek,utra,opti,adra,datalink,fido",
    packages=find_packages(),
    python_requires='>=3.5, <4',
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
)
