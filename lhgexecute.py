import pandas as pd
import csv 

count = 0
while count < 1000:
    execfile('lhg_vnonprint.py')
    
    with open('top_24.csv', 'a') as f:
        top24 = csv.writer(f, dialect = 'excel')
        top24.writerow(t24)
    
    with open('top_12.csv', 'a') as f:
        top12 = csv.writer(f, dialect = 'excel')
        top12.writerow(t12)
    
    with open('top_6.csv', 'a') as f:
        top6 = csv.writer(f, dialect = 'excel')
        top6.writerow(t6)
        
    with open('top_3.csv', 'a') as f:
        top3 = csv.writer(f, dialect = 'excel')
        top3.writerow(t3)
        
    with open('winners.csv', 'a') as f:
        top1_winner = csv.writer(f, dialect = 'excel')
        top1_winner.writerow(t1)
        
    count += 1 



