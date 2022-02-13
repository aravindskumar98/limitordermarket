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
        for data in self.data_array:
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
        print('----------------------------------------------')
        ## store the interval size/step size --> can be changed for finer control
        self.intervalSize = intervalSize
        self.tstart = self.data[0][2]
        self.tend = self.data[-1][2]
        
        self.snaps = []
        self.generate_snaps()        
    

    
    def generate_snaps(self):
        start = self.tstart
        while start+self.intervalSize < self.tend:
            snap = snapshot(self.data,start,self.intervalSize)
            snap.describe()
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
            if row[2] < self.startTime+self.intervalSize:
                if row[-1]==1:
                    self.buy.append(row[2])
                    self.buySize+=1
                else:
                    self.sell.append(row[2])
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
            self.BASpread = self.sell[-1]-self.buy[-1]
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
            

Env = env("../data/numpydatabook1.txt",30)
Env.orderbook_daily[3].snaps
        
                    
        

            





            
