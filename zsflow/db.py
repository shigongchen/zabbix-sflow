# -*- coding: utf-8 -*-

import datetime
import sqlite3


class DB(object):

    def __init__(self, name):
        self.name = name

    def get_conn(self):
        return sqlite3.connect(self.name)

    def init(self):
        conn = self.get_conn()
        c = conn.cursor()
        for tbname in ("TCP", "UDP", "ARP"):
            sql = ("DROP TABLE IF EXISTS {t}".format(t=tbname))
            c.execute(sql)
            sql = ("CREATE TABLE IF NOT EXISTS "
                   "{t}(src_ip text, src_port integer, "
                   "dest_ip text, dest_port integer, "
                   "datetime text) ".format(t=tbname))
            c.execute(sql)
            sql = ("CREATE INDEX IF NOT EXISTS idx_datetime ON "
                   "{t}(datetime)".format(t=tbname))
            c.execute(sql)
            conn.commit()
        sql = "DROP TABLE IF EXISTS STATUS"
        c.execute(sql)
        sql = ("CREATE TABLE IF NOT EXISTS STATUS( "
               "status text, src_ip, text, src_port integer, "
               "dest_ip text, dest_port integer, datetime text, "
               "type text)")
        c.execute(sql)
        c.close()
        conn.close()

    def reset_db(self):
        self.init()

    def record(self, tbname, src_ip, src_port, dest_ip, dest_port):
        conn = None
        c = None
        try:
            conn = self.get_conn()
            c = conn.cursor()
            sql = ("INSERT INTO {tbname}(src_ip, src_port, dest_ip, "
                   "dest_port, datetime) VALUES ('{src_ip}', {src_port}, "
                   "'{dest_ip}', {dest_port}, '{dt}')".format(
                tbname=tbname,
                src_ip=src_ip,
                src_port=src_port,
                dest_ip=dest_ip,
                dest_port=dest_port,
                dt=datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S'),
            ))
            c.execute(sql)
            conn.commit()
        except Exception as e:
            print(str(e))
        finally:
            if c:
                c.close()
            if conn:
                conn.close()

    def query_status(self, tbname, begin_date, end_date):
        conn = None
        c = None
        try:
            conn = self.get_conn()
            c = conn.cursor()
            sql = ("SELECT * FROM {t} WHERE datetime > '{b}' "
                   "AND datetime <= '{e}'".format(
                t=tbname,
                b=begin_date.strftime('%y-%m-%d %H:%M:%S'),
                e=end_date.strftime('%y-%m-%d %H:%M:%S')
            ))
            c.execute(sql)
            return c.fetchall()
        except Exception as e:
            print(str(e))
        finally:
            if c:
                c.close()
            if conn:
                conn.close()


if __name__ == "__main__":
    db = DB("a.db")
    db.init()
