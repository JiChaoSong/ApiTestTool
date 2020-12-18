#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2020/11/17 18:23
    Desc  :
--------------------------------------
"""
from faker import Faker

f = Faker('zh-cn')


def random_name():
    """
    随机用户名
    :return:
    """

    return f.name()


def random_phone():
    """
    随机手机号
    :return:
    """

    return f.phone_number()


def random_id_card():
    """
    随机身份证号
    :return:
    """

    return f.ssn()


def random_country():
    """
    随机国家
    :return:
    """

    return f.country()


def random_address():
    """
    随机详细地址
    :return:
    """

    return f.address()


def random_int(*args):
    """
    随机是数字, 默认范围为0-9999, 可通过min,max参数修改
    :param args:
    :return:
    """

    return f.random_int(args)


def random_user_name():
    """
    随机用户名
    :return:
    """

    return f.user_name()


def random_job():
    """
    随机职位
    :return:
    """

    return f.job()


def random_paragraph():
    """
    随机生成段落
    :return:
    """

    return f.paragraph()


def random_sentence():
    """
    随机生成一句话
    :return:
    """

    return f.sentence()


def random_article():
    """
    随机一篇文章
    :return:
    """

    return f.text()


def random_word():
    """
    随机词语
    :return:
    """

    return f.word()


def random_user_agent():
    """
    随机user_agent
    :return:
    """

    return f.user_agent()


def random_email():
    """
    随机邮箱
    :return:
    """

    return f.email()


def random_postcode():
    """
    随机邮编
    :return:
    """

    return f.postcode()


def random_company():
    """
    随机公司名
    :return:
    """

    return f.company()


if __name__ == '__main__':
    print(random_name())
    print(random_phone())
