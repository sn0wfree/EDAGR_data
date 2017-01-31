# -*- coding:utf-8 -*-


import os
import os.path
import zipfile


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


def input_unzip_funtion():
    r = 1
    while r:
        print 'plesea enter which year you  want to unzip(default=all years)\n'
        print 'if you want unzip multi - file please type each year with comma(for example: 2003, 2004)'
        print 'if you want unzip single year please just type the year(for example: 2003)'

        years = raw_input('please just type the year: ')

        if years == "all":
            years = [i for i in xrange(2002, 2016 + 1)]
            # path = "/Users/sn0wfree/Documents/python_projects/download-data/logfile"
            # path = raw_input('please enter the path of the zip file')
            path = os.path.split(os.path.realpath(__file__))[0]
            r = 0
        else:
            # handle off path.
            default_path = os.path.split(os.path.realpath(__file__))[0]
            print 'detect the current path: %s' % default_path
            path = raw_input('type default to use current path or type yours:')
            if path == 'default':
                path = default_path
            else:
                path = path
            # handle the years
            if ',' in years:
                years = years.split(',')
                r = 0
            else:
                if isinstance(int(years), int):
                    years = int(years)
                    r = 0
                else:
                    print "unrecoginisation year"
    return (years, path)


def generate_unzip_path(years, path):

    if isinstance(years, int):
        print 'this program will uncompress the %d-year file to %s/unzip' % (years, path)
        path_target = path + "/" + str(years)
        path_unzip = path + "/unzip" + "/" + str(years)

    elif isinstance(years, list):
        print 'this program will uncompress the %s-%syear file to %s/unzip' % (str(years[0]), str(years[-1]), path)
        path_target = [path + "/" + str(i) for i in years]
        path_unzip = [path + "/unzip" + "/" + str(i) for i in years]

    else:
        print 'cannot recoginse the path or years'
        path_unzip = None
        path_target = None

    # print path_unzip
    # print years

    return (years, path_target, path_unzip)
if __name__ == "__main__":
    # zip_dir(r'E:/python/learning',r'E:/python/learning/zip.zip')
    # unzip_file(r'E:/python/learning/zip.zip',r'E:/python/learning2')

    # for root, dirs, files in os.walk(dirname):

    (years, path) = input_unzip_funtion()
    (years, path_target, path_unzip) = generate_unzip_path(years, path)
    # print 'years: %s,\n target path: %s,\npath_unzip: %s\n' % (years,
    # path_target, path_unzip)
    if isinstance(years, int):
        pp = (years, path_target, path_unzip)
    elif isinstance(years, list):
        pp = zip(years, path_target, path_unzip)

    # print pp
    for p in pp:
        unzip_file(p[1], p[2])

        # unzip_file(zipfilename, unziptodir)
