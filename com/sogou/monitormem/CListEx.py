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
        #print self.list_datas
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
