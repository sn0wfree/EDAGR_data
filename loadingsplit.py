# -*- coding:utf-8 -*-



#from selenium import webdriver
import urllib,os
#import urllib2
import requests


#browser = webdriver.Chrome()
#browser.get('http://www.baidu.com/')




def obatin_file_in_dir(mypath):
    f = []
    for (dirpath, dirnames, filenames) in os.walk(mypath):
        f.extend(filenames)
        break
    return



def python_download(url,path="default",symbol="UI-friendly"):
    if symbol =="UI-friendly":
        print "Begin download with urllib"
    else:
        pass
    #--------------
    if path == "default":
        (url_default,path_default,file_name)=(url, "logfile","log20160330.zip")
        (url,path)=(url,path_default+"/"+file_name)
    else:
        pass

    urllib.urlretrieve(url,path)
    #-----------------
    if symbol =="UI-friendly":
        print "Downloading completed"
    else:
        pass


def projetcdata_txt_wholewrite(items,files):

    with open(files,'w+') as f:

        for item in items:
            f.write(item+"\n")


def readacsv(file):
    with open(file,'r+') as f:
        w=pd.read_csv(file,skip_footer=1,engine='python')
    return w

def read_text_file(file):
    with open (file,'r') as file_file:
        file_list=file_file.readlines()
        return file_list

def multi_name_and_assign_data_dev(range_subname):
    names={}
    if type(range_subname) == type(1):
        range_subname=xrange(range_subname)
    elif type(range_subname) == list or type(range_subname) == tuple:
        pass
    elif type(range_subname) == dict:
        range_subname=range_subname.keys()
    for i in range_subname:
        if type(i) != str:
            i=str(i)
        else:
            pass
        #if list_or_dict == "list":
        locals()[i]=[]
        #elif list_or_dict == "dict":
        #    locals()[i]={}
        names[i]=locals()[i]
    return names




class classify_data():
    def __init__(self):
        self.year="year"
        self.Qtr="Qtr"
        self.month="month"
        self.day="day"
        self.url="url"
    def name_it(self, year,Qtr,month,day,url):
        self.year=year
        self.Qtr=Qtr
        self.month=month
        self.day=day
        self.url=url



if __name__ =="__main__":
    chrome = 'Mozilla/5.0 (X11; Linux i86_64) AppleWebKit/537.36 ' + '(KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
    headers = {'User-Agent': chrome}


    # Test URL
    #url = "http://www.sec.gov/dera/data/Public-EDGAR-log-file-data/2016/Qtr1/log20160330.zip"
    target="/Users/sn0wfree/Documents/python_projects/download-data/target.txt"
    lis=read_text_file(target)[0].split(" ")

    headd="URL Structure to access files (by Qtrs)".split(" ")
    head_address="www.sec.gov/dera/data/Public-EDGAR-log-file-data/"
    #initial date


    #end initial date





    error_url=[]



    years=[str(i) for i in xrange(2002,2016+1)]


    Qtrs=["Qtr1","Qtr2","Qtr3","Qtr4"]
    category=(years,Qtrs)
    #create container
    all_url=multi_name_and_assign_data_dev(years)




    for orignal_url in lis:
        if orignal_url in headd:
            # ingore "URL Structure to access files (by Qtrs)"
            pass
        else:
            temp=classify_data()
            if head_address in orignal_url:
                addr_clean=orignal_url.split(head_address)[1]

                addr_clean=addr_clean.split("/")
                #print addr_clean
                if addr_clean[0] in years:
                    #when years 2016

                    year=addr_clean[0]

                    if addr_clean[1] in Qtrs:
                        Qtr=addr_clean[1]
                        if ".zip" in addr_clean[2]:
                            md=addr_clean[2].split(".zip")[0].split(year)[1]
                            if len(md) == 4:
                                (month,day)=(md[0:2],md[2:4])


                                temp.name_it(year,Qtr,month,day,orignal_url)

                                #print temp.year
                                #print temp.Qtr

                                all_url[temp.year].append(temp)
                            else:
                                error_url.append(orignal_url)
                                error_tag="Non-recoginised Month and Day"
                                pass
                        else:
                            error_url.append(orignal_url)
                            error_tag="Non-recoginised zip"
                            pass
                    else:
                        error_url.append(orignal_url)
                        error_tag="Non-recoginised Qtr"
                        pass
                else:
                    error_url.append(orignal_url)
                    error_tag="Non-recoginised year"
                    pass

    #for year in years:
    #    for q in Qtrs:
    bbb=all_url["2013"][12]
    path="/Users/sn0wfree/Documents/python_projects/download-data/logfile"

    #print type(all_url["2013"])
    for y in years:
        locals()["year"+y]=[]
        for ur in all_url[y]:
            locals()["year"+y].append(ur.url)

        subpath=path +"/"+y+"/"+y+".txt"
        if os.path.isdir(path +"/"+y):
            pass
        else:
            os.mkdir(path +"/"+y)

        projetcdata_txt_wholewrite(locals()["year"+y],subpath)
    #test_path2013=path +"/2014/2014.txt"



    #print year2013
