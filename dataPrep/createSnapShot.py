# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 03:02:37 2022

@author: aravi
"""

import pandas as pd
import numpy as np

## class for creating snapshots
class orderbook:
    def __init__(self,filepath,intervalSize):
        # id,time,vd,vo,lp,isbuy
   
        ## Load data onto a numpy array
        self.data = self.getdata(filepath)
        ## store the interval size/step size --> can be changed for finer control
        self.intervalSize = intervalSize * 60
        self.tstart = self.data[0][1]
        self.tend = self.data[-1][1]
        
        self.snaps = []
        self.generate_snaps()        
    
    def getdata(self,filepath): ## function to load data from the filepath
        df = np.loadtxt(filepath,dtype = np.float32)
        return df
    
    def generate_snaps(self):
        start = self.tstart
        while start+self.intervalSize < self.tend:
            snap = snapshot(self.data,start,self.intervalSize)
            self.snaps.append(snap)
            start+=self.intervalSize       

class snapshot:
    
    def __init__(self,orderbook,startTime,intervalSize):
        self.data = orderbook
        self.startTime = startTime
        self.intervalSize = intervalSize
        ## initialising the descriptors of the state
        self.sell, self.buy= [],[]
        self.trade_list = []
        self.sellSize,self.buySize,self.tradeSize = 0,0,0
        self.BASpread, self.volatility = 0,{"buy":0,"sell":0,"trade":0}
        
        self.generateSnap()

        
    ## This function resets the state and sets it back to the initial empty condition
    def resetState(self):
        self.sell, self.buy = [],[]
        self.trade_list = []
        self.sellSize, self.buySize, self.tradeSize = 0,0,0
        print("Initialising a new Snap of the limit-book..")
    
    def sortHeap(self):
        ## heap will be implemented in later updates
        if self.buy:    
            self.buy.sort()
        if self.sell:
            self.sell.sort(reverse=True)
        
    def trade_act(self): ## this function executes trades in the current limit order snapshot
        if not self.buy or not self.sell:
            return
        highest_buy = self.buy[-1]
        lowest_sell = self.sell[-1]
        if lowest_sell <= highest_buy:
            # print(self.trade_list)
            self.trade_list.append((highest_buy,lowest_sell))
            self.buy.pop()
            self.sell.pop()
            self.tradeSize+=1
            
            # self.sellSize-=1
            # self.buySize-=1
        
    def generateSnap(self):
        ## reset leftovers from the last state
        self.resetState()
        
        ## Iterate through all transactions within the intervalSize
        for row in self.data:
            if row[1] < self.startTime+self.intervalSize:
                if row[-1]==1:
                    self.buy.append(row[1])
                    self.buySize+=1
                else:
                    self.sell.append(row[1])
                    self.sellSize+=1
                
                ## sort the buy side and sell side postings and generate current snapshot
                self.sortHeap()
                self.trade_act()
                        
        
        self.calculate_state()
    
    def find_volatility(self):
        trade = np.array(self.trade_list)
        buy = np.array(self.buy)
        sell = np.array(self.sell)
        self.volatility["trade"] = np.std(trade)
        self.volatility["buy"] = np.std(buy)
        self.volatility["sell"] = np.std(sell)
        
    
    def calculate_state(self):
        if self.buy and self.sell:
            self.BASpread = max(self.sell[-1]-self.buy[-1],0)
        self.find_volatility()

    ##function to display stuff
    def describe(self):
        print("SELL SIDE")
        for i in range(1,min(len(self.sell),6)):
            print(self.sell[-6+i])
        
        print("<---------->")
        for i in range(1,min(len(self.buy),6)):
            print(self.buy[-i])
        print("BUY SIDE")
            
        for key in self.volatility:
            print(f"Volatility : {key} = {self.volatility[key]}")
        
        print(f"Current bid ask spread = {self.BASpread}")
            

Order = orderbook("../data/numpydatabook.txt",30)
Order.snaps[0].describe()
        
                    
        

            





            
