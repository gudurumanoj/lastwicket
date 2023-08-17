## standard imports
import argparse
import numpy as np
import pulp

## argument parser
parser = argparse.ArgumentParser()

## algorithm solver class
class planner():
    ## init 
    def __init__(self, mdppath, algorithm, policy = None) :
        self.mdp = self.extractmdp(mdppath)
        if policy == None:
            if algorithm == "vi":
                self.valuefunc, self.policy = self.valueiteration()
            elif algorithm == "hpi":
                self.valuefunc, self.policy = self.howardpolicyiteration()
            else:
                self.valuefunc, self.policy = self.linearprogramming()
        else:
            self.policy = self.extractpolicy(policy)
            self.valuefunc = self.evalpolicy(self.policy, self.mdp["noofstates"])
        self.printoutput()


    ## function to extract mdp from the text file
    def extractmdp(self, mdppath):
        mdp = dict()
        lines = open(mdppath).read().strip()
        lines = lines.split("\n")
        for line in lines:
            l = line.split()
            if l[0] == "transition":
                s1 = int(l[1])
                ac = int(l[2])
                s2 = int(l[3])
                r = float(l[4])
                p = float(l[5])
                mdp["transitionfunc"][s1][ac][s2] = p
                mdp["rewardfunc"][s1][ac][s2] = r
            elif l[0] == "numStates":
                mdp["noofstates"] = int(l[1])
            elif l[0] == "numActions":
                mdp["noofactions"] = int(l[1])
                ## initialising transition and reward funtion
                mdp["transitionfunc"] = np.zeros((mdp["noofstates"], mdp["noofactions"], mdp["noofstates"]))
                mdp["rewardfunc"] = np.zeros((mdp["noofstates"], mdp["noofactions"], mdp["noofstates"]))
            elif l[0] == "mdptype":
                mdp["mdptype"] = l[1]
            elif l[0] == "discount":
                mdp["discountfactor"] = float(l[1])
            elif l[0] == "end":
                pass
        return mdp

    ## function to extract policy
    def extractpolicy(self, policypath):
        policy = []
        lines = open(policypath).read().strip()
        lines = lines.split("\n")
        for line in lines:
            policy.append(int(line))
        return np.array(policy)

    ## function for value iteration
    def valueiteration(self,):
        noofstates = int(self.mdp["noofstates"])
        v = np.zeros(noofstates)        ## initial value function
        vdash = np.zeros(noofstates)    ## value function after applying the operator
        while(True):                    ## iterating until all are within a tolerance of 1e-8 since precision is only upto 6
            vdash = np.sum(self.mdp["transitionfunc"]*(self.mdp["rewardfunc"] + self.mdp["discountfactor"]*v), axis=2)
            vdash = np.max(vdash, axis = 1)
            if(np.sum(vdash - v < 1e-8) == noofstates ):
                break
            v = vdash
        policy = np.sum(self.mdp["transitionfunc"]*(self.mdp["rewardfunc"] + self.mdp["discountfactor"]*v), axis=2)
        policy = np.argmax(policy, axis = 1)
        return vdash, policy


    ## function for linear programming
    def linearprogramming(self,):
        lpsolver = pulp.LpProblem('linearprogformdp', pulp.LpMaximize)    ## the linear program solver
        noofstates = self.mdp["noofstates"]
        noofactions = self.mdp["noofactions"]
        vars = ["v" + str(i) for i in range(0, noofstates)]              ## creating the linear programs variables's names
        v = [pulp.LpVariable(i) for i in vars]                ## converting them into pulp variables
        v = np.array(v)                                     ## putting them into numpy array to make calculation easier later
        lpsolver += (-pulp.lpSum(v))                           ## the objective function

        for s in range(0, noofstates):
            for a in range(0, noofactions):
                lpsolver += v[s] >= pulp.lpSum(self.mdp["transitionfunc"][s][a]*(self.mdp["rewardfunc"][s][a] + self.mdp["discountfactor"]*v))

        lpsolver.solve(pulp.PULP_CBC_CMD(msg=False))        ## to make pulp print nothing on the terminal

        valfunc = []
        for i in range(0, noofstates):
            valfunc.append(pulp.value(v[i])) 
        valfunc = np.array(valfunc)
        policy = np.sum(self.mdp["transitionfunc"]*(self.mdp["rewardfunc"] + self.mdp["discountfactor"] * valfunc), axis=2)
        policy = np.argmax(policy, axis = 1)
        return valfunc, policy


    ## function for howard policy iteration
    def howardpolicyiteration(self,):
        noofstates = self.mdp["noofstates"]
        noofactions = self.mdp["noofactions"]
        policy = np.random.randint(low=0, high=noofactions, size=noofstates)            ## random initialisation of actions for the states
        policydash = np.random.randint(low=0, high=noofactions, size=noofstates)
        valfunc = None
        while(True):
            valfunc = self.evalpolicy(policy, noofstates)       ## doing policy evaluation
            policydash = np.sum(self.mdp["transitionfunc"]*(self.mdp["rewardfunc"] + self.mdp["discountfactor"]*valfunc), axis=2)
            policydash = np.argmax(policydash, axis = 1)
            if np.array_equal(policydash, policy):
                break
            policy = policydash
        return valfunc, policydash
        

    ## function for evaluating given policy
    def evalpolicy(self, policy, noofstates):
        statearray = np.arange(noofstates)
        transitionfunc = self.mdp["transitionfunc"][statearray,policy]
        rewardfunc = self.mdp["rewardfunc"][statearray,policy]
        tr = np.sum(transitionfunc*rewardfunc, axis=1)
        tr = np.reshape(tr,(tr.shape[0],1))
        invmat = np.linalg.inv(np.identity(noofstates) - self.mdp["discountfactor"]*transitionfunc)
        v = np.matmul(invmat, tr)
        v = np.reshape(v,(v.shape[0]))
        return v

    ## function to print the output
    def printoutput(self,):
        for i in range(0,self.mdp["noofstates"]):
            print('{:.6f}'.format(round(self.valuefunc[i], 6))," ",self.policy[i])

if __name__ == "__main__":
    
    ## parsing args 
    parser.add_argument("--mdp",type=str)
    parser.add_argument("--algorithm",type=str,default="vi")
    parser.add_argument("--policy",type=str)
    args = parser.parse_args()

    ## calling planner to solve
    planner(args.mdp, args.algorithm,args.policy)
