import goGameClass as go
from utils import *
'''
-----------------------------------------------
'''

#Helper for vitalpoint
def Most_Common(lst):
    data = Counter(lst)
    return data.most_common(1)[0][0]
    
#needs to know which players turn it is
#check for spots that have potential to be eyes
def vitalpoint(state, player):
    #eyes.append({'Group': group, 'EyeType': eyeType, 'FalseSpots': falseSpotCount})
    vitals = {2:[], 3:[]};   weight2 = 1;    weight3 = 1;     
    notplayer = if_(player == 'Att', 'Def', 'Att')
    # if not('Group' in state.eyes):
    # state.eyes['Group'] = []]
    alleyes = []

    if state.eyes:
        for i in state.eyes:
            alleyes += i['Group']
    
    for spot in state.moves:
        #for each spot, we want to check if the surrounding are of the same color
        if not(spot in alleyes):
            diagcount = 0;  piececolor = 0;   tempspots = []

            up = (spot[0] + 1, spot[1]);   down = (spot[0] -1 , spot[1])
            left = (spot[0], spot[1] - 1); right = (spot[0], spot[1] + 1)
            
            topleft = (spot[0]-1, spot[1]-1);    topright = (spot[0]-1, spot[1]+1)
            bottomleft = (spot[0]+1, spot[1]-1); bottomright = (spot[0]+1, spot[1]+1)
            
            checkspots = [up, down, left, right]
            diagspots = [topleft, topright, bottomleft, bottomright]
            
            falseref = go.countDiagNeighborSpots(spot)
            for x in copy.copy(checkspots):
                if (x in alleyes): #this shouldnt actually be possible.
                    checkspots.remove(x) #altho it is an eye, it would be our eye if pass
                elif ((x[0] < 0) or (x[1] < 0)):
                    checkspots.remove(x)
                elif (x in state.board[player]): #in player color
                        checkspots.remove(x)     #by the end if all is removed, then we good
                elif (x in state.board['Avail']):#in Avail
                    tempspots.append(x)          #save all avails for if all tests pass
                    checkspots.remove(x)
            for x in diagspots:                  #diagonal checks
                if (x in state.board[notplayer]):#other player, count these
                    diagcount += 1
                    
            if (len(checkspots) == 0) and (diagcount < falseref['False']):
                if (len(tempspots) in vitals):
                    vitals[len(tempspots)] = vitals[len(tempspots)] + tempspots
                else: 
                    vitals[len(tempspots)]= tempspots
                
    #weighted
    totalvitals = []
    vitalsall = vitals[2] + vitals[3]
    for entry in set(vitalsall):
        totalvitals.append((entry, (vitals[2].count(entry) * weight2) + 
                                    (vitals[3].count(entry) * weight3)))
    totalvitals.sort(key = lambda x: -x[1])
    #print vitalsall
    #return totalvitals
    #or to return a sorted list of recommendations with no score: 
    listvitals = map(lambda x: x[0], totalvitals)
    listvitals.extend(list(set(state.moves) - set(listvitals)))
    return listvitals
'''
----------------------------------------------------------------
'''
def determineStableState(state):
    eyes = state.eyes
    player = state.player
    for eye in eyes:
        if (eye['EyeType'] == 'Real') & (determineEyeState(eye['Group'], player)):
            return True
    return False

def determineEyeState(eye, player):
    #assume solid eyes and Att plays next
    if len(eye) == 3:#straight or bent 3
        #whoever plays next wins
        if player == 'Def':
            return True
        else:
            return False
    elif len(eye) == 4:
        #pyramid 4 (one of the spot is neighbor to all other spots)
        for spot in eye:
            if len(set(go.generateNeighbors([spot])).intersection(set(eye))) == 3:
                # whoever plays next wins
                if player == 'Def':
                    return True
                else:
                    return False
        #square 4
        if (len(set([x[0] for x in eye]))==2) & (len(set([x[1] for x in eye]))==2):
            # whoever plays next wins
            if player == 'Def':
                return True
            else:
                return False
        #all other 4's are survival states
        return True
    elif len(eye) == 5:
        #cross 5 (one of the spot is neighbor to all other spots)
        for spot in eye:
            if len(set(go.generateNeighbors([spot])).intersection(set(eye))) == 4:
                # whoever plays next wins
                if player == 'Def':
                    return True
                else:
                    return False
            #bulky 5 (4 of the 5 spots forms a square)
            else:
                groupOfFour = [x for x in eye if x != spot]
                if (len(set([x[0] for x in groupOfFour])) == 2) & (len(set([x[1] for x in groupOfFour])) == 2):
                    # whoever plays next wins
                    if player == 'Def':
                        return True
                    else:
                        return False
        #All other states are survival states
        return True

print(determineEyeState([(3,0), (3,1), (3,2)], 'Att'))
print(determineEyeState([(3,0), (3,1), (4,1)], 'Att'))
print(determineEyeState([(3,0), (3,1), (3,2), (4,1)], 'Att'))
print(determineEyeState([(3,0), (3,1), (4,0), (4,1)], 'Att'))
print(determineEyeState([(3,0), (3,1), (4,0), (4,1), (4,2)], 'Att'))
print(determineEyeState([(3,3), (3,1), (3,2), (4,2), (2,2)], 'Att'))

print(determineEyeState([(3,0), (3,1), (3,2)], 'Def'))
print(determineEyeState([(3,0), (3,1), (4,1)], 'Def'))
print(determineEyeState([(3,0), (3,1), (3,2), (4,1)], 'Def'))
print(determineEyeState([(3,0), (3,1), (4,0), (4,1)], 'Def'))
print(determineEyeState([(3,0), (3,1), (4,0), (4,1), (4,2)], 'Def'))
print(determineEyeState([(3,3), (3,1), (3,2), (4,2), (2,2)], 'Def'))

