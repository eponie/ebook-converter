import sys
import subprocess
import re
import logging
from logging import handlers
import os.path
import shutil
from lxml import etree
import glob
import ConfigParser


def get_logger(name, debug=True):
    log_file = './%s.log' %name
    logger = logging.getLogger(name)
    if debug:
        out_hdlr = logging.StreamHandler(sys.stdout)
    else:
        out_hdlr = handlers.RotatingFileHandler(log_file, maxBytes = 1024 * 1024, backupCount = 1)
    out_hdlr.setFormatter(logging.Formatter("[%(asctime)s]-[%(levelname)s] %(message)s"))
    out_hdlr.setLevel(logging.DEBUG)
    logger.addHandler(out_hdlr)
    logger.setLevel(logging.DEBUG)
    return logger

class ebook_converter:
    def __init__(self, logger=None):
        if logger == None:
            self.logger = get_logger('converter')
        else:
            self.logger = logger
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.conf_file = os.path.realpath(os.path.join(self.path,'ebc.conf'))
        conf = ConfigParser.ConfigParser()
        conf.read(self.conf_file)
        self.config = conf
        self.kup = os.path.realpath(os.path.join(self.path, conf.get('ebc', 'kindleunpack'))) #'KindleUnpack-master/lib/kindleunpack.py'
        self.kgen = os.path.realpath(os.path.join(self.path, conf.get('ebc', 'kindlegen'))) #'./KindleGen_Mac_i386_v2_9/kindlegen'
    
    def _fail(self, msg):
        self.logger.error(msg)
        sys.exit(1)


    def _run_command(self, cmd):
        self.logger.debug('going to run command: %s' %cmd)
        process = subprocess.Popen([cmd], shell=True, \
                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        ret = process.returncode
        return ret, stdout, stderr

    def _mobi_opf_gettitle(self, opf_file):
        try:
            et = etree.parse(opf_file)
            root = et.getroot()
            for item in et.xpath('//*'):
                if item.tag.endswith('title'):
                    return item.text
        except:
            return None
        return None

    def _mobi_opf2v(self, opf_file):
        try:
            et = etree.parse(opf_file)
            root = et.getroot()
            for item in et.xpath('//*'):
                if item.tag.endswith('meta') and \
                   item.get('name') == "primary-writing-mode":
                    item.set('content', 'vertical-rl')
                    #print etree.tostring(item)
                if item.tag.endswith('language'):
                    #print item.text
                    item.text = 'zh-tw'
            with open(opf_file, 'w') as opf:
                opf.write(etree.tostring(root, pretty_print =True))
        except Exception as e:
            self.logger.error('FAIL updateing opd %s: %s' %(opf_file, str(e)))
            raise

    def _unpack_mobi(self, inf, outf):
        cmd = 'python %s %s %s' %(self.kup, inf, outf)
        ret, out, err = self._run_command(cmd)
        return ret, out, err

    def _conver2mobi(self, inf, outf):
        cmd = '%s %s -o %s' %(self.kgen, inf, outf)
        ret, out, err = self._run_command(cmd)
        return ret, out, err

    def _css2v(self, css_file):
        newset = '''
body {
    margin: 5%;
    text-align: justify;
    -webkit-writing-mode: vertical-rl;
}'''
        with open(css_file, 'a') as css:
            css.write(newset)
        #print css_file

    def epub2vmobi_convert(self, ori_file, n_name=''):
        ori_folder = os.path.dirname(ori_file)
        n_epub = 'book.epub'
        n_mobi = 'book.mobi'
        up_folder = 'book/'
        up_opfdir = 'book/mobi8/OEBPS/'
        up_opf = 'book/mobi8/OEBPS/content.opf'
        up_style = 'book/mobi8/OEBPS/Styles/*.css'
        up_Text = 'book/mobi8/OEBPS/Text/'
        n_vmobi = n_name + '.mobi'
        b_epub = n_name + '.epub'

        # 1. prepare & check
        if not ori_file.endswith('.epub'):
            self._fail('original file check fail')
        if os.path.realpath(ori_file) != os.path.realpath(n_epub):
            shutil.copyfile(ori_file, n_epub)

        # 2. convert to mobi
        ret, out, err = self._conver2mobi(n_epub, n_mobi)
        if ret == 0:
            self.logger.info('SUCCESS convert to mobi')
        else:
            self._fail('FAIL convert to mobi')

        self.mobi2vmobi_convert(n_mobi, n_name) 
        os.rename(n_epub, b_epub)
        #os.remove(n_epub)


    def mobi2vmobi_convert(self, ori_file, n_name=''):
        ori_folder = os.path.dirname(ori_file)
        n_mobi = 'book.mobi'
        up_folder = 'book/'
        up_opfdir = 'book/mobi8/OEBPS/'
        up_opf = 'book/mobi8/OEBPS/content.opf'
        up_style = 'book/mobi8/OEBPS/Styles/*.css'
        up_Text = 'book/mobi8/OEBPS/Text/'
        n_vmobi = n_name + '.mobi'

        # 0. prepare & check
        if not ori_file.endswith('.mobi'):
            self._fail('original file check fail')
        if os.path.realpath(ori_file) != os.path.realpath(n_mobi):
            shutil.copyfile(ori_file, n_mobi)

        # 1. unpack mobi
        ret, out, err = self._unpack_mobi(n_mobi, up_folder)
        if ret == 0:
            self.logger.info('SUCCESS unpack mobi')
        else:
            self._fail('FAIL unpack mobi')

        # 2. update content.opf
        self._mobi_opf2v(up_opf)
        self.logger.info('SUCCESS update opf %s' %up_opf)

        # 3. update css
        for css_file in glob.glob(up_style):
           self._css2v(css_file) 
        self.logger.info('SUCCESS update css in %s' %up_style)

        # 4. update text

        # 5. pack to new mobi
        ret, out, err = self._conver2mobi(up_opf, n_vmobi)
        if ret == 0:
            self.logger.info('SUCCESS export to %s' %n_vmobi)
        else:
            self._fail('FAIL convert to mobi %s' %err)

        # 6. wrap up
        title = self._mobi_opf_gettitle(up_opf)
        if not n_name:
            n_vmobi = title + '.mobi'
        path_vmobi = os.path.join(up_opfdir, n_vmobi)
        shutil.copyfile(path_vmobi, n_vmobi)
        os.remove(n_mobi)
        shutil.rmtree(up_folder)


<<<<<<< HEAD
if __name__ == "__main__":
    con = ebook_converter()
    if len(sys.argv) != 3:
        print 'python epub2vmobi.py path2epub booktitle'
        sys.exit(1)
    else:
        con.epub2vmobi_convert(sys.argv[1], sys.argv[2])
=======

if len(sys.argv) != 3:
    print 'python epub2vmobi.py path2epub booktitle'
    sys.exit(1)
else:
    con = ebook_converter()
    con.epub2vmobi_convert(sys.argv[1], sys.argv[2])
>>>>>>> 39921e563cc3b996048736430962120353f07da3



    


