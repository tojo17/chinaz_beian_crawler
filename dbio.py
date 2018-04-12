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
        self.count = 0
        
    def write_data(self, rows):
        count = 0
        self.logger.debug("Writing domain data...")
        cu = self.conn.cursor()
        for index in range(0, len(rows)):
            if index % 100 == 0:
                print('\rWritting %.2f %%, %d of %d' %
                      (100*(index+1)/len(rows), index+1, len(rows)), end='')
            try:
                domain_row = rows[index]
                # if duplicate data, write will return an exception
                cu.execute('INSERT INTO domains_icp (domain, owner_name, owner_type, icp_cert, site_name, homepage, time, update_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (
                    domain_row[1], domain_row[2], domain_row[3], domain_row[4], domain_row[5], domain_row[6], domain_row[7],
                    datetime.datetime.now()))
                count += 1
            except:
                pass
        self.conn.commit()
        self.count += count
        print('\t' * 12, end = '\r')
        return count

    def close(self):
        self.logger.info('%d data written to DB in total.' % self.count)
        self.conn.close()
