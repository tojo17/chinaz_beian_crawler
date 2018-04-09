#!/usr/bin/python3
# coding=utf-8

import xlrd
import logging
import requests
import sys
import time
import multiprocessing.dummy
from dbio import DBIO


class Exporter:
    def __init__(self, baseurl, dbio, threads):
        self.logger = logging.getLogger("cnzz_crawler.exporter")
        # base url was http://icp.chinaz.com/saveExc.ashx
        self.baseurl = baseurl
        self.db = dbio
        self.threads = threads

    def write_data(self, rows):
        count = 0
        for row in rows:
            try:
                self.db.write(row)
                count += 1
            except:
                pass
        return count

    def analyse_xls(self, xls_data):
        xls = xlrd.open_workbook(file_contents=xls_data)
        x_table = xls.sheets()[0]
        if x_table.nrows > 1:
            ret = []
            for i in range(2, x_table.nrows):
                ret.append(x_table.row_values(i))
            print(' returned %d results.' % (len(ret)))
            return ret
        else:
            return []

    def fetch(self, start_str_time):
        self.get_para['_btime'] = start_str_time
        self.get_para['_etime'] = start_str_time
        print('\rProcessing %s' % start_str_time, end='')
        try:
            ret_xls = requests.post(self.baseurl, data=self.get_para).content
        except:
            self.logger.error('Network error!')
            return []
        return self.analyse_xls(ret_xls)

    def get_province(self, province, start_date):
        self.logger.info('Getting province of %s' % province)
        # date must be YYYYMMDD
        try:
            start_asc_time = time.mktime(time.strptime(start_date, '%Y%m%d'))
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
        thread_pool = multiprocessing.dummy.Pool(processes = self.threads)
        results = []
        while start_asc_time < time.time():
            start_str_time = time.strftime(
                '%Y-%m-%d', time.localtime(start_asc_time))
            results.append(thread_pool.apply_async(
                self.fetch, args = (start_str_time,)))
            # add one day to time
            start_asc_time += (3600*24)
        thread_pool.close()
        thread_pool.join()
        domain_data = []
        for result in results:
            domain_data += result.get()
        self.logger.info('Got %d results from %s' % (len(domain_data), province))
        written_count = self.write_data(domain_data)
        self.logger.info('%d results written' % (written_count))
        
