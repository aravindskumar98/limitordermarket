import numpy as np
from createSnapShot import env


class ActionSpace():

    def __init__(orderbook,num_split,side,multiplier): ##num_split specifies how close the potential actions are spaced
        self.snapshots = orderbook.snaps
        self.num_split = num_split
        self.multiplier = multiplier ##multiplier for the spread
        self.side = side ## specifies if buy or sell
        self.intervalSize = orderbook.intervalSize
        self.actions_for_snaps = []
        self.generate_actions()

    ## This function generates all potential actions 
    ## for all snapshots within the orderbook
    def generate_actions(self):
        for snap in self.snapshots:
            potentialActions = self.generateActionSpace(snap)
            self.actions_for_snaps.append((potentialActions,snap))
    
    ## for a given snapshot 
    ## generate potential actions according to the split value
    def generateActionSpace(self,snap):
        highest_buy = snap.buy[-1]
        lowest_sell = snap.sell[-1]
        spread = self.multiplier*snap.BASpread
        potentialActions = None
        if self.side = 'buy':
            left = highest_buy - spread
            right = highest_buy + spread
            potentialActions = np.arange(left,right,spread/self.num_split)
    
        elif self.side = 'sell':
            left = lowest_sell - spread
            right = lowest_sell + spread
            potentialActions = np.arange(left,right,spread/self.num_split)
        else:
            print("Order Execution Failed")

        return potentialActions


    


