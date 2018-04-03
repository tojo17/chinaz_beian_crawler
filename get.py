#!/usr/bin/python3
# coding=utf-8

from exporter import Exporter
from dbio import DBIO
import logging
import argparse

def init_logger():
    logger = logging.getLogger("cnzz_crawler")    
    logger.setLevel(logging.DEBUG)
    # logger.setLevel(logging.INFO)
    log_handler = logging.StreamHandler()
    logger.addHandler(log_handler)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)
    return logger

provinces = ["京","津","冀","晋","蒙","辽","吉","黑","沪","苏","浙","皖","闽","赣","鲁","豫","鄂","湘","粤","桂","琼","渝","蜀","黔","滇","藏","陕","陇","青","宁","新"]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database', required = True, help = 'SQLite database name')
    parser.add_argument('-s', '--startdate', required = True, help = 'start date (YYYYMMDD)')
    parser.add_argument('-p', '--province', help = 'the province to get, if not assigned crawl all')
    args = parser.parse_args()

    db = DBIO(args.database)
    ex = Exporter('http://icp.chinaz.com/saveExc.ashx', db)
    if args.province:
        ex.get_province(args.province, args.startdate)
    else:
        for prov in provinces:
            ex.get_province(prov, args.startdate)
    
    

