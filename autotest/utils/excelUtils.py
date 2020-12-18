#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2020/11/19 14:04
    Desc  :
--------------------------------------
"""

import xlrd


class ExcelUtils:

    @staticmethod
    def read_excel(filepath):
        """
        读取excel'
        :return:
        """

        data = xlrd.open_workbook(filepath)

        # 获取sheet
        table = data.sheets()[0]

        # 获取总行数
        nrows = table.nrows

        info_list = []

        # 遍历每行数据
        for row in range(1, nrows):
            info_list.append(table.row_values(row))

        # print(info_list)

        return info_list
