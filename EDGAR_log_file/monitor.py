# -*- coding:utf-8 -*-


#-------------------
__version__ = "1.0"
__author__ = "sn0wfree"
#-------------------
import urllib2
import sys
import os
import urllib
import random
import time
import datetime
import platform
import gc
import download2 as download
import multiprocessing as mp


def path_based_by_system(download_file_path, year):
    sys_info = platform.system()
    if "Windows" in sys_info:
        temp_symbol = "\\"
    elif "Darwin" in sys_info:
        temp_symbol = "/"
    else:
        temp_symbol = "/"

    txt_path = download_file_path + temp_symbol + year + ".txt"
    return txt_path_based_by_system


def read_text_file(file):
    with open(file, 'r') as file_file:
        file_list = file_file.readlines()
        return file_list
if __name__ == "__main__":

    chrome = 'Mozilla/5.0 (X11; Linux i86_64) AppleWebKit/537.36 ' + \
        '(KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
    headers = {'User-Agent', chrome}

    check_url = "https://www.sec.gov/files/edgar_logfile_list.html"
    #content = urllib2.urlopen(check_url).read()
    req = urllib2.Request(check_url)  # sent request form

    response = urllib2.urlopen(req)  # recevie feedback data
    content = response.readlines()  # read it
    all_target_url = []
    for url in content:
        if "www.sec.gov/dera/data/Public-EDGAR-log-file-data/" in url:
            url = url.split(".zip")[0] + ".zip"
            all_target_url.append(url)

    year = str(datetime.datetime.now()).split("-")[0]
    this_year_urls = [
        urls for urls in all_target_url if urls.split("/")[-3] == year]
    print this_year_urls
    download_file_path = raw_input(
        "please type in the storage path of this year data")
    txt_file_path = path_based_by_system(download_file_path, year)
    file_list = read_text_file(txt_file_path)
