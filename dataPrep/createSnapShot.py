# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 03:02:37 2022

@author: aravi
"""

import pandas as pd
import numpy as np

class env():
    
    def __init__(self,filepath,intervalSize):
        self.data_array = None
        self.load_data(filepath) ## Creates array of numpy array based on date
        self.orderbook_daily = []
        self.intervalSize = intervalSize * 60 ## in seconds
        for i,data in enumerate(self.data_array):
            print("Day : ",i+1)
            print('---------')
            self.orderbook_daily.append(Orderbook(data,self.intervalSize))

    def load_data(self,filepath):
        df = np.loadtxt(filepath,dtype = np.float32)
        self.data_array = np.split(df, np.where(np.diff(df[:,1]))[0]+1)

## class for creating snapshots
class Orderbook:
    def __init__(self,data,intervalSize):
        # id,date,time,vd,vo,lp,isbuy
   
        ## Load data onto a numpy array
        self.data = data
        ## store the interval size/step size --> can be changed for finer control
        self.intervalSize = intervalSize
        self.tstart = self.data[0][2]
        self.tend = self.data[-1][2]
        # print(self.tstart,self.tend)
        
        self.snaps = []
        self.generate_snaps()        
    
    def generate_snaps(self):
        start = self.tstart
        count = 1
        while start+self.intervalSize < self.tend:
            print("Interval Number : ",count)
            snap = snapshot(self.data,start,self.intervalSize)
            snap.describe()
            print("..")
            self.snaps.append(snap)
            start+=self.intervalSize  
            count+=1

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
        print("..")
    
    def sortHeap(self):
        ## heap will be implemented in later updates
        if self.buy:    
            self.buy.sort()
        if self.sell:
            self.sell.sort(reverse=True)
        
    def trade_act(self): ## this function executes trades in the current limit order snapshot
        if not self.buy or not self.sell:
            return
        
        while self.sell and self.buy and self.sell[-1][0] <= self.buy[-1][0]:
            # print(self.trade_list)
            tradeVal = min(self.buy[-1][1],self.sell[-1][1])
            self.trade_list.append((self.buy[-1][0],self.sell[-1][0],tradeVal))
            self.buy[-1][1]-=tradeVal
            self.sell[-1][1]-=tradeVal
            if self.buy[-1][1]==0:
                self.buy.pop()
            if self.sell[-1][1]==0:
                self.sell.pop()
            self.tradeSize+=1
            
    def generateSnap(self):
        ## reset leftovers from the last state
        self.resetState()
        
        ## Iterate through all transactions within the intervalSize
        for row in self.data:
            # print(row)
            if row[2] < self.startTime+self.intervalSize:
                if row[5]==0:
                    continue ### Assuming that garbage values can be removed
                elif row[-1]==1:
                    self.buy.append([row[5],row[4]])
                    self.buySize+=1
                else:
                    self.sell.append([row[5],row[4]])
                    self.sellSize+=1
                
                ## sort the buy side and sell side postings and generate current snapshot
                self.sortHeap()
                self.trade_act()
                        
        
        self.calculate_state()
    
    def find_volatility(self):
        trade = np.array(self.trade_list)
        buy = np.array(self.buy)
        sell = np.array(self.sell)
        self.volatility["trade"] = np.std(trade[:,0])
        self.volatility["buy"] = np.std(buy[:,0])
        self.volatility["sell"] = np.std(sell[:,0])
        
    
    def calculate_state(self):
        if self.buy and self.sell:
            self.BASpread = self.sell[-1][0]-self.buy[-1][0]
        self.find_volatility()

    ##function to display stuff
    def describe(self):
        print("SELL SIDE")
        size = min(len(self.sell),6)
        for i in range(1,min(len(self.sell),6)):
            print(self.sell[-size+i])
        
        print("<---------->")
        for i in range(1,min(len(self.buy),6)):
            print(self.buy[-i])
        print("BUY SIDE")
            
        for key in self.volatility:
            print(f"Volatility : {key} = {self.volatility[key]}")
        
        print(f"Current bid ask spread = {self.BASpread}")
            

Env = env("../data/numpydatabook.txt",30)

        

            





            
