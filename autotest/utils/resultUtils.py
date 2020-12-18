#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2020/11/18 11:29
    Desc  :
--------------------------------------
"""


class ResultUtils(object):
    """
    单条测试结果-字典
    """

    def __init__(self, data: list, status: str, errors=None, response = None):
        self.data = data
        self.status = status
        self.errors = errors
        self.response = response

    def result(self):
        apiInfo = {
            'apiName': self.data[1],
            'apiPath': self.response.request.url,
            'apiMethod': self.response.request.method,
            'apiParam': self.response.request.body,
            'apiHeaders': self.response.request.headers,
            }

        # del apiInfo['content']
        res = {
            "apiInfo": apiInfo,
            "status": self.status,
            "response": self.response.text,
            "errors": self.errors
        }

        if self.errors is None:
            del res['errors']

        return res
