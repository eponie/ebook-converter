# -*- coding: utf-8 -*-
import sys
import glob
import os.path
import time
import datetime
from epub2vmobi import ebook_converter
import shutil

calipath = sys.argv[1]
con = ebook_converter()
for f in glob.glob(calipath):
    mt = int(os.path.getmtime(f))
    today = int(time.mktime(datetime.date.today().timetuple()))
    todo = False
    if 86400 >= (mt-today) >=0:
        todo = True
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
