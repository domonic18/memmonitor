# encoding: utf-8

'''
Created on 2016年3月18日

@author: Dongming
'''


import os
import datetime
import time
import sys

from CListEx import Clist_type


class memlog:
    str_dir_result = ""
    str_path_result = ""
    str_app_name = "com.sohu.inputmethod.sogou"
    interval = 1
    def __init__(self  , name ):
        self.str_app_name = name
        self.str_dir_result = os.path.join(os.getcwd(), "result")
        if os.path.exists( self.str_dir_result ) == False:
            os.mkdir(self.str_dir_result)
        
        currentdate = datetime.datetime.now()
        self.str_path_result = os.path.join(self.str_dir_result, str(currentdate)[0:10])
        if os.path.exists( self.str_path_result ) == False:
            os.mkdir(self.str_path_result)
        
        print self.str_dir_result
        print self.str_path_result
    def getMeminfo(self):
        command = "adb shell dumpsys meminfo " + self.str_app_name
        ret = os.popen(command).readlines()
        return ret
    def setInterval(self , interval):
        self.interval = int(interval)
    def WriteLog(self , content ):
        currentime = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime())
        print currentime
        path = os.path.join( self.str_path_result, currentime + ".log")
        fp = open(path,'wb')
        fp.writelines(content)
        fp.close()
    def Run(self):
        print "Start Monitor\n"
        while True:
            print "Get Meminfo..."
            mem = self.getMeminfo()
            self.WriteLog(mem)
            time.sleep(self.interval)

import fnmatch
import re
import xlwt

class memloganalyze:
    CONST_coloum_memtype = ["PssTotal" , 
                            "PrivateDirty" , 
                            "PrivateClean" , 
                            "SwappedDirty" , 
                            "Heap_size" ,
                            "Heap_Alloc" , 
                            "Heap_Free" ]    
    list_tag = ['Native Heap' , 
                'Dalvik Heap' , 
                'Dalvik Other',
                'Stack',
                'Ashmem',
                'Gfx dev',
                'Other dev',
                '.so mmap',
                '.apk mmap',
                '.ttf mmap',
                '.oat mmap',
                '.art mmap',
                '.dex mmap',
                'Unknown',
                'GL',
                'Other mmap',
                'TOTAL']   
    def __init__(self  , ipath , opath ):
        self.dict_mem_result =  Clist_type()
        self.str_path_result = ipath
        self.str_path_output = opath
        if os.path.exists( self.str_path_output ) == False:
            os.mkdir(self.str_path_output)
    def setTag(self , list_arv=['Native Heap' , 'Dalvik Heap' , 'Dalvik Other']):
        self.list_tag = list_arv
        for pname in self.list_tag:
            self.dict_mem_result.settag(pname, self.CONST_coloum_memtype)
    
    def ftw(self , root=os.getcwd(), patterns='*'):
        list = []
        pattern_list = patterns.split(';') 
        for (path, dirs, files) in os.walk(root): 
            for name in files: 
                fullname = os.path.join(path, name) 
                for pattern in pattern_list: 
                    if fnmatch.fnmatch(name, pattern):
                        list.append(fullname)
        list.sort()
        return list
    
    def parseFile(self , filepath , rowname):
        fp = open(filepath,'rb')
        content = fp.readlines()
        fp.close()
        for line in content:
            line = line.strip(" ").strip("\t").strip("\n")
            if line.startswith(rowname):
                print line
                verPattern = re.compile("\d+")
                num = verPattern.findall(line)
                for n in xrange(0,len(num)):
                    self.dict_mem_result.settypedata( rowname, self.CONST_coloum_memtype[n], num[n])       
    
    def createExcelHandler(self , sheetName):  
        wb = xlwt.Workbook()  
        ws = wb.add_sheet(sheetName, cell_overwrite_ok=True)  
        return wb, ws  
                    
    def writeResult(self , filename):
        #filepath = self.str_path_output + "\\" + filename + ".xls"
        filepath = os.path.join(self.str_path_output, filename + '.xls')
        wb = xlwt.Workbook()
        for n in self.list_tag:
            ws = wb.add_sheet(n, cell_overwrite_ok=True)
            for index in range(len(self.CONST_coloum_memtype)):
                ws.write(0 , index , self.CONST_coloum_memtype[index] )#写第一列
                list_temp = self.dict_mem_result.gettypedata(n, self.CONST_coloum_memtype[index])
                style=xlwt.easyxf('font: name Times New Roman', num_format_str='#,##0.00')
                for rownum in range(len(list_temp)):
                    ws.write(rownum + 1 , index , int(list_temp[rownum]) , style)
        wb.save(filepath)
                    
    def doAnalyze(self):
        list_log = []
        self.setTag(self.list_tag)
        for nindexname in self.list_tag:
            print "Analyze  " + nindexname
            list_log = self.ftw( self.str_path_result , "*.log")
            for pfile in list_log:
                print pfile
                self.parseFile(pfile , nindexname)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        appname = sys.argv[1]
        print appname
        interval = sys.argv[2]
        print interval 
        mem = memlog(appname)
        mem.setInterval(interval)
        mem.Run()
    else:
        while(True):
            
            print "Please select function:( )"
            print "1.Monitor package meminfo."
            print "2.Analyze monitor result."
            select = raw_input("> ")
            if select == "1":
                appname = raw_input("Please input packagename:(e.g:com.sohu.inputmethod.sogou)\n")
                if appname == "":
                    appname = "com.sohu.inputmethod.sogou"
                mem = memlog(appname)
                mem.Run()
            elif select == "2":
                dict_dir = {}
                root = os.path.join( os.getcwd(), 'result')
                for (path, dirs, files) in os.walk(root):
                    index = 1 
                    for name in dirs: 
                        print str(index) + "." + name
                        dict_dir[str(index)] = name
                        index += 1
                ret = raw_input("Please select result path:\n")
                if ret in dict_dir:
                    path = dict_dir[ret]
                    inpath = os.path.join(root,path)
                    memanalyze = memloganalyze( inpath , root )
                    memanalyze.doAnalyze()
                    memanalyze.writeResult("result")
                    print "Result:\t" +  inpath + "\n"
            else:
                continue
