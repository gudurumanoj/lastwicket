## standard imports
import argparse
import numpy as np

## argument parser
parser = argparse.ArgumentParser()

## class to convert the output into required format
class decoder():
    ## init
    def __init__(self, valpolfilepath, statespath):
        self.valpolfilepath = valpolfilepath
        self.statespath = statespath
        self.statestonum, self.numtostates = self.extractstates()
        self.numtoaction = np.array([0, 1, 2, 4, 6])
        self.valpol, self.action = self.extractvalpol()
        self.noofstates = (int(self.numtostates[0][0:2]) * int(self.numtostates[0][2:]))
        self.printoutput()

    ## function to extract value policy from the file
    def extractvalpol(self,):
        lines = open(self.valpolfilepath).read().strip()
        lines = lines.split("\n")
        valpol = []
        action = []
        for line in lines:
            l = line.split()
            val = float(l[0])
            act = int(l[1])
            valpol.append(val)
            action.append(self.numtoaction[act])
        return np.array(valpol), np.array(action)


    ## function to extract states from the states file
    def extractstates(self,):
        lines = open(self.statespath).read().strip()
        lines = lines.split("\n")
        statestonum = dict()
        numtostates = dict()
        count = 0
        for line in lines:
            statestonum[line] = count
            numtostates[count] = line
            count += 1
        return statestonum, numtostates


    ## function to print in the given format
    def printoutput(self,):
        for i in range(0, self.noofstates):
            print(self.numtostates[i],self.action[i],'{:.6f}'.format(round(self.valpol[i], 6)))

if __name__ == "__main__":
    
    ## parsing args 
    parser.add_argument("--value-policy",type=str)
    parser.add_argument("--states",type=str)
    args = parser.parse_args()
    decoder(args.value_policy, args.states)
