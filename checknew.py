# -*- coding: utf-8 -*-
import sys
import glob
import os.path
import time
import datetime
from epub2vmobi import ebook_converter
import shutil
import argparse


parser = argparse.ArgumentParser(description='check specific path.')
parser.add_argument('calipath', metavar='epub_path',
                    help='path of epub. e.g. \'/Users/myname/Calibre Library/*/*/*.epub\'')
args = parser.parse_args()
calipath = args.calipath
con = ebook_converter()
#for f in glob.glob(calipath):
#    print f
for f in glob.glob(calipath):
    mt = int(os.path.getmtime(f))
    today = int(time.mktime(datetime.date.today().timetuple()))
    todo = False
    if 86400 >= abs(today-mt) >=0:
        todo = True
    #msg = '{}, do'.format(mt) if todo else '{}, skip'.format(mt)
    #print msg
    if todo:
        #print f, mt
        bn = os.path.basename(f)
        print bn
        name = raw_input('輸入書名：')
        if len(name.strip()) != 0:
            print name
        else:
            print 'skip'
            continue
        try:
            shutil.copy(f,name+'.epub')
            con.epub2vmobi_convert(f,name)
        except Exception as e:
            print 'fail to convert %s' %name
            print e
