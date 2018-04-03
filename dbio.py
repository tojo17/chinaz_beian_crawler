#!/usr/bin/python3

import logging
import sqlite3
import datetime

class DBIO:
    'open db for io'
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.logger = logging.getLogger("cnzz_crawler.dbio")
        self.logger.info("Database connected successfully.")

    def write(self, domain_row):
        self.logger.debug("Writing domain data...")
        cu = self.conn.cursor()
        # if duplicate data, write will return an exception
        cu.execute('INSERT INTO domains_icp (domain, owner_name, owner_type, icp_cert, site_name, homepage, time, update_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (
            domain_row[1], domain_row[2], domain_row[3], domain_row[4], domain_row[5], domain_row[6], domain_row[7],
            datetime.datetime.now()))
        self.conn.commit()
        
    def close(self):
        self.conn.close()
