## standard imports
import argparse
from asyncore import readwrite
import numpy as np

## argument parser
parser = argparse.ArgumentParser()


## class to encode the game as mdp
class encoder():
    ## init
    def __init__(self, statespath, parameterspath, q):
        self.statespath = statespath
        self.parameterspath = parameterspath
        self.q = float(q)
        self.params = self.extractparameters()
        actions = np.array([0, 1, 2, 4, 6])
        possa = np.array([-1, 0, 1, 2, 3, 4, 6])
        possb = np.array([-1, 0, 1])
        noofactions = len(actions)
        noofstates, statetonum, states = self.extractstates()
        transitionfunc, rewardfunc =  self.encodeasmdp(actions, possa, possb, noofactions, noofstates, states, self.params, self.q, statetonum)
        self.printoutput(noofstates, noofactions, transitionfunc, rewardfunc)


    ## function to extract parameters
    def extractparameters(self,):
        lines = open(self.parameterspath).read().strip()
        lines = lines.split("\n")
        params = np.zeros((5, 7))
        for i in range(1, 6):
            line = lines[i].split()
            for j in range(1, 8):
                params[i-1][j-1] = float(line[j])
        return params

    ## function to extract states from statesfile
    def extractstates(self,):
        lines = open(self.statespath).read().strip()
        lines = lines.split("\n")
        statesa = [(i + "0") for i in lines]
        statesb = [(i + "1") for i in lines]
        states = statesa + statesb + ["win"] + ["loss"]

        noofstates = len(states)

        statetonum = {}

        for i in range(len(states)):
            statetonum[states[i]] = i
        return noofstates, statetonum, states

    ## function to encode the game as mdp
    def encodeasmdp(self,actions,possa,possb,noofactions,noofstates,states,params, q,statetonum):
        transitionfunc = np.zeros((noofstates, noofactions, noofstates))
        rewardfunc = np.zeros((noofstates, noofactions, noofstates))
        for i in range(noofstates-2):
            balls = int(states[i][0:2])
            runs = int(states[i][2:4])
            player = int(states[i][4])
            if (player == 0):                               ## when the batsman isn't tailender
                for j in range(len(actions)):
                    for k in range(len(possa)):
                        if (params[j][k] > 1e-6):
                            if ((possa[k] == -1) or ((balls == 1) and (runs > possa[k]))):      ## direct losing case
                                transitionfunc[i][j][noofstates-1] += params[j][k] 
                            elif (runs <= possa[k]):                                            ## direct winning case
                                transitionfunc[i][j][noofstates-2] += params[j][k]
                                rewardfunc[i][j][noofstates-2] = 1
                            else :                                                              ## all other cases
                                score = int(possa[k])
                                ballsleft = balls - 1
                                runsleft = runs - score
                                strikechange = player
                                if ((ballsleft%6 != 0 and score%2 == 1) or (ballsleft%6 == 0 and score%2 == 0)):    ## strike change check
                                    strikechange = 1 - player
                                ballsleft = (str(ballsleft)).zfill(2)
                                runsleft = (str(runsleft)).zfill(2)
                                nextstate = ballsleft + runsleft + str(strikechange)
                                nextstate = statetonum[nextstate]
                                transitionfunc[i][j][nextstate] += params[j][k]
            else:                                                                   ## when the batsman is tailender
                for j in range(len(actions)):
                    for k in range(len(possb)):
                        if (possb[k] == -1):                                        ## direct losing case
                            transitionfunc[i][j][noofstates-1] += q 
                        elif (((balls == 1) and (runs > possb[k]))):                ## direct losing case            
                            transitionfunc[i][j][noofstates-1] += (1-q)/2
                        elif (runs <= possb[k]):                                    ## direct winning case
                            transitionfunc[i][j][noofstates-2] += (1-q)/2
                            rewardfunc[i][j][noofstates-2] = 1
                        else :                                                      ## all other cases
                            score = int(possb[k])
                            ballsleft = balls - 1
                            runsleft = runs - score
                            strikechange = player
                            if ((ballsleft%6 != 0 and score%2 == 1) or (ballsleft%6 == 0 and score%2 == 0)):        ## strike change check
                                strikechange = 1 - player
                            ballsleft = (str(ballsleft)).zfill(2)
                            runsleft = (str(runsleft)).zfill(2)
                            nextstate = ballsleft + runsleft + str(strikechange)
                            nextstate = statetonum[nextstate]
                            transitionfunc[i][j][nextstate] += (1-q)/2 
        return transitionfunc, rewardfunc

    def printoutput(self,noofstates, noofactions, transitionfunc, rewardfunc):
        print("numStates", noofstates)
        print("numActions", noofactions)
        print("end", noofstates-1, noofstates-2)
        for i in range(noofstates):
            for j in range(noofactions):
                for k in range(noofstates):
                    if transitionfunc[i][j][k] !=0:         ## printing only when there is a transition
                        print("transition", i, j, k, rewardfunc[i][j][k],transitionfunc[i][j][k])
        print("mdptype episodic")
        print("discount", 1.0)              


if __name__ == "__main__":
    
    ## parsing args 
    parser.add_argument("--states",type=str)
    parser.add_argument("--parameters",type=str)
    parser.add_argument("--q",type=str)
    args = parser.parse_args()

    encoder(args.states, args.parameters, args.q)
