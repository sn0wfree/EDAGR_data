# -*- coding:utf-8 -*-

#-------------------
__version__ = "0.8"
__author__ = "sn0wfree"
'''
this py file can download the index file for each company's filings
'''
#-------------------
import os
import datetime
import sqlite3
import gc
import requests

import requests_cache
from enum import Enum
import multiprocessing as mp


class Qtr(Enum):
    # initial quarter
    QTR1 = 1
    QTR2 = 2
    QTR3 = 3
    QTR4 = 4

    def describe(self):
        # Describe the member with name and value
        return self.name, self.value

    def QuarterViewStr(self):
        #
        if self.value == 1:
            print ("this is the %sst quarter") % self.value
        elif self.value == 2:
            print ("this is the %snd quarter") % self.value
        elif self.value == 3:
            print ("this is the %srd quarter") % self.value
        elif self.value == 4:
            print ("this is the %sth quarter") % self.value
        else:
            print "un-recogizated Quarter"

    def TranslateQuarter(self, date):
        if isinstance(date, tuple) or isinstance(date, list):
            if len(date) >= 2:
                test_quarter = date[1]
                quarter = (test_quarter - 1) / 3 + 1
                return quarter
            else:

                raise "un-recogizated Quarter"
        else:
            print '''No-tuple or No-list type detected,
                    please use list or tuple type pf date,
                    like (2017,1,1) or [2017,1,1]
                    '''
            raise "un-included type detected"


class rNN_process_delete_invald_space():
    # initial valid characher scaner

    def __init__(self, dict_string):
        self.import_string = dict_string
        self.Good = ['010', '011', '110', '111', '101']
        # self.temp_string = {}
        self.output_string = {}

    def TranslateIntoMethod(self, string):
        string_trans = ''
        for i in xrange(len(string)):
            if string[i] == " ":
                string_trans += '0'
            elif string[i] != " ":
                string_trans += '1'
        return string_trans

    def translate(self):

        target_keys = self.import_string.keys()
        for target_key in target_keys:
            temp_string = self.TranslateIntoMethod(
                self.import_string[target_key])
            temp_signal = ['0'] * len(temp_string)
            if temp_string[0] == '1':
                temp_signal[0] = '1'

            elif temp_string[0] == '0':
                temp_signal[0] = '0'

            if temp_string[-1] == '1':
                temp_signal[-1] = '1'

            elif temp_string[-1] == '0':
                temp_signal[-1] = '1'

            for w in xrange(1, len(temp_string) - 1):
                temp_singal_for_scan = temp_string[
                    w - 1] + temp_string[w] + temp_string[w + 1]
                if temp_singal_for_scan in self.Good:
                    temp_signal[w] = '1'
                else:
                    temp_signal[w] = '0'
            self.output_string[target_key] = ''
            for signal_d in xrange(len(temp_signal)):
                if temp_signal[signal_d] == '1':
                    self.output_string[
                        target_key] += self.import_string[target_key][signal_d]
                else:
                    pass

        return self.output_string


class now_info_date():

    def __init__(self):
        self.start_date = (1993, 1, 1)
        self.start_quarter = 1

        self.current_date = (datetime.date.today().year, datetime.date.today(
        ).month,  datetime.date.today().day)
        self.current_quarter = (datetime.date.today().month - 1) / 3 + 1
        self.years = xrange(self.start_date[0], self.current_date[0])

    def year_quarter_list(self):

        temp_current_year_quarter = [(self.current_date[0], quarter)
                                     for quarter in Qtr.__members__.keys() if Qtr[quarter].value <= self.current_quarter]
        # print temp_current_year_quarter
        target_year_quarter_list = [(year, quarter)
                                    for year in self.years for quarter in Qtr.__members__.keys()]

        target_year_quarter_list.extend(temp_current_year_quarter)

        return target_year_quarter_list


def read_idx_file(url):

    lines = requests.get(url[0]).text.splitlines()
    allrecords = [list(line.split('|')) for line in lines]

    title_dict = rNN_process_delete_invald_space({a[0].split(": ")[0]: a[0].split(": ")[1]
                                                  for a in allrecords[0:5]}).translate()

    field_name = allrecords[9]
    field_name.extend([unicode('Url'), unicode('Accession')])

    content = allrecords[11:]
    main_domin = 'https://www.sec.gov/Archives/'
    for a in content:
        a.extend([unicode(main_domin + a[-1]),
                  unicode(a[4].split("/")[-1].split(".")[0])])

    # print content[1], len(field_name), len(content[1])
    # print '%s,%s,%s,%s,%s,%s,%s' % (tuple(field_name))
    return (title_dict, field_name, content)


class create_database_sqlite():

    def __init__(self, database_sqlite_name, url, field_name):
        self.sqlite_name = database_sqlite_name
        self.url = url
        self.field_name = field_name

    def create_database_file(self):
        conn = sqlite3.connect(self.sqlite_name)

        cur = conn.cursor()

        cur.execute('DROP TABLE IF EXISTS %s;' %
                    (self.url[1][1] + 'of' + str(self.url[1][0])))

        cur.execute('CREATE TABLE %s' % (self.url[1][1] + 'of' + str(self.url[1][0])) + '(%s TEXT, %s TEXT, %s TEXT, %s TEXT, %s TEXT, %s TEXT, %s TEXT)' % (
            tuple(field_name)))

        cur.executemany('INSERT INTO %s VALUES' % (str(self.url[1][
                        1] + 'of' + str(self.url[1][0]))) + ' (?, ?, ?, ?, ?, ?, ?)', content)
        conn.commit()
        conn.close()


if __name__ == '__main__':
    gc.enable

    # requests_cache initial
    requests_cache.install_cache(
        cache_name="EDGAR_filings_request_cache", backend="sqlite", expire_date=1800)
    main_domin = 'https://www.sec.gov/Archives/'

    # generate the target urls
    urls = [('https://www.sec.gov/Archives/edgar/full-index/%d/%s/master.idx' % (year, quarter), (year, quarter))
            for year, quarter in now_info_date().year_quarter_list()]
    # print urls[1]

    # locate the path
    locals_file_path = os.path.split(os.path.realpath(__file__))[0]
    # create sqlite database

    for url in urls:
        # https://www.sec.gov/Archives/edgar/data/60512/0000060512-94-000005.txt

        (title_dict, field_name, content) = read_idx_file(url)

        create_database_sqlite('edgar_idx.db', url,
                               field_name).create_database_file()
        gc.collect

        print '%s %s idx download completed' % (url[1][0], url[1][1])

        # field_name = ['CIK', 'Company Name', 'Form Type', 'Date Filed',
        # 'Filename']
