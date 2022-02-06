# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 03:02:37 2022

@author: aravi
"""

import pandas as pd
import numpy as np

## class for creating snapshots
class snapshot:
    
    def __init__(self,filepath,intervalSize):
        # id,time,vd,vo,lp,isbuy
   
        ## Load data onto a numpy array
        self.data = self.getdata(filepath)
        ## store the interval size/step size --> can be changed for finer control
        self.intervalSize = intervalSize 
        
        ## initialising the descriptors of the state
        self.sell, self.buy = [],[]
        self.sellSize,self.buySize = 0,0
        self.BASpread, self.volatility = 0,0
        
    def getdata(self,filepath): ## function to load data from the filepath
        df = np.loadtxt(filepath,dtype = np.float32)
        return df
        
    ## This function resets the state and sets it back to the initial empty condition
    def resetState(self):
        self.sell, self.buy = [],[]
        self.sellSize, self.buySize = 0,0
        print("Initialising a new Snap of the limit-book..")
    
    def sortHeap(self):
        ## heap will be implemented in later updates
        self.buy.sort(reverse=True)
        self.sell.sort()
        
    
    def generateSnap(self,startTime):
        ## reset leftovers from the last state
        self.resetState()
        
        ## Iterate through all transactions within the intervalSize
        for row in self.data:
            if row[1] < startTime+self.intervalSize:
                if row[-1]==1:
                    self.buy.append(row)
                    self.buySize+=1
                else:
                    self.sell.append(row)
                    self.sellSize+=1
                        
        ## sort the buy side and sell side postings and generate current snapshot
        self.sortHeap()
        self.calculate_state()
    
    def calculate_state():
        self.BASpread = max(self.sell[0]-self.buy[0],0)
        self.volatility = self.stddev()

    ##function to display stuff
                    
        

            





            
