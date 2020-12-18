#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2020/11/19 14:46
    Desc  :
--------------------------------------
"""
import json
import re

import jsonpath
import requests
from autotest.config import *
from loguru import logger


def get_jsonPath(result, value, index=0):
    """
    获取jsonpath的值  默认获取第一个
    :param result: requests格式
    :param value:  需要获取的值
    :param index:  需要获取的值的下标
    :return:
    """
    return jsonpath.jsonpath(result.json(), value)[index]


class BaseRequests:

    def __init__(self, excelData: list):
        """
        初始化
        :param excelData: excel一行数据
        """
        # 接口名称
        self.apiName = excelData[EXCEL_INFO.get('apiName')]
        # 接口地址
        self.apiPath = excelData[EXCEL_INFO.get('apiPath')]
        # 请求方法
        self.apiMethod = excelData[EXCEL_INFO.get('apiMehtod')]
        # 请求参数
        self.apiParam = excelData[EXCEL_INFO.get('apiParam')]
        # 提取参数
        self.extract = excelData[EXCEL_INFO.get('extract')]
        # 断言字段
        self.assertPatam = excelData[EXCEL_INFO.get('assertPatam')]
        # 执行次数
        self.runCount = excelData[EXCEL_INFO.get('runCount')]

        # 断言字段的值
        self.assertValue = int(excelData[EXCEL_INFO.get('assertValue')]) if excelData[EXCEL_INFO.get(
            'assertValue')] != "" else excelData[EXCEL_INFO.get('assertValue')]
        # 是否执行
        self.isRun = excelData[EXCEL_INFO.get('isRun')]
        # 是否带请求头
        self.isHeaders = excelData[EXCEL_INFO.get('isHeaders')]

        # 存取测试结果
        self.responseList = []

        # 各种状态得数量 0通过， 1失败， 2跳过， 3错误
        self.isPass = 0

    def set_url(self):
        """
        设置url
        :return: url
        """
        return BASE_URL + self.apiPath

    def set_apiParam(self):
        """
        设置请求参数
        :return: self.apiParam
        """
        if self.apiParam != "":
            apiParam = json.loads(self.apiParam)
            for i in apiParam:
                if len(self.get_re_result(apiParam[i])) != 0:
                    for j in self.get_re_result(apiParam[i]):
                        if 'random' in j:
                            apiParam[i] = eval(j)()
                        else:
                            apiParam[i] = self.get_extract(j)
            self.apiParam = apiParam
        else:
            self.apiParam = None

    def set_result(self, result=None, **kwargs):
        """
        构造返回结果
        :param result: request格式
        :return: dict
        """
        if result is None:
            apiInfo = dict(apiName = self.apiName,
                           apiPath = str(kwargs.get("apiPath")),
                           apiMethod = result,
                           apiParam = str(kwargs.get("apiParam")),
                           apiHeaders = result
                           )
            response = result
            costTime = None
        else:
            response = result.text
            costTime = result.elapsed.total_seconds()
            apiInfo = dict(apiName = self.apiName,
                           apiPath = str(kwargs.get("apiPath")),
                           apiMethod = result.request.method,
                           apiParam = str(kwargs.get("apiParam")),
                           apiHeaders = dict(result.request.headers)
                           )

        return dict(apiInfo = apiInfo, status = kwargs.get('status'), response = response,
                    errors = kwargs.get('errors'), costTime = costTime)

    def assert_result(self, result):
        """
        断言结果
        :param result: requests格式
        :return: bool
        """
        try:
            if self.assertPatam != "":
                assertResult = get_jsonPath(result, self.assertPatam)

                # 构造断言结果字段
                assertDict = {
                    "预期结果": f"{self.assertPatam[3:]}={self.assertValue}",
                    "实际结果": f"{self.assertPatam[3:]}={assertResult}",
                }

                logger.info(f"断言结果--{assertDict}")
                if assertResult == self.assertValue:
                    self.isPass = 0
                    return 100
                else:
                    self.isPass = 1
                    return 101
        except Exception as e:
            self.isPass = 3
            logger.error(f'断言错误--{e}')
            return 102

    def set_extract(self, result):
        """
        设置提取的变量
        :return:
        """
        extract = ''
        try:
            if self.extract != '':
                for i in eval(self.extract):
                    extract = i
                    EXTRACT_VARIABLE[i] = get_jsonPath(result, f"$..{i}")
        except Exception as e:
            logger.error(f'参数提取失败--{extract}--{e}')

    def set_headers(self, **kwargs):
        """
        设置请求头
        :return:
        """
        headers = dict(accesstoken = self.get_extract('accesstoken'), root = self.get_extract("organize"))
        if self.isHeaders == 0:
            # logger.info(f"请求头--{dict(headers, **kwargs)}")
            return dict(headers, **kwargs)

        else:
            return kwargs

    @staticmethod
    def get_re_result(result):
        """
        正则替换请求参数变量
        :param result:
        :return:
        """
        return re.compile("{{(.*?)}}").findall(str(result))

    @staticmethod
    def get_extract(value):
        """
        获取提取变量的值
        :return:
        """
        return EXTRACT_VARIABLE.get(value)


class RequestsUtils(BaseRequests):

    def __init__(self, excelData: list):
        """
        初始化
        :param excelData: excel一行数据
        """
        # 接口名称
        super().__init__(excelData)

    def post(self, **kwargs):
        return requests.post(url = self.set_url(), data = self.apiParam, headers = self.set_headers(**kwargs))

    def get(self, **kwargs):
        return requests.get(url = self.set_url(), params = self.apiParam, headers = self.set_headers(**kwargs))

    def get_request(self):

        return {
            'post': self.post(),
            'get': self.get(),
        }

    def response(self, result, status:int):

        return self.set_result(result, status = CASE_STATUS[status], apiParam = self.apiParam,
                               apiPath = self.apiPath)

    def skip_response(self):

        return self.set_result(status = CASE_STATUS[103], apiParam = self.apiParam, apiPath = self.apiPath)

    def request(self):
        """
        发起请求入口
        :return: dict
        """
        # 1. 设置请求参数
        self.set_apiParam()

        # 2. 请求开始
        result = self.get_request().get(self.apiMethod)
        logger.info(f"请求参数--{self.apiParam}")
        logger.info(f"响应内容--{result.text}")

        # 3. 参数提取
        self.set_extract(result)

        # 4. 断言
        assertResult = self.assert_result(result)

        # 5. 返回结果
        response = self.response(result, assertResult)
        return response