#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2020/11/17 17:40
    Desc  :
--------------------------------------
"""

import os
import time

from loguru import logger

from autotest.utils.excelUtils import ExcelUtils
from autotest.utils.reportUtils import ReportUtils
from autotest.utils.requestsUtils import RequestsUtils


def run(filepath):
    begin_time = time.strftime("%Y-%m-%d %H:%M:%S")
    startTime = time.time()
    responseList = []
    testPass = 0
    testAll = 0
    testFail = 0
    testError = 0
    testSkip = 0

    dataList = ExcelUtils.read_excel(filepath)
    for i in dataList:
        if int(RequestsUtils(i).isRun) == 0:
            if isinstance(RequestsUtils(i).runCount, float):
                for j in range(int(RequestsUtils(i).runCount)):
                    testAll += 1
                    logger.info(f"--------------------------第{j + 1}次--请求开始--{RequestsUtils(i).apiName}--------------------------")
                    response = RequestsUtils(i).request()
                    responseList.append(response)
                    isPass = RequestsUtils(i).isPass
                    if isPass == 0:
                        testPass += 1
                    elif isPass == 1:
                        testFail += 1
                    elif isPass == 2:
                        testError += 1
        else:
            responseList.append(RequestsUtils(i).skip_response())
            testSkip += 1
            testAll += 1
    totalTime = round(time.time() - startTime, 2)
    summary =  [
        {
            "value": testAll,
            "name": "用例总数"
        },
        {
            "value": testPass,
            "name": "用例通过"
        },
        {
            "value": testFail,
            "name": "用例失败"
        },
        {
            "value": testSkip,
            "name": "用例跳过"
        },
        {
            "value": begin_time,
            "name": "开始时间"
        },
        {
            "value": f'{totalTime}s',
            "name": "耗时"
        }
    ]
    return {
        'responseList': responseList,
        'testAll': testAll,
        'testPass': testPass,
        'testFail': testFail,
        'testError': testError,
        'testSkip': testSkip,
        'summary': summary,
    }


if __name__ == '__main__':
    filepath = os.getcwd() + r"\case\蒙多奇超级后台接口测试.xlsx"

    reponse = run(filepath)
    now = time.strftime("%Y-%m-%d-%H-%M-%S")
    result = ReportUtils(reponse = reponse)
    result.report(title = "蒙多奇超级后台接口测试", filename = now, report_dir = "report")
    # 确保index是最新的
    result.report(title = "蒙多奇超级后台接口测试", filename = "index", report_dir = "report")