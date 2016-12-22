# -*- coding:utf-8 -*-


#-------------------
__version__="1.0"
__author__="sn0wfree"
#-------------------

import os,platform,zipfile
import loadingsplit
import download2 as download
import multiprocessing as mp


def check_zipfile_for_pool(zip_file_path_lists):



    if  zipfile.is_zipfile(zip_file_path_lists)!= True:
        a=zip_file_path_lists

    else:
        a=0


    return a

def check_zipfile(check_path):
    sys_info=platform.system()
    error_zipfile=[]
    if os.path.isfile(check_path):
        file_name=os.path.split(os.path.realpath(check_path))[1]
        if file_name.split(".")[-1] == "zip":
            #check zip
            if zipfile.is_zipfile(check_path) != True:
                error_zipfile.append(check_path)
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


def check_and_download(error_zipfile_url_1,d="download"):

    if error_zipfile_url_1 !=[]:
        downloaded_files=[f for f in os.listdir(check_path) if f.split(".")[-1]=="txt"]
        if len(downloaded_files) == 1:
            year = downloaded_files[0].split(".")[0]
        elif len(downloaded_files) > 1:
            target =[files.split(".")[0] for files in downloaded_files if int(files.split(".")[0]) > 2002]
            if len(target)==1:
                year=target
            else:
                raise Expection("Error, Missing txt file!")
        else:
            raise Expection("Error, un-recogization path and txt file!")
        target_txt_file=check_path+"/"+year+".txt"
        #print target_txt_file
        all_urls=loadingsplit.read_text_file(target_txt_file)
        all_urls_t=[uuu.split()[0] for uuu in all_urls]

        all_missing_data_urls=[(u,check_path+"/") for u in all_urls_t if u.split("/")[-1] in error_zipfile_url_1]
        #print all_missing_data_urls
        if d=="download":
            print all_missing_data_urls[1][1]


            download.poolfunction(all_missing_data_urls)
            #aaaaa=1
    else:
        print "all good"
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
    error_zipfiles=check_zipfile(check_path)
    error_zipfile_url_1=[error_zipfile.split('/')[-1] for error_zipfile in error_zipfiles]
    print error_zipfile_url_1
    check_and_download(error_zipfile_url_1,d="download")











    #loading txt






        #/Users/sn0wfree/Documents/python_projects/download-data/logfile/2003










    #find data
