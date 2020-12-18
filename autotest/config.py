#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2020/11/18 8:55
    Desc  :
--------------------------------------
"""

# 基础url
BASE_URL = "http://testapi.mondoq.cn"

# token
ACCESSTOKEN = ''

# 用户名
USERNAME = "admin"
# 密码
PASSWORD = "741A627471982D84D67177464D006A01"

# 全局请求头
HEADERS = {
    "Authorization": 'Bearer {}'
}

# excel列表结果
EXCEL_INFO = {
    'index': 0,         # 第一位为序号
    'apiName': 1,       # 接口名称
    'apiPath': 2,       # 接口地址
    'apiMehtod': 3,     # 请求方法
    'apiParam': 4,      # 接口参数
    'extract': 5,       # 提取参数
    'assertPatam': 6,   # 断言字段
    'assertValue': 7,   # 断言值
    'isRun': 8,         # 是否执行
    'isHeaders': 9,      # 是否带请求头
    'runCount': 10,      # 是否带请求头
}


# 用来存提取的变量的
EXTRACT_VARIABLE = {
    "username": USERNAME,
    "password": PASSWORD,
}

# 用户状态
CASE_STATUS = {
    100: "PASS",
    101: "FAIL",
    102: "ERROR",
    103: "SKIP",
}