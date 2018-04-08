#!/usr/bin/python3
# coding=utf-8

import xlrd
import logging
import requests
import sys
import time
from dbio import DBIO


class Exporter:
    def __init__(self, baseurl, dbio):
        self.logger = logging.getLogger("cnzz_crawler.exporter")        
        # base url was http://icp.chinaz.com/saveExc.ashx
        self.baseurl = baseurl
        self.total = 0
        self.db = dbio
    
    def analyse_xls(self, xls_data):
        xls = xlrd.open_workbook(file_contents = xls_data)
        x_table = xls.sheets()[0]
        if x_table.nrows > 0:
            count = 0
            for i in range(2, x_table.nrows):
                try:
                    self.db.write(x_table.row_values(i))
                    count += 1
                except:
                    pass
            return count
        else:
            return 0

    def get_province(self, province, start_date):
        subtotal = 0
        self.logger.info('Getting province of %s' % province)
        # date must be YYYYMMDD
        try:
            start_asc_time = time.mktime(time.strptime(start_date,'%Y%m%d'))
        except:
            self.logger.error('Time format error!')
            return
        self.get_para = {
            '_host': '',
            '_companyName': '',
            '_companyXZ': '不限',
            '_wname': '',
            '_provinces': province,
            '_btime': '',
            '_etime': '',
            '_page': '',
            'saveData': '导出所有结果'
        }
        while start_asc_time < time.time():
            start_str_time = time.strftime('%Y-%m-%d', time.localtime(start_asc_time))
            print('Processing %s...' % start_str_time, end = '')
            self.get_para['_btime'] = start_str_time
            self.get_para['_etime'] = start_str_time
            try:
                ret_xls = requests.post(self.baseurl, data = self.get_para).content
            except:
                self.logger.error('Network error!')
                return
            count = self.analyse_xls(ret_xls)
            self.total += count
            subtotal += count
            print(' returned %d results. %d results in total.' % (count, self.total), end = '\r')
            # add one day to time
            start_asc_time += (3600*24)

        self.logger.info('Got %d results from %s' % (subtotal, province))



