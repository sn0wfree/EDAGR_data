# -*- coding:utf-8 -*-


#-------------------
__version__="1.0"
__author__="sn0wfree"
#-------------------

import os,platform,zipfile
import multiprocessing as mp


def check_zipfile_for_pool(zip_file_path_lists):



    if  zipfile.ZipFile(zip_file_path_lists).testzip() != None:
        a=zipfile.ZipFile(zip_file_path_lists).testzip()

    else:
        a=0


    return a

def check_zipfile(check_path):
    error_zipfile=[]
    if os.path.isfile(check_path):
        file_name=os.path.split(os.path.realpath(check_path))[1]
        if file_name.split(".")[-1] == "zip":
            #check zip
            if zipfile.ZipFile(check_path).testzip() != None:
                error_zipfile.append(zipfile.ZipFile(check_path).testzip())
            else:
                print "All Good!"
        else:
            print "Detected %s file, Non-zip file. Cannot test it!"%file_name.split(".")[-1]
    elif os.path.isdir(check_path):
        file_list=os.listdir(check_path)
        zip_file_list=[zipfff for zipfff in file_list if zipfff.split(".")[-1] == "zip"]
        if "Windows" in sys_info:
            temp_symbol="\\"
        elif "Darwin" in sys_info:
            temp_symbol="/"
        else:
            temp_symbol="/"

        if check_path[-1] != temp_symbol:
            check_path+=temp_symbol
        else:
            pass


        zip_file_path_lists=[check_path + zipfff_path for zipfff_path in zip_file_list]

        #error_zipfile=check_zipfile(zip_file_path_lists)
        pool=mp.Pool()
        error_zipfile_temp=pool.map(check_zipfile_for_pool,zip_file_path_lists)
        error_zipfile=[error_zipfile_name for error_zipfile_name in error_zipfile_temp if error_zipfile_name  != 0]
    else:
        print "Unexpected path, Exit!"

    return error_zipfile


if __name__ =="__main__":
    #detect current path
    sys_info=platform.system()
    #-----------
    dirs=os.path.split(os.path.realpath(__file__))[0]
    if "logfile" in os.listdir(dirs):
        if "Windows" in sys_info:
            logfile_dirs=dirs+"\\logfile\\"


        elif "Darwin" in sys_info:
            logfile_dirs=dirs+"/logfile/"

        else:
            #default
            logfile_dirs=dirs+"/logfile/"

    else:
        logfile_dirs="Nothing"
    #--------------

    check_path=raw_input("please enter the path of zipfiles or folders to check:")
    #check_path=__file__
    error_zipfile=check_zipfile(check_path)
    print error_zipfile





        #/Users/sn0wfree/Documents/python_projects/download-data/logfile/2003










    #find data
