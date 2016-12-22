# -*- coding:utf-8 -*-

#-------------------
__version__="1.0"
__author__="sn0wfree"
#-------------------
import urllib2, sys,os,urllib,random,time,datetime,platform,gc
import download2 as download
import multiprocessing as mp

import zipfile

def zip_dir(dirname,zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else :
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        #print arcname
        zf.write(tar,arcname)
    zf.close()


def unzip_file(zipfilename, unziptodir):
    if not os.path.exists(unziptodir): os.mkdir(unziptodir, 0777)
    zfobj = zipfile.ZipFile(zipfilename)
    for name in zfobj.namelist():
        name = name.replace('\\','/')

        if name.endswith('/'):
            os.mkdir(os.path.join(unziptodir, name))
        else:
            ext_filename = os.path.join(unziptodir, name)
            ext_dir= os.path.dirname(ext_filename)
            if not os.path.exists(ext_dir) : os.mkdir(ext_dir,0777)
            outfile = open(ext_filename, 'wb')
            outfile.write(zfobj.read(name))
            outfile.close()



def check_Missing_file(target_url_a,target_path):
    target_url_file_and_url={}
    for ff in target_url_a:
        target_url_file_and_url[ff.split("/")[-1]]=ff
    while 1:
        downloaded_all_files=os.listdir(target_path)
        downloaded_files=[f for f in downloaded_all_files if f.split(".")[-1]=="zip"]
        if set(target_url_file_and_url.keys()) != set(downloaded_files):
            undownload_file=set(target_url_file_and_url.keys())-set(downloaded_files)
            undownload_files=[ (target_url_file_and_url[ffs],target_path) for ffs in undownload_file]
            print "\n !!! Found %d missing file(s), Begin downloading missing file(s). \n Please have coffe and wait!!!\n"%len(undownload_files)
            download.poolfunction(undownload_files)
        else:
            break
    return downloaded_files
def unzip_file_for_pool(target_code):
    unzip_file(target_code[0],target_code[1])
if __name__ =="__main__":
    check_url="https://www.sec.gov/files/edgar_logfile_list.html"
    gc.enable()
    target_year=raw_input("which year data want to compare or unzip:")
    #compare
    target_url_a,target_path,unzip_pardir=download.import_data(target_year,pardir_status=1)

    downloaded_files=check_Missing_file(target_url_a,target_path)
    #print target_path


    #return full path
    downloaded_files_full_path=[target_path + temp for temp in downloaded_files]

    target_code=[(tempss, unzip_pardir) for tempss in downloaded_files_full_path]
    pool=mp.Pool()


    pool.map(unzip_file_for_pool,target_code)
    print "%s year zip logfile(s) unzip completed"%target_year
