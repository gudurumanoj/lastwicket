# ## standard imports
# import argparse
# import numpy as np

# ## argument parser
# parser = argparse.ArgumentParser()

# ## class to encode the game as mdp
# class encoder():
#     ## init
#     def __init__(self, statespath, parameterspath, q):
#         self.statespath = statespath
#         self.parameterspath = parameterspath
#         self.q = q
#         self.parameters = self.extractparameters()
#         self.statestonum, self.numtostates = self.extractstates()
#         self.noofstates = (int(self.numtostates[0][0:2]) * int(self.numtostates[0][2:])) + 2    ## two extra states, one for win and one for loss
#         self.statestonum["win"] = self.noofstates - 2
#         self.statestonum["loss"] = self.noofstates -1
#         self.numtostates[self.noofstates - 2] = "win"
#         self.numtostates[self.noofstates - 1] = "loss"
#         self.noofactions = 5
#         self.actionstonum = {0:0, 1:1, 2:2, 4:3, 6:4}
#         self.numtoactions = {0:0, 1:1, 2:2, 3:4, 4:6}


#     ## function to extract parameters
#     def extractparameters(self,):
#         parameters = dict()
#         lines = open(self.parameterspath).read().strip()
#         lines = lines.split("\n")
#         for line in lines:
#             l = line.split()
#             if l[0] != "action":
#                 problist = []
#                 for i in range(1,8):
#                     problist.append(float(l[i]))
#                 parameters[int(l[0])] = np.array(problist)
#         return parameters

#     ## function to extract states from statesfile
#     def extractstates(self,):
#         lines = open(self.statespath).read().strip()
#         lines = lines.split("\n")
#         statestonum = dict()
#         numtostates = dict()
#         count = 0
#         for line in lines:
#             statestonum[line] = count
#             numtostates[count] = line
#             count += 1
#         return statestonum, numtostates 

#     ## function to encode the game as mdp
#     def encodeasmdp(self,):
#         mdp = dict()
#         noofstates = self.noofstates
#         noofactions = self.noofactions
#         params = self.parameters
#         lines = []
#         actionstonum = {0:0, 1:1, 2:2, 4:3, 6:4}
#         numtoactions = {0:0, 1:1, 2:2, 3:4, 4:6}
#         outcomestonum = {-1:0 ,0:1, 1:2, 2:3, 3:4, 4:5, 6:6}
#         numtooutcomes = {0:-1, 1:0, 2:1, 3:2, 4:3, 5:4, 6:6}
#         mdp["transitionfunc"] = np.zeros((mdp["noofstates"], mdp["noofactions"], mdp["noofstates"]))
#         mdp["rewardfunc"] = np.zeros((mdp["noofstates"], mdp["noofactions"], mdp["noofstates"]))
#         for i in range(0, self.noofstates):
#             balls = int(self.numtostates[i][0:2])
#             runs = int(self.numtostates[i][2:4])
#             for j in range(0,5):        ## j represents each action's number
#                 for k in range(0,7):    ## k represents the possible outcome's number
#                     if(numtooutcomes[k] == -1) or ((balls == 1) and (runs > numtooutcomes[k])):     ## direct losing case
#                         mdp["transitionfunc"][i][j][noofstates-1] += params[numtoactions[j]][k]
#                         mdp["rewardfunc"][i][j][noofstates-1] = 0
#                     elif runs <= numtooutcomes[k]:                                                  ## direct winning case 
#                         #lines.append(i, j, noofstates-2, 1, params[numtoactions[j]][k])
#                         mdp["transitionfunc"][i][j][noofstates-2] += params[numtoactions[j]][k]
#                         mdp["rewardfunc"][i][j][noofstates-2] = 0
#                     else:                                                                   ## all other cases
#                         if balls%6 == 1:                                                    ## overchange happens
#                             if(numtooutcomes[k]%2 == 1):                                    ## odd no of runs, batsman stays in the crease
#                                 toruns = runs - numtooutcomes[k]
#                                 toballs = balls -1
#                                 toballs = (str(toballs)).zfill(2)
#                                 toruns = (str(toruns)).zfill(2)
#                                 nextstate = self.statestonum[toballs + toruns]
#                                 # lines.append((i, j, nextstate, 0, params[numtoactions[j]][k]))
#                                 mdp["transitionfunc"][i][j][nextstate] += params[numtoactions[j]][k]
#                                 mdp["rewardfunc"][i][j][nextstate] = 0
#                         else:                                                               ## no overchange case
#                             if(numtooutcomes[k]%2 == 0):                                    ## even no of runs, batsman stays in the crease
#                                 toruns = runs - numtooutcomes[k]
#                                 toballs = balls -1
#                                 toballs = (str(toballs)).zfill(2)
#                                 toruns = (str(toruns)).zfill(2)
#                                 nextstate = self.statestonum[toballs + toruns]
#                                 # lines.append((i, j, nextstate, 0, params[numtoactions[j]][k]))
#                                 mdp["transitionfunc"][i][j][nextstate] += params[numtoactions[j]][k]
#                                 mdp["rewardfunc"][i][j][nextstate] = 0
    



# if __name__ == "__main__":
    
#     ## parsing args 
#     parser.add_argument("--states",type=str)
#     parser.add_argument("--parameters",type=str)
#     parser.add_argument("--q",type=str)
#     args = parser.parse_args()

#     encoder(args.states, args.parameters, args.q)


##############################################################################################################################

## standard imports
import argparse
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
        self.parameters = self.extractparameters()
        self.statestonum, self.numtostates, self.noofstates = self.extractstates()
        actions = np.array([0, 1, 2, 4, 6])
        outcomes = np.array([-1, 0, 1, 2, 3, 4, 6])
        boutcomes = np.array([-1, 0, 1])
        A = len(actions)
        self.noofactions = 5
        self.actionstonum = {0:0, 1:1, 2:2, 4:3, 6:4}
        self.numtoactions = {0:0, 1:1, 2:2, 3:4, 4:6}
        self.mdp = self.encodeasmdp(actions,outcomes,boutcomes,A)
        self.printoutput()


    ## function to extract parameters
    def extractparameters(self,):
        parameters = dict()
        lines = open(self.parameterspath).read().strip()
        lines = lines.split("\n")
        count = 0
        probs = np.zeros((5, 7))
        for line in lines:
            l = line.split()
            if l[0] != "action":
                for i in range(1,8):
                    probs[count-1][i-1] = float(l[i])
            count += 1   
        print(probs)
        return probs

    ## function to extract states from statesfile
    def extractstates(self,):
        lines = open(self.statespath).read().strip()
        lines = lines.split("\n")
        statestonum = dict()
        numtostates = dict()
        statesbatsman = [(i + "0") for i in lines]              ## indicates state of the main batsman
        statestailender = [(i + "1") for i in lines]            ## indicates the state of the tail ender
        states = statesbatsman + statestailender
        states += ["win", "loss"]
        for i in range(0, len(states)):
            statestonum[states[i]] = i
            numtostates[i] = states[i]
        return statestonum, numtostates, len(states)

    ## function to encode the game as mdp
    def encodeasmdp(self,actions,outcomes,boutcomes,A,S,states,probs, q,mapStrToState):
        # mdp = dict()
        # noofstates = self.noofstates
        # noofactions = self.noofactions
        # params = self.parameters
        # # lines = []
        # numtoactions = {0:0, 1:1, 2:2, 3:4, 4:6}
        # numtooutcomes = {0:-1, 1:0, 2:1, 3:2, 4:3, 5:4, 6:6}
        # numtooutcomesb = {0:-1, 1:0, 2:1}
        # mdp["transitionfunc"] = np.zeros((noofstates, noofactions, noofstates))
        # mdp["rewardfunc"] = np.zeros((noofstates, noofactions, noofstates))
        # for i in range(0, self.noofstates-2):
        #     balls = int(self.numtostates[i][0:2])
        #     runs = int(self.numtostates[i][2:4])
        #     batsman = int(self.numtostates[i][4])
        #     if batsman == 0:
        #         for j in range(0,5):        ## j represents each action's number
        #             for k in range(0,7):    ## k represents the possible outcome's number
        #                 if((numtooutcomes[k] == -1) or ((balls == 1) and (runs > numtooutcomes[k]))):     ## direct losing case
        #                     mdp["transitionfunc"][i][j][noofstates-1] += params[numtoactions[j]][k]
        #                     mdp["rewardfunc"][i][j][noofstates-1] = 0
        #                 elif runs <= numtooutcomes[k]:                                                  ## direct winning case 
        #                     #lines.append(i, j, noofstates-2, 1, params[numtoactions[j]][k])
        #                     mdp["transitionfunc"][i][j][noofstates-2] += params[numtoactions[j]][k]
        #                     mdp["rewardfunc"][i][j][noofstates-2] = 1
        #                 else:                                                                   ## all other cases
        #                     score = int(numtooutcomes[k])
        #                     ballsleft = balls-1
        #                     runsleft = runs - score
        #                     strikechange = 0        ## will be set to 1 if a strike change's gonna happen
        #                     if(((ballsleft%6 != 0) and (score%2==1)) or ((ballsleft%6 == 0) and (score%2 == 0))):
        #                         strikechange = 1
        #                     ballsleft = (str(ballsleft)).zfill(2)
        #                     runsleft = (str(runsleft)).zfill(2)
        #                     nextstate = ballsleft + runsleft + str(strikechange)
        #                     nextstate = self.statestonum[nextstate]
        #                     mdp["transitionfunc"][i][j][nextstate] += params[numtoactions[j]][k]
        #                     mdp["rewardfunc"][i][j][nextstate] = 0
        #     else:
        #         for j in range(0,5):        ## j represents each action's number
        #             for k in range(0,3):    ## k represents the possible outcome's number
        #                 if(numtooutcomesb[k] == -1):     ## direct losing case when the non-striker gets out
        #                     mdp["transitionfunc"][i][j][noofstates-1] += self.q
        #                     mdp["rewardfunc"][i][j][noofstates-1] = 0
        #                 elif ((balls == 1) and (runs > numtooutcomesb[k])):
        #                     mdp["transitionfunc"][i][j][noofstates-1] += (1-self.q)/2
        #                     mdp["rewardfunc"][i][j][noofstates-1] = 0
        #                 elif runs <= numtooutcomesb[k]:                                                  ## direct winning case 
        #                     #lines.append(i, j, noofstates-2, 1, params[numtoactions[j]][k])
        #                     mdp["transitionfunc"][i][j][noofstates-2] += (1-self.q)/2
        #                     mdp["rewardfunc"][i][j][noofstates-2] = 1
        #                 else:                                                                   ## all other cases
        #                     score = int(numtooutcomesb[k])
        #                     ballsleft = balls-1
        #                     runsleft = runs - score
        #                     strikechange = 1            ## will be set to 0 if a strike change is gonna happen
        #                     if(((ballsleft%6 != 0) and (score%2==1)) or ((ballsleft%6 == 0) and (score%2 == 0))):
        #                         strikechange = 0
        #                     ballsleft = (str(ballsleft)).zfill(2)
        #                     runsleft = (str(runsleft)).zfill(2)
        #                     nextstate = ballsleft + runsleft + str(strikechange)
        #                     nextstate = self.statestonum[nextstate]
        #                     mdp["transitionfunc"][i][j][nextstate] += (1-self.q)/2
        #                     mdp["rewardfunc"][i][j][nextstate] = 0
        # return mdp
        transitionMatrix = np.zeros((A, S, S))

        for i in range(S-2):
            balls = int(states[i][0:2])
            runs = int(states[i][2:4])
            player = int(states[i][4])
            if (player == 0):
                for j in range(len(actions)):
                    for k in range(len(outcomes)):
                        if (probs[j][k] > 1e-6):
                            if ((outcomes[k] == -1) or ((balls == 1) and (runs > outcomes[k]))):
                                transitionMatrix[j][i][S-1] += probs[j][k] 
                            elif (runs <= outcomes[k]):
                                transitionMatrix[j][i][S-2] += probs[j][k]
                            else :
                                scored = int(outcomes[k])
                                ballsNew = balls - 1
                                runsNew = runs - scored
                                playerNew = player
                                if ((ballsNew%6 != 0 and scored%2 == 1) or (ballsNew%6 == 0 and scored%2 == 0)):
                                    playerNew = 1 - player
                                ballsNew = (str(ballsNew)).zfill(2)
                                runsNew = (str(runsNew)).zfill(2)
                                newStateStr = ballsNew + runsNew + str(playerNew)
                                newState = mapStrToState[newStateStr]
                                transitionMatrix[j][i][newState] += probs[j][k]
            else:
                for j in range(len(actions)):
                    for k in range(len(boutcomes)):
                        if (boutcomes[k] == -1):
                            transitionMatrix[j][i][S-1] += q
                        elif (((balls == 1) and (runs > boutcomes[k]))):
                            transitionMatrix[j][i][S-1] += (1-q)/2
                        elif (runs <= boutcomes[k]):
                            transitionMatrix[j][i][S-2] += (1-q)/2
                        else :
                            scored = int(boutcomes[k])
                            ballsNew = balls - 1
                            runsNew = runs - scored
                            playerNew = player
                            if ((ballsNew%6 != 0 and scored%2 == 1) or (ballsNew%6 == 0 and scored%2 == 0)):
                                playerNew = 1 - player
                            ballsNew = (str(ballsNew)).zfill(2)
                            runsNew = (str(runsNew)).zfill(2)
                            newStateStr = ballsNew + runsNew + str(playerNew)
                            newState = mapStrToState[newStateStr]
                            transitionMatrix[j][i][newState] += (1-q)/2

    ## function to print output
    def printoutput(self,):
        print("numStates",self.noofstates)
        print("numActions", self.noofactions)
        print("end", self.noofstates-1, self.noofstates-2)
        transitionfunction = self.mdp["transitionfunc"]
        rewardfunction = self.mdp["rewardfunc"]
        for i in range(0,self.noofstates):
            for j in range(0,self.noofactions):
                sum = 0
                entered = 0
                for k in range(0,self.noofstates):
                    if(transitionfunction[i][j][k] > 0):
                        print("transtiton", i, j, k, rewardfunction[i][j][k], transitionfunction[i][j][k])
                        entered =1
                    sum += transitionfunction[i][j][k]
                if(sum != 1 and entered == 1):
                    print(i,j)
                # assert(sum ==1 and entered == 1)
        print("mdptype episodic")
        print("discount", 1.0)




if __name__ == "__main__":
    
    ## parsing args 
    parser.add_argument("--states",type=str)
    parser.add_argument("--parameters",type=str)
    parser.add_argument("--q",type=str)
    args = parser.parse_args()

    encoder(args.states, args.parameters, args.q)


#################################################################################################################################

# import argparse
# import numpy as np

# parser = argparse.ArgumentParser()
# parser.add_argument("--states")
# parser.add_argument("--parameters")
# parser.add_argument("--q")

# args = parser.parse_args()
# statesPath = args.states
# parametersPath = args.parameters
# q = float(args.q)

# parametersFile = open(parametersPath, 'r')
# parameterLines = parametersFile.readlines()

# probs = np.zeros((5, 7))

# for i in range(1, 6):
#     parameterLine = parameterLines[i].strip().split()
#     for j in range(1, 8):
#         probs[i-1][j-1] = float(parameterLine[j])

# statesFile = open(statesPath, 'r')
# stateLines = statesFile.readlines()

# stateLines = [i.strip().split()[0] for i in stateLines]
# stateLinesA = [(i + "0") for i in stateLines]
# stateLinesB = [(i + "1") for i in stateLines]
# states = stateLinesA + stateLinesB
# states += ["W", "L"]
# S = len(states)
# actions = np.array([0, 1, 2, 4, 6])
# outcomes = np.array([-1, 0, 1, 2, 3, 4, 6])
# boutcomes = np.array([-1, 0, 1])
# A = len(actions)

# mapStrToState = {}
# mapStateToStr = {}
# for i in range(len(states)):
#     mapStrToState[states[i]] = i
#     mapStateToStr[i] = states[i]

# discount = 1.0
# transitions = []

# transitionMatrix = np.zeros((A, S, S))

# for i in range(S-2):
#     balls = int(states[i][0:2])
#     runs = int(states[i][2:4])
#     player = int(states[i][4])
#     if (player == 0):
#         for j in range(len(actions)):
#             for k in range(len(outcomes)):
#                 if (probs[j][k] > 1e-6):
#                     if ((outcomes[k] == -1) or ((balls == 1) and (runs > outcomes[k]))):
#                         transitionMatrix[j][i][S-1] += probs[j][k] 
#                     elif (runs <= outcomes[k]):
#                         transitionMatrix[j][i][S-2] += probs[j][k]
#                     else :
#                         scored = int(outcomes[k])
#                         ballsNew = balls - 1
#                         runsNew = runs - scored
#                         playerNew = player
#                         if ((ballsNew%6 != 0 and scored%2 == 1) or (ballsNew%6 == 0 and scored%2 == 0)):
#                             playerNew = 1 - player
#                         ballsNew = (str(ballsNew)).zfill(2)
#                         runsNew = (str(runsNew)).zfill(2)
#                         newStateStr = ballsNew + runsNew + str(playerNew)
#                         newState = mapStrToState[newStateStr]
#                         transitionMatrix[j][i][newState] += probs[j][k]
#     else:
#         for j in range(len(actions)):
#             for k in range(len(boutcomes)):
#                 if (boutcomes[k] == -1):
#                     transitionMatrix[j][i][S-1] += q
#                 elif (((balls == 1) and (runs > boutcomes[k]))):
#                     transitionMatrix[j][i][S-1] += (1-q)/2
#                 elif (runs <= boutcomes[k]):
#                     transitionMatrix[j][i][S-2] += (1-q)/2
#                 else :
#                     scored = int(boutcomes[k])
#                     ballsNew = balls - 1
#                     runsNew = runs - scored
#                     playerNew = player
#                     if ((ballsNew%6 != 0 and scored%2 == 1) or (ballsNew%6 == 0 and scored%2 == 0)):
#                         playerNew = 1 - player
#                     ballsNew = (str(ballsNew)).zfill(2)
#                     runsNew = (str(runsNew)).zfill(2)
#                     newStateStr = ballsNew + runsNew + str(playerNew)
#                     newState = mapStrToState[newStateStr]
#                     transitionMatrix[j][i][newState] += (1-q)/2

# print("numStates", S)
# print("numActions", len(actions))
# print("end", S-1, S-2)

# for i in range(A):
#     for j in range(S):
#         for k in range(S):
#             reward = 0
#             if (k == S-2):
#                 reward = 1
#             if transitionMatrix[i][j][k] > 0:
#                 print("transition", j, i, k, reward ,transitionMatrix[i][j][k])

# print("mdptype episodic")
# print("discount", 1.0)