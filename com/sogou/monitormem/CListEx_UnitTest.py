# encoding: utf-8

'''
Created on 2016年4月4日

@author: Dongming
'''

import unittest
from CListEx import Clist_coloum
from CListEx import Clist_type

class UnitTest(unittest.TestCase):
    def setUp(self):
        self.CONST_coloum_memtype = ["Total" , "PrivateDirty" , "Clean" , "SwappedDirty" , "Heap_size" ,"Heap_Alloc" , "Heap_Free" ]


    def testClist_coloum(self):
        cola = Clist_coloum(self.CONST_coloum_memtype)
        #print cola
        colb = Clist_coloum(self.CONST_coloum_memtype)
        #print colb
        cola.setData("Total", 1)
        cola.setData("Total", 2)
        cola.setData("Total", 3)
        cola.setData("Clean", 11)
        cola.setData("Clean", 12)

        colb.setData("Total", 51)
        colb.setData("Total", 52)
        colb.setData("PrivateDirty", 101)
        colb.setData("PrivateDirty", 102)

        self.assertEquals(cola.getData("Total") , [1,2,3])
        self.assertEquals(cola.getData("Clean") , [11,12])

        self.assertEquals(colb.getData("Total") , [51,52])
        self.assertEquals(colb.getData("PrivateDirty") , [101,102])


    def testClist_type(self):
        meminfo  = Clist_type()
        meminfo.settag("Native Heap" , self.CONST_coloum_memtype)
        meminfo.settag("Davil Heap" , self.CONST_coloum_memtype)
        meminfo.settypedata("Native Heap", "Total", 1)
        meminfo.settypedata("Native Heap", "Total", 2)
        meminfo.settypedata("Native Heap", "Heap_size", 50)
        meminfo.settypedata("Native Heap", "Heap_size", 51)
        meminfo.settypedata("Davil Heap", "Total", 101 )
        meminfo.settypedata("Davil Heap", "Total", 102 )
        meminfo.settypedata("Davil Heap", "Total", 103 )



        self.assertEquals (meminfo.gettypedata("Native Heap", "Total" ) , [1 , 2 ] )
        self.assertEquals (meminfo.gettypedata("Native Heap", "Heap_size" ) , [50, 51])
        self.assertEquals (meminfo.gettypedata("Davil Heap", "Total" ) , [101 , 102, 103])

if __name__ == '__main__':
    unittest.main()