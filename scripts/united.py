#! /usr/bin/env python

# -*- coding=utf-8 -*-

# ---

# @Author:wensheng.yu

# @File:test1.py

# @Time:2023年04月03日

# ---

import SqlQueryBase

 

class SqlInterfaceCtAspects:

 

  def __init__(self, series_instance_uid1, series_instance_uid2, series_instance_uid3, series_instance_uid4):

        """

        初始化

        param page: 网页

        param key_info: 患者编号或检查号

        """

    self.series_instance_uid1 = series_instance_uid1

         self.series_instance_uid2 = series_instance_uid2

        self.series_instance_uid3 = series_instance_uid3

        self.series_instance_uid4 = series_instance_uid4

 

    def get_aspects_summary_result(self, series_instance_uid1, series_instance_uid2):

        """

        通过seriseUID获取查询脑缺血左右大脑评分的基本信息

        """

        sql = f"SELECT SummaryScore " \

              f"FROM ct_head_aspects_summary where SeriesInstanceUID = '{series_instance_uid1}';"

        sql = f"SELECT SummaryScore " \

              f"FROM ct_head_aspects_summary where SeriesInstanceUID = '{series_instance_uid2}';"

        results = SqlQueryBase().query('ct_head', sql)

        list_results = results[0]

        summary_score = list_results["SummaryScore"]

        summary_score = eval(summary_score)

        left_score = summary_score["left"]

        return left_score

 

series_instance_uid1 = 1

series_instance_uid2 = 2

series_instance_uid3 = 3

series_instance_uid4 = 4

sql = SqlInterfaceCtAspects()

left_score = sql.get_aspects_summary_result(series_instance_uid1, series_instance_uid2, series_instance_uid3)

print(left_score)

left_score1 = sql.get_aspects_summary_result(series_instance_uid1, series_instance_uid2, series_instance_uid3, series_instance_uid4)

print(left_score1)