#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2020/11/20 16:19
    Desc  :
--------------------------------------
"""
import json
import os
from loguru import logger


class PATH:
    template_path = os.path.join(os.path.dirname(__file__), 'template')
    config_tmp_path = os.path.join(template_path, 'template.html')


class ReportUtils(PATH):
    """
    生成测试报告类
    """

    def __init__(self, reponse: dict):
        """
        :param title: 报告标题
        :param report_dir: 报告存储路径
        :param filename: 文件名
        :param reponse: 测试报告列表
        """
        self.title = "接口自动化测试报告"
        self.report_dir = None
        self.filename = 'report.html'
        self.reponse = reponse
        logger.debug(reponse)

    def report(self, title, filename: str = None, report_dir='.'):
        """
        生成测试报告,并放在当前运行路径下
        :param title: 标题
        :param report_dir: 报告存放目录
        :param filename: 生成文件的名字
        :return:
        """

        if filename:
            self.filename = filename if filename.endswith(".html") else filename + '.html'

        if title:
            self.title = title

        self.report_dir = os.path.abspath(report_dir)
        os.makedirs(self.report_dir, exist_ok = True)
        self.output_report()
        text = '\n测试已全部完成, 可打开 {} 查看报告'.format(os.path.join(self.report_dir, self.filename))
        print(text)

    def output_report(self):
        """
        生成测试报告到指定路径
        :return:
        """

        def render_template(param: dict, template: str):
            for name, value in param.items():
                name = "${" + name + "}"
                template = template.replace(name, value)
            return template

        template_path = self.config_tmp_path
        render_params = {
            'resultData': json.dumps(self.reponse, ensure_ascii = False, indent = 2),
            'title': self.title,
        }

        override_path = os.path.abspath(self.report_dir) if \
            os.path.abspath(self.report_dir).endswith('/') else \
            os.path.abspath(self.report_dir) + '/'

        with open(template_path, 'rb') as file:
            body = file.read().decode('utf-8')

        with open(override_path + self.filename, 'w', encoding = 'utf-8', newline = '\n') as write_file:
            html = render_template(render_params, body)
            write_file.write(html)
