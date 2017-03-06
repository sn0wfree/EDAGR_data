# -*- coding:utf-8 -*-
#-------------------
__version__ = "1.0"
__author__ = "sn0wfree"
#-------------------
import urllib
import os
import urllib2

import requests


def initial_headers_FILE():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux i86_64) AppleWebKit/537.36 ' + '(KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
    }
    return headers


if __name__ == "__main__":
    watching_url = 'https://www.sec.gov/files/edgar_logfile_list.html'
