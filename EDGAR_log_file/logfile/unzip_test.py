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


def unzip_file_extractall(zipfilename, unziptodir):
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
            print ext_dir

            outfile.close()


def detect_operation_system_symb():
    if "Windows" in platform.system():
        symb = "\\"
    elif "Darwin" in platform.system():
        symb = '/'
    else:
        symb = '/'
    return symb


def generate_path(father_path, symb):
    years = [str(i) for i in xrange(2002, datetime.datetime.now().year + 1)]

    target_year = set(os.listdir(father_path)) & set(years)

    years_target = raw_input(
        'please enter the year which you want to unzip,combined with comma:')
    if years_target == 'all':
        pass
    elif ',' in years_target:
        years_target = years_target.split(',')
        target_year = target_year & set(years_target)
    elif '-' in years_target:
        years_target = [str(i) for i in xrange(int(years_target.split(
            '-')[0]), int(years_target.split('-')[-1]) + 1)]
        # print set(years_target)
        target_year = target_year & set(years_target)
    elif years_target in years:
        # print years_target, years

        target_year = target_year & set([years_target])
    else:
        raise 'unknown years'

    if target_year == set([]):
        raise 'empty year'
    else:
        pass
    # print target_year
    # print father_path

    logfile_dir_path = [father_path + symb + i for i in target_year]
    logfile_dir_path = dict(zip(target_year, logfile_dir_path))
    # print logfile_dir_path
    logfile_path = {}

    for key in logfile_dir_path.keys():
        # print pp
        temp_path = os.listdir(logfile_dir_path[key])
        # print temp_path
        logfile_path[key] = [logfile_dir_path[key] + symb +
                             f for f in temp_path if f.split('.')[-1] == 'zip']
    target_unzip_path = father_path + symb + 'unzip' + symb

    return logfile_path, logfile_dir_path, target_unzip_path


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


if __name__ == '__main__':
    father_path = os.path.split(os.path.realpath(__file__))[0]
    symb = detect_operation_system_symb()
    logfile_path, child_path, target_unzip_path = generate_path(
        father_path, symb)
    # print 'logfile path is %s' % logfile_path
    # print 'child path includes %s' % child_path
    print target_unzip_path
    #pool = mp.Pool()
    if target_unzip_path[-1] != symb:
        target_unzip_path += symb
    if not os.path.exists(target_unzip_path):
        os.mkdir(target_unzip_path)

    for pa in logfile_path.keys():
        dest_target = target_unzip_path + pa
        if not os.path.exists(dest_target):
            os.mkdir(dest_target)
        else:
            pass

        yyy = [(fi, dest_target) for fi in logfile_path[pa]]
        if yyy != []:
            ready_file = [r.split('.')[0] for r in os.listdir(
                dest_target) if r.split('.')[-1] == 'csv']
            for y in yyy:
                name = y[0].split(symb)[-1].split('.zip')[0]
                if name in ready_file:
                    pass
                else:
                    unzip_file_for_map(y)
                gc.collect()
            #pool.map(unzip_file_for_map, yyy)

        # mutli_unzip

        # child_path

        #    zip_file_list = [
        # zipfff for zipfff in file_list if zipfff.split(".")[-1] == "zip"]
