# encoding: utf-8

'''
Created on 2016年3月18日

@author: Dongming
'''

'''
#    数据结构类型
#    Native Heap
#        --a(Total)
#          |--[1,2,3,4,5,6,7,8....]
#        --b(PrivateDirty)
#          |--[1,2,3,4,5,6,7,8....]
#        --c
#          |--[1,2,3,4,5,6,7,8....]
#    Davil Heap
#        --a(Total)
#          |--[1,2,3,4,5,6,7,8....]
#        --b(PrivateDirty)
#          |--[1,2,3,4,5,6,7,8....]
#        --c
#          |--[1,2,3,4,5,6,7,8....]
#由以上数据内容，形成的数据结构
#
#    
#    Clist_type
#      Clist_coloum
#          |--Clist_data(list)
#
'''
class Clist_data(object):
    list_result = []
    def __init__(self ):
        self.list_result = []
#        print self.list_result
    def add(self , num):
        self.list_result.append(num)
    def getlenth(self):
        return len(self.list_result)
    def getDatas(self ):
        return self.list_result
    
class Clist_coloum( object ):
    list_datas = []
    list_coloum_type = []
    def __init__(self , list_type ):
        self.list_datas = []
        self.list_coloum_type = []
        print self.list_datas
        self.list_coloum_type = list_type
        for i in xrange(len(self.list_coloum_type)):
            idata = Clist_data()
            self.list_datas.append(idata)        
    def getData(self , name ):
        try:
            index = (self.list_coloum_type).index( name )
            return (self.list_datas[index]).getDatas()
        except:
            print "Not foud Index"
    def setData(self , name  , value):
        try:
            index = (self.list_coloum_type).index( name )
            self.list_datas[index].add(value)
        except:
            print "Not foud Index"

class Clist_type:
    def __init__(self ):
        self.list_types = []
        self.list_coloums = []
        
    def settag(self , typename , list_coloum):
        try:
            index = (self.list_types).index(typename )
            return index
        except:
            self.list_types.append(typename)
            icoloum  = Clist_coloum( list_coloum )
            self.list_coloums.append(icoloum)
    def settypedata(self , typename , coluname , value):
        try:
            index = (self.list_types).index( typename )
            return (self.list_coloums[index]).setData(coluname , value)
        except:
            print "Not foud Index"
    
    def gettypedata(self , typename , coluname ):
        try:
            index = (self.list_types).index( typename )
            return (self.list_coloums[index]).getData(coluname)
        except:
            print "Not foud Index"

#CONST_coloum_memtype = ["Total" , "PrivateDirty" , "Clean" , "SwappedDirty" , "Heap_size" ,"Heap_Alloc" , "Heap_Free" ]
#cola = Clist_coloum(CONST_coloum_memtype)
#print cola
#colb = Clist_coloum(CONST_coloum_memtype)
#print colb
#cola.setData("Total", 1)
#cola.setData("Total", 2)
#cola.setData("Total", 3)
#cola.setData("Clean", 11)
#cola.setData("Clean", 12)
#print cola.getData("Total")
#print cola.getData("Clean")
#
#colb.setData("Total", 51)
#colb.setData("Total", 52)
#colb.setData("PrivateDirty", 101)
#colb.setData("PrivateDirty", 102)
#print colb.getData("Total")
#print colb.getData("PrivateDirty")
#
#meminfo  = Clist_type()
#meminfo.settag("Native Heap" , CONST_coloum_memtype)
#meminfo.settag("Davil Heap" , CONST_coloum_memtype)
#meminfo.settypedata("Native Heap", "Total", 1)
#meminfo.settypedata("Native Heap", "Total", 2)
#meminfo.settypedata("Native Heap", "Heap_size", 50)
#meminfo.settypedata("Native Heap", "Heap_size", 51)
#meminfo.settypedata("Davil Heap", "Total", 101 )
#meminfo.settypedata("Davil Heap", "Total", 102 )
#meminfo.settypedata("Davil Heap", "Total", 103 )
#print meminfo.gettypedata("Native Heap", "Total" )
#print meminfo.gettypedata("Native Heap", "Heap_size" )
#print meminfo.gettypedata("Davil Heap", "Total" )

import os
import datetime
import time
import sys

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
    CONST_coloum_memtype = ["Total" , "PrivateDirty" , "Clean" , "SwappedDirty" , "Heap_size" ,"Heap_Alloc" , "Heap_Free" ]    
    list_tag = ['Native Heap' , 'Dalvik Heap' , '.dex mmap','Other mmap']   
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
#            self.writeResult( nindexname )
#     
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
