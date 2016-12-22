# -*- coding:utf-8 -*-
import urllib2, sys,os,urllib,random,time,datetime,platform,gc
import loadingsplit
import multiprocessing as mp

#-------------------
__version__="2"
__author__="sn0wfree"
#-------------------

def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return local_filename



def chunk_report(bytes_so_far, chunk_size, total_size):
   percent = float(bytes_so_far) / total_size
   percent = round(percent*100, 2)
   sys.stdout.write("Downloaded %d of %d bytes (%0.2f%%)\r" %
       (bytes_so_far, total_size, percent))

   if bytes_so_far >= total_size:
      sys.stdout.write('\n')

def chunk_read(response, chunk_size=8192, report_hook=None):
   total_size = response.info().getheader('Content-Length').strip()
   total_size = int(total_size)
   bytes_so_far = 0

   while 1:
      chunk = response.read(chunk_size)
      bytes_so_far += len(chunk)

      if not chunk:
         break

      if report_hook:
         report_hook(bytes_so_far, chunk_size, total_size)

   return bytes_so_far



def python_download(url,target_path,symbol="UI-friendly",reporthook=None):
    #global speed
    f=time.time()
    #global download_count,total_count
    #if symbol =="UI-friendly":
    #    print "Begin download with urllib"
    #else:
    #    pass
    #--------------
    if target_path == "default":
        (url_default,path_default,file_name)=(url, "logfile","log20160330.zip")
        (url,path_filename)=(url,path_default+"/"+file_name)
    else:
        pass

    path_filename=target_path+url.split("/")[-1]

    #f = urllib2.urlopen(url)
    #with open("code2.zip", "wb") as code:
    #    code.write(f.read())

    urllib.urlretrieve(url,path_filename,reporthook=reporthook)
    #-----------------
    #download_count+=1
    speed=time.time()-f
    if symbol =="UI-friendly":
        #progress_test(download_count,total_count,speed,speed*(total_count-download_count))


        sys.stdout.write( "\rDownloading %s completed,Speed: %0.2f s/zip " %(url.split("/")[-1],speed))
        sys.stdout.flush()
    else:
        pass


def progress_test(counts,lenfile,speed,w):
    bar_length=20
    eta=time.time()+w
    precent =counts/float(lenfile)

    ETA=datetime.datetime.fromtimestamp(eta)
    hashes = '#' * int(precent * bar_length)
    spaces = ' ' * (bar_length - len(hashes))
    sys.stdout.write("""\r%d%%|%s|download %d projects|Speed : %.4f |ETA: %s """ % (precent*100,hashes + spaces,counts,speed,ETA))

    #sys.stdout.write("\rthis spider has already read %d projects, speed: %.4f/projects" % (counts,f2-f1))

    #sys.stdout.write("\rPercent: [%s] %d%%,remaining time: %.4f mins"%(hashes + spaces,precent,w))
    sys.stdout.flush()

def import_data(target_year,pardir_status=None):
    dirs=os.path.split(os.path.realpath(__file__))[0]
    if "Windows" in platform.system():
        pardir=dirs+"\\logfile\\unzip\\"+target_year+"\\"
        target_path=dirs+"\\logfile\\"+target_year+"\\"
        target_txt_file=target_path+"\\"+target_year+".txt"

    elif "Darwin" in platform.system():
        pardir=dirs+"/logfile/unzip/"+target_year+"/"
        target_path=dirs+"/logfile/"+target_year+"/"
        target_txt_file=target_path+"/"+target_year+".txt"
    else:
        pardir=dirs+"/logfile/unzip/"+target_year+"/"
        target_path=dirs+"/logfile/"+target_year+"/"
        target_txt_file=target_path+"/"+target_year+".txt"


    target_url=loadingsplit.read_text_file(target_txt_file)
    target_url_a=[ur.split("\n")[0] for ur in target_url ]
    if pardir_status==None:
        return target_url_a,target_path
    elif pardir_status==1 or pardir_status==True:
        return target_url_a,target_path,pardir
    else:
        return target_url_a,target_path



def transfer_url_and_download(target_url_combine):
    target_url=target_url_combine[0]
    target_path=target_url_combine[1]
    url='https://'+ target_url
    #urlretrieve(response, filename=None, reporthook=chunk_report)
    #chunk_read(response, report_hook=chunk_report)
    python_download(url,target_path=target_path,symbol="UI-friendly")
    time.sleep(2*random.random())

def poolfunction(need_downloand_file):
    pool=mp.Pool()
    pool.map(transfer_url_and_download,need_downloand_file)

if __name__ == '__main__':
    gc.enable()
    #download_count=0
    #global target_path
    #global download_count,total_count

    #target_year="2010"
    target_year=raw_input("which year data want to download:")



    target_urls,target_path=import_data(target_year)
    #obtain downloaded files
    downloaded_files=os.listdir(target_path)
    #print target_url[0],type(target_url[0])
    #print target_url[0].split("/")[-1]
    need_downloand_file=[]
    for target_url in target_urls:
        filenames=target_url.split("/")[-1]
        if filenames not in downloaded_files:
            need_downloand_file.append((target_url,target_path))
        else:
            pass
    total_count=len(need_downloand_file)

    poolfunction(need_downloand_file)

    print "Downloading completed! all files are downloaded"








    #response = urllib2.urlopen('https://'+ target_url[0])
