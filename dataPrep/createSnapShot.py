# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 03:02:37 2022

@author: aravi
"""

import pandas as pd
import numpy as np


class snapshot:
    
    def __init__(self,filepath,intervalSize):
        # id,time,vd,vo,lp,isbuy
        self.data = self.getdata(filepath)
        self.intervalSize = intervalSize 
        self.sell, self.buy = [],[]
        self.sellSize,self.buySize = 0,0
        self.BASpread, self.volatility = 0,0
        
    def getdata(self,filepath):
        df = np.loadtxt('numpydatabook.txt',dtype = np.float32)
        return df
        
    def resetState(self):
        self.sell, self.buy = [],[]
        self.sellSize, self.buySize = 0,0
        print("Creating a new Snap of the limit-book..")
    
    def sortHeap(self):
        ## heap will be implemented in later updates
        self.buy.sort(reverse=True)
        self.sell.sort()
        
    
    def generateSnap(self,startTime):
        
        self.resetState()
        
        for row in self.data:
            if row[1] < startTime+self.intervalSize:
                if row[-1]==1:
                    self.buy.append(row)
                    self.buySize+=1
                else:
                    self.sell.append(row)
                    self.sellSize+=1
        
        self.sortHeap()
        
    ##function to display stuff
                    
        

            





            