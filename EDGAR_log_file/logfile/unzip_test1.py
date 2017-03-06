# -*- coding:utf-8 -*-


import os
import time
import datetime
import platform
import os.path
import zipfile
import gc
import multiprocessing as mp


def zip_dir(dirname, zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else:
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        # print arcname
        zf.write(tar, arcname)
    zf.close()


def unzip_file_for_map(zu):
    (zipfilename, unziptodir) = (zu[0], zu[1])
    unzip_file(zipfilename, unziptodir)


def unzip_file(zipfilename, unziptodir):
    if not os.path.exists(unziptodir):
        os.mkdir(unziptodir, 0777)
    zfobj = zipfile.ZipFile(zipfilename)
    for name in zfobj.namelist():
        name = name.replace('\\', '/')

        if name.endswith('/'):
            os.mkdir(os.path.join(unziptodir, name))
        else:
            ext_filename = os.path.join(unziptodir, name)
            ext_dir = os.path.dirname(ext_filename)
            if not os.path.exists(ext_dir):
                os.mkdir(ext_dir, 0777)
            outfile = open(ext_filename, 'wb')
            outfile.write(zfobj.read(name))

            outfile.close()


def unzip_file_extract(zipfilename, unziptodir):
    if not os.path.exists(unziptodir):
        os.mkdir(unziptodir, 0777)
    zfobj = zipfile.ZipFile(zipfilename)
    for name in zfobj.namelist():
        name = name.replace('\\', '/')

        if name.endswith('/'):
            os.mkdir(os.path.join(unziptodir, name))
        else:
            ext_filename = os.path.join(unziptodir, name)
            ext_dir = os.path.dirname(ext_filename)
            if not os.path.exists(ext_dir):
                os.mkdir(ext_dir, 0777)
            #outfile = open(ext_filename, 'wb')
            # outfile.write(zfobj.read(name))
            zfobj.extract(name, path=ext_dir)

            # outfile.close()


def detect_operation_system_symb():
    if "Windows" in platform.system():
        symb = "\\"
    elif "Darwin" in platform.system():
        symb = '/'
    else:
        symb = '/'
    return symb


if __name__ == '__main__':
    unziptodir = raw_input('please enter the dir, connected by comma')
    #zipfilename, unziptodir = w.split(',')[0], w.split(',')[1]
    zipfilename = '/Users/sn0wfree/Documents/python_projects/download-data/logfile/2016/log20160322.zip'

    unzip_file_extract(zipfilename, unziptodir)

    # mutli_unzip

    # child_path

    #    zip_file_list = [
    # zipfff for zipfff in file_list if zipfff.split(".")[-1] == "zip"]
