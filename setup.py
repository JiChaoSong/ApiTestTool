#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2020/12/18 14:05
    Desc  :
--------------------------------------
"""

from setuptools import find_packages, setup
setup(
    name='ApiTestTool',
    version='1.0.0',
    description = '接口测试工具',
    author = 'jichaosong',
    author_email = 'jichaosong@outlook.com',
    url='https://github.com/JiChaoSong/ApiTestTool.git',
    packages = ['autotest'],
    install_requires = [
        'loguru==0.5.3',
        'xlrd==1.2.0',
        'Faker==4.15.0',
        'requests==2.25.0',
    ],
)