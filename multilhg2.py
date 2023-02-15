                                # Setup and Import Stats 
from __future__ import division 
import itertools
from itertools import groupby
import sys
import collections
import operator
import random 
from random import randint
import csv
import multiprocessing 
import pandas as pd
import numpy as np  

data = pd.read_csv('lhgdata.csv', index_col='id')
data.coordx =data.coordx.astype(int)
data.coordy =data.coordy.astype(int)

df = data
participants = len(df.index) # number of initial participants
field = 10 # length of field  
djoins = list() # id tracking for district groups 

                                # Arena Function Definitions  

# create b x b arena 
def create_arena(a, b):
    for x in range(b):
        a.append(['_'] * b)
    return a 

# print b x b arena 
def print_arena(a):
    for row in a:
        print ' '.join(row)
    print '\n'

arena = [] 
create_arena(arena, 10)

# Combat Functions 

# create dictionary matching 2 lists
def dictionary_create(a,b):
    d = collections.defaultdict(list)
    for a, b in zip(a, b):
        d[a].append(b)
    return d  

# return key of max value in dictionary 
def strongest(d): 
    return max(d.iteritems(),key=operator.itemgetter(1))[0]

# combat calculations  
def combat(a):
# find coordinates of battle   
    position = np.array(a) 
    x, y = np.where(position == 'X')
    x.tolist
    y.tolist
    battle = zip(x, y) # coordinates of battles
  
    for xcord, ycord in battle:
# list of id     
        combatants = df[np.logical_and(df['coordx'] == xcord,  
        df['coordy'] ==ycord) ].index.tolist()

# list of districts, scores, and id 
        district = list()
        score = list()
        id = list()
        for combatant in combatants:
            district.append(df.loc[combatant, 'district'])
            score.append(df.loc[combatant, 'score'])
            id.append(combatant)

# dictionary of district and team score   
        dist_score = dictionary_create(district, score)
        teamscore = dict()
        for key in dist_score:
            teamscore[key] = sum(dist_score[key]) 
    
# list of tuples of district and team score     
        teamscore_tup = list()
        for v, k in teamscore.items():
            teamscore_tup.append( (v, k))
      
                                # Calculating Total Scores and Eliminate 

# only 1 team occupy space  
        teams_remaining = len(teamscore_tup)
        if teams_remaining == 1:  
            df.loc[len(df.index)+1, 'district'] = teamscore_tup[0][0] 
            df.loc[len(df.index), 'score'] = teamscore_tup[0][1]
            df.loc[len(df.index), 'coordx'] = xcord
            df.loc[len(df.index), 'coordy'] = ycord
            for n in combatants:
                df.loc[n, 'coordx'] = 10
                df.loc[n, 'coordy'] = 10
        
            for item in zip(district, id):
                if item[1] > participants:
                    gen = (tuple for tuple in djoins if tuple[0] == item[1]) 
                    for x in gen:
                        djoins.append((len(df.index), x[1]))
                else: 
                    djoins.append((len(df.index), item[1]))
        else: 
    
# >1 teams occupy space
            rem_teamscore = teamscore.copy()
            district_id = zip(district, id)
            while teams_remaining > 1: 
                strongest_team = strongest(rem_teamscore) # district of strongest team
                strong_teamodds = rem_teamscore[strongest_team] ** 4 / (
                (sum(rem_teamscore.values()) - rem_teamscore[strongest_team]) ** 4
                + rem_teamscore[strongest_team] ** 4) # strong_teamodds of strongest team
                while True:
                    rand = random.random()
                    if rand != strong_teamodds : break
        
# strongest team wins
                if strong_teamodds > rand: 
                    if district.count(strongest_team) == 1: # winning team = 1 combatant
                        for item in district_id: # losers elimiated
                            if item[0] == strongest_team : continue
                            df.loc[item[1], 'coordx'] = 10
                            df.loc[item[1], 'coordy'] = 10 
                    elif district.count(strongest_team) > 1: # winning team >1 combatant
                        df.loc[len(df.index)+1, 'district'] = strongest_team
                        df.loc[len(df.index), 'score'] = rem_teamscore[strongest_team]
                        df.loc[len(df.index), 'coordx'] = xcord
                        df.loc[len(df.index), 'coordy'] = ycord
                        for n in combatants:
                            df.loc[n, 'coordx'] = 10
                            df.loc[n, 'coordy'] = 10 
                            
                        same_team = (x for x in district_id if x[0] == strongest_team)
                        for item in same_team:
                            if item[1] > participants:
                                gen = (tuple for tuple in djoins if tuple[0] == item[1]) 
                                for x in gen:
                                    djoins.append((len(df.index), x[1]))
                            else: 
                                djoins.append((len(df.index), item[1]))
                        
                    teams_remaining = 1
                    continue 

# strongest team loses
                else:
                    for item in district_id: # losers elimiated
                        if item[0] != strongest_team : continue
                        df.loc[item[1], 'coordx'] = 10  
                        df.loc[item[1], 'coordy'] = 10
                    del rem_teamscore[strongest_team]
                    teams_remaining -= 1
                    district_id = [item for item in district_id if item[0] != strongest_team]
                    rem_teamscore.pop(strongest_team, None)
                    if teams_remaining == 1:
                        if len(district_id) > 1:
                            for item in district_id:
                                if item[1] > participants:
                                    gen = (tuple for tuple in djoins if tuple[0] == item[1]) 
                                    for x in gen:
                                        djoins.append((len(df.index), x[1]))
                                else: 
                                    djoins.append((len(df.index), item[1]))
                        break 

                                # Perform Combat and Track id 

def aftermath():
    for id in df.index:
        if df.loc[id, 'coordx'] == 10 : continue 
        if arena[int(df.loc[id, 'coordx'])][int(df.loc[id, 'coordy'])] != '_':
            arena[int(df.loc[id, 'coordx'])][int(df.loc[id, 'coordy'])] = 'X'
        else:
            arena[int(df.loc[id, 'coordx'])][int(df.loc[id, 'coordy'])] = str(id)

def surviving_teams():
    counter = 0
    for id in df.index:
        if df.loc[id, 'coordx'] == 10 : continue
        counter +=1 
    return counter 

def survivor():
    counter = 0
    for id in df.index:
        if df.loc[id, 'coordx'] == 10 : continue
        if id <= participants:
            counter +=1 
        else: 
            counter = counter + len([item for item in djoins if item[0] == id])
    return counter     
        
                                # Movement, Position, Arena Shift Function Definitions 

def move(field, arena):
    for id in df.index:
        if int(df.loc[id, 'coordx']) == 10 : continue 
        if int(df.loc[id, 'coordx']) == field-1:
            df.loc[id, 'coordx'] = int(df.loc[id, 'coordx']) + random.randint(-1, 0)
        elif int(df.loc[id, 'coordx']) == 0:
            df.loc[id, 'coordx'] = int(df.loc[id, 'coordx']) + random.randint(0, 1)
        else: 
            df.loc[id, 'coordx'] = int(df.loc[id, 'coordx']) + random.randint(-1, 1)
        if int(df.loc[id, 'coordy']) == field-1:
            df.loc[id, 'coordy'] = int(df.loc[id, 'coordy']) + random.randint(-1, 0)
        elif int(df.loc[id, 'coordy']) == 0:
            df.loc[id, 'coordy'] = int(df.loc[id, 'coordy']) + random.randint(0, 1)
        else:
            df.loc[id, 'coordy'] = int(df.loc[id, 'coordy']) + random.randint(-1, 1)
        
        if arena[int(df.loc[id, 'coordx'])][int(df.loc[id, 'coordy'])] != '_':
            arena[int(df.loc[id, 'coordx'])][int(df.loc[id, 'coordy'])] = 'X'
        else:
            arena[int(df.loc[id, 'coordx'])][int(df.loc[id, 'coordy'])] = str(id)

def field_shift(field, arena):    
    for id in df.index:
        if df.loc[id, 'coordx'] == 10 : continue 
        if df.loc[id, 'coordx'] >= field:
            df.loc[id, 'coordx'] = field-1
        if df.loc[id, 'coordy'] >= field:
            df.loc[id, 'coordy'] = field - 1
        if arena[int(df.loc[id, 'coordx'])][int(df.loc[id, 'coordy'])] != '_':
            arena[int(df.loc[id, 'coordx'])][int(df.loc[id, 'coordy'])] = 'X'
        else:
            arena[int(df.loc[id, 'coordx'])][int(df.loc[id, 'coordy'])] = str(id)

results24 = multiprocessing.Queue()
results12 = multiprocessing.Queue()
results6 = multiprocessing.Queue()
results3 = multiprocessing.Queue()
results1 = multiprocessing.Queue() 

            
def hunger_games():
    execfile('lhg_singleround.py')
    

if __name__ == '__main__':
    processes = [multiprocessing.Process(target=hunger_games) for i in range(25)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    
    top24 = [results24.get() for p in processes]
    top12 = [results12.get() for p in processes]
    top6 = [results6.get() for p in processes]
    top3 = [results3.get() for p in processes]
    top1 = [results1.get() for p in processes]


        