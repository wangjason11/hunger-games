                                # Setup and Import Stats 
from __future__ import division 
import itertools
from itertools import groupby
import sys
import collections
import operator
import numpy as np   
import random 
from random import randint
import csv 

import pandas as pd
data = pd.read_csv('lhgdata.csv', index_col='id')
data.coordx =data.coordx.astype(int)
data.coordy =data.coordy.astype(int)

df = data

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

                                # Creating Field, Arena, and 1st Iteration  

participants = len(df.index) # number of initial participants
field = 10 # length of field                               
arena = [] 
create_arena(arena, 10)

for id in df.index:
    df.loc[id, 'coordx'] = randint(0, field - 1) # Random x coordinate
    df.loc[id, 'coordy'] = randint(0, field - 1) # Random y coordinate
    if arena[df.loc[id, 'coordx']][df.loc[id, 'coordy']] != '_':
        arena[df.loc[id, 'coordx']][df.loc[id, 'coordy']] = 'X'
    else:
        arena[df.loc[id, 'coordx']][df.loc[id, 'coordy']] = str(id)

djoins = list() # create list that tracks id  

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
    df.to_csv('r1_results.csv', sep = '\t') 
                                
                                # Perform Combat and Track id 

combat(arena)
arena = []
create_arena(arena, 10)

def aftermath():
    for id in df.index:
        if df.loc[id, 'coordx'] == 10 : continue 
        if arena[int(df.loc[id, 'coordx'])][int(df.loc[id, 'coordy'])] != '_':
            arena[int(df.loc[id, 'coordx'])][int(df.loc[id, 'coordy'])] = 'X'
        else:
            arena[int(df.loc[id, 'coordx'])][int(df.loc[id, 'coordy'])] = str(id)

aftermath()

                                # End Initial Run 

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

    
t24 = []
t12 = []
t6 = []
t3 = []
t1 = [] 

while survivor() >= 24:
    arena = [] 
    create_arena(arena, 10)
    move(field, arena)
    combat(arena)
    arena = []
    create_arena(arena, 10)
    aftermath()
    if survivor() <= 24:
        for id in df.index:
            if df.loc[id, 'coordx'] == 10 : continue
            if id <= participants:
                t24.append(df.loc[id, 'nickname'])
            else:              
                for item in djoins:
                    if item[0] != id: continue
                    t24.append(df.loc[item[1], 'nickname'])
        break

arena = []
create_arena(arena, 10)
move(field, arena)
field = field - 2
arena = []
create_arena(arena, 8)
field_shift(field, arena)
combat(arena)
arena = []
create_arena(arena, 8)
aftermath()    
         
while survivor() >= 12:
    arena = [] 
    create_arena(arena, 8)
    move(field, arena)
    combat(arena)
    arena = []
    create_arena(arena, 8)
    aftermath()  
    if survivor() <= 12:
        for id in df.index:
            if df.loc[id, 'coordx'] == 10 : continue
            if id <= participants:
                t12.append(df.loc[id, 'nickname'])
            else:
                for item in djoins:
                    if item[0] != id: continue 
                    t12.append(df.loc[item[1], 'nickname'])
        break 

arena = []
create_arena(arena, 8)
move(field, arena)
field = field - 2
arena = []
create_arena(arena, 6)
field_shift(field, arena)
combat(arena)
arena = []
create_arena(arena, 6)
aftermath() 

while survivor() >= 6:
    if surviving_teams() < 2: break 
    arena = [] 
    create_arena(arena, 6)
    move(field, arena)
    combat(arena)
    arena = []
    create_arena(arena, 6)
    aftermath()
    if survivor() <= 6:
        for id in df.index:
            if df.loc[id, 'coordx'] == 10 : continue
            if id <= participants:
                t6.append(df.loc[id, 'nickname'])
            else:
                for item in djoins:
                    if item[0] != id: continue 
                    t6.append(df.loc[item[1], 'nickname'])
        break 

arena = []
create_arena(arena, 6)
move(field, arena)
field = field - 2
arena = []
create_arena(arena, 4)
field_shift(field, arena)
combat(arena)
arena = []
create_arena(arena, 4)
aftermath()        

while survivor() >= 3:
    if surviving_teams() < 2: break 
    arena = [] 
    create_arena(arena, 4)
    move(field, arena)
    combat(arena)
    arena = []
    create_arena(arena, 4)
    aftermath()
    if survivor() <= 3:
        for id in df.index:
            if df.loc[id, 'coordx'] == 10 : continue
            if id <= participants:
                t3.append(df.loc[id, 'nickname'])
            else:
                for item in djoins:
                    if item[0] != id: continue 
                    t3.append(df.loc[item[1], 'nickname'])
        break 

arena = []
create_arena(arena, 4)
move(field, arena)
field = field - 1
arena = []
create_arena(arena, 3)
field_shift(field, arena)
combat(arena)
arena = []
create_arena(arena, 3)
aftermath()         

while survivor() >= 1:
    if surviving_teams() < 2 : break 
    arena = [] 
    create_arena(arena, 3)
    move(field, arena)
    combat(arena)
    arena = []
    create_arena(arena, 3)
    aftermath()

if survivor() == 1:
    for id in df.index:
        if df.loc[id, 'coordx'] == 10 : continue
        t1.append(df.loc[id, 'nickname'])
     

if surviving_teams() == 1 and survivor() > 1:
    last_standing = [] 
    for a, b in djoins:
        if df.loc[a, 'coordx'] == 10 : continue
        last_standing.append(b)
    last_scores = []
    for x in last_standing:
        last_scores.append(df.loc[x, 'score'])
    last_idscores = zip(last_standing, last_scores)
    counter = len(last_standing)
    while counter > 1:
        strongest_score = max([b for a, b in last_idscores])
        strongest_one = random.choice([a for a, b in last_idscores if b == strongest_score]) 
        strongest_odds = strongest_score ** 4 / ((sum([b for a, b in last_idscores]) 
        - strongest_score) ** 4 + strongest_score ** 4)
        while True:
            rand = random.random()
            if rand != strongest_odds: break
        
        if strongest_odds > rand: 
            t1.append(df.loc[strongest_one, 'nickname'])
            counter = 1 
            continue 
        else:
            last_idscores = [item for item in last_idscores if item[0] != strongest_one]
            counter -= 1
            if counter == 6:
                for a, b in last_idscores: 
                    t6.append(df.loc[a, 'nickname'])
            if counter == 3:
                for a, b in last_idscores: 
                    t3.append(df.loc[a, 'nickname'])
            if counter == 1:
                t1.append(df.loc[last_idscores[0][0], 'nickname'])

print t1                 