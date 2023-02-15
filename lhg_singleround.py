                                # Creating Field, Arena, and 1st Iteration  
                            
for id in df.index:
    df.loc[id, 'coordx'] = randint(0, field - 1) # Random x coordinate
    df.loc[id, 'coordy'] = randint(0, field - 1) # Random y coordinate
    if arena[df.loc[id, 'coordx']][df.loc[id, 'coordy']] != '_':
        arena[df.loc[id, 'coordx']][df.loc[id, 'coordy']] = 'X'
    else:
        arena[df.loc[id, 'coordx']][df.loc[id, 'coordy']] = str(id)
                                                               
combat(arena)
arena = []
create_arena(arena, 10)
aftermath()

t24 = []
t12 = []
t6 = []
t3 = []
t1 = []

                                # End Initial Run     
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

results24.put(t24)
results12.put(t12)
results6.put(t6)
results3.put(t3)
results1.put(t1)                 