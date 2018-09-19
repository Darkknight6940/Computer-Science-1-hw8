import json
from math import sqrt
from Person import *
from Universe import *
def openfile(l):#a function to import the file and make it into Universe,return a list with universes
    data=json.loads(open(l).read())
    l2=[]
    for b in data:
        x=b["universe_name"]
        y=b['rewards']
        z=b['portals']
        l2.append(Universe(x,y,z))
    return l2
dictdata=dict()
def openfile2(l):#a function to import the file and make it into person,return a dictionary
    data=json.loads(open(l).read())
    for data in data:
        x=data["individuals"]
        for n in x:
            dictdata[n[0]]=[n[1],n[2],n[3],n[4],n[5],data["universe_name"]]
    return dictdata 
def openfile3(l):
    printoutform=[]
    data=json.loads(open(l).read())
    for data in data:
        x=data["individuals"]
        for n in x:
            printoutform.append([n[0],n[1],n[2],n[3],n[4],n[5],data["universe_name"]])
    return printoutform     
file=str(input('Input file => '))
#file='file4.txt'#here,it's the filllllllllllllllllllllllllllllllllllllllllllllllllllle.
print(file)
print("All universes")
print("-"*40)
alluniverses=openfile(file)#Print out all universes and individuals
for a in alluniverses:
    print("Universe: {} ({} rewards and {} portals)".format(a,len(a.rewards),len(a.portals)))
    print("Rewards:")
    if a.rewards==[]:
        print("None")
    else:
        for n in a.rewards:
            print("at ({},{}) for {} points: {}".format(n[0],n[1],n[2],n[3]))
    print("Portals:")
    if a.portals==[]:
        print("None")
    else:
        for n in a.portals:
            print("{}:({},{}) -> {}:({},{})".format(a.name,n[0],n[1],n[2],n[3],n[4]))
    print()
print("All individuals")
print("-"*40)
b=openfile2(file)
printoutform=openfile3(file)
names=[]
individuals=dict()
for line in b:
    c=Person(line,b[line][0],b[line][1],b[line][2],b[line][3],b[line][4],b[line][5],b[line][5])
    individuals[line]=c
for line in printoutform:
    print("{} of {} in universe {}".format(line[0],line[-1],line[-1]))
    print("    at ({:.1f},{:.1f}) speed ({:.1f},{:.1f}) with {} rewards and {} points".format(line[2],line[3],line[4],line[5],0,0))
    names.append(line[0])
print()
print("Start simulation")
print("-"*40)
#print out the stimulation
stop=[]
k=int(0)
num=0
crash=set()
while k<100:
    num+=1
    for n in individuals:#let all individuals move 1 step
        if n in stop:
            continue
        else:
            people=individuals[n]
            if abs(people.dx)<10 or abs(people.dy)<10:
                stop.append(n)
                print(n+' stopped at simulation step '+str(num-1)+' at location ({:.1f}'.format(people.x)+',{:.1f}'.format(people.y)+')')
                print()
            elif people.x<=0 or people.x>=1000 or people.y<=0 or people.y>=1000:#whether a individual stops
                stop.append(n)
                print(n+' stopped at simulation step '+str(num-1)+' at location ({:.1f}'.format(people.x)+',{:.1f}'.format(people.y)+')')
                print()                 
            else:
                people.x+=people.dx
                people.y+=people.dy
                if people.x<=0 or people.x>=1000 or people.y<=0 or people.y>=1000:#whether a individual stops
                    stop.append(n)
                    print(n+' stopped at simulation step '+str(num)+' at location ({:.1f}'.format(people.x)+',{:.1f}'.format(people.y)+')')
                    print()    
    for n in individuals:#ignore the ones stopped.
        if n in stop:
            continue
        else:        
            people=individuals[n]#find the right universes that the individuals are currently in
            for a in alluniverses:
                if people.current==a.name:
                    neededuniverse=a
            for x in neededuniverse.rewards:#whether individuals get a reward
                origindx=people.dx
                origindy=people.dy
                if sqrt((people.x-x[0])**2+(people.y-x[1])**2)<=people.radius and people.current==neededuniverse.name:
                    people.rewards.append([x,people.current])
                    people.dx=origindx-(len(people.rewards)%2)* (len(people.rewards)/6)*origindx
                    people.dy=origindy-((len(people.rewards)+1)%2)* (len(people.rewards)/6)*origindy
                    people.points+=x[-2]
                    print (n+' picked up "'+x[-1]+'" at simulation step '+ str(num))
                    print("{} of {} in universe {}".format(n,people.home,people.current))
                    print("    at ({:.1f},{:.1f}) speed ({:.1f},{:.1f}) with {} rewards and {} points".format\
                          (people.x,people.y,people.dx,people.dy,len(people.rewards),people.points))
                    print()
                    (neededuniverse.rewards).remove(x)
                    if abs(people.dx)<10 or abs(people.dy)<10:
                        stop.append(n)
                        print(n+' stopped at simulation step '+str(num)+' at location ({:.1f}'.format(people.x)+',{:.1f}'.format(people.y)+')')
                        print()                       
    
    for n in individuals:
        people=individuals[n]#whether individuals crash
        for n2 in individuals:
            people2=individuals[n2]
            if (people.x-people2.x)**2+(people.y-people2.y)**2<=\
               (people.radius+people2.radius)**2 and people!=people2 \
               and people.name not in crash and\
               people.current==people2.current:
                print("{} and {} crashed at simulation step {} in universe {}".format(people.name,people2.name,num,people.current))
                crash.add(people2.name)
                if len(people.rewards)>0:
                    people.dx=-(people.dx + (len(people.rewards)%2)* ((len(people.rewards)-1)/6)*people.dx)
                    people.dy = -(people.dy + ((len(people.rewards)+1)%2)* (len(people.rewards)/6)*people.dy)
                    people.points-=people.rewards[0][0][-2]#drop the first prize
                    
                    for a in alluniverses:
                        if people.current==a.name:
                            neededuniverse=a                    
                    neededuniverse.rewards.append(people.rewards[0][0])
                    print(people.name+' dropped "'+people.rewards[0][0][-1]+\
                          '", reward returned to '+neededuniverse.name+\
                          ' at ('+str(people.rewards[0][0][0])+','+\
                          str(people.rewards[0][0][1])+')')
                    del people.rewards[0]
                     
                if len(people2.rewards)>0:
                    people2.dx=-(people2.dx + (len(people2.rewards)%2)* ((len(people2.rewards)-1)/6)*people2.dx)
                    people2.dy = -(people2.dy + ((len(people2.rewards)+1)%2)* (len(people2.rewards)/6)*people2.dy)
                    people2.points-=people2.rewards[0][0][-2]
                    
                    for a in alluniverses:
                        if people.current==a.name:
                            neededuniverse=a                    
                    neededuniverse.rewards.append(people2.rewards[0][0])
                    print(people2.name+' dropped "'+people2.rewards[0][0][-1]+\
                          '", reward returned to '+neededuniverse.name+\
                          ' at ('+str(people2.rewards[0][0][0])+','+\
                          str(people2.rewards[0][0][1])+')')
                    del people2.rewards[0] 
                print("{} of {} in universe {}".format(people.name,people.home,people.current))#print out the current condition
                print("    at ({:.1f},{:.1f}) speed ({:.1f},{:.1f}) with {} rewards and {} points".format\
                      (people.x,people.y,people.dx,people.dy,len(people.rewards),people.points))
                print("{} of {} in universe {}".format(people2.name,people.home,people.current))
                print("    at ({:.1f},{:.1f}) speed ({:.1f},{:.1f}) with {} rewards and {} points".format\
                      (people2.x,people2.y,people2.dx,people2.dy,len(people2.rewards),people2.points))
                print()
            if people in crash:
                crash.discard(people)            
    for n in individuals:  #whether individuals get into s portal
        people=individuals[n]
        for universe in alluniverses:
            if universe.name == people.current:
                for portal in universe.portals:
                    if sqrt((people.x-portal[0])**2+\
                            (people.y-portal[1])**2)<= people.radius:
                        print(people.name+' passed through a portal at simulation step '+str(num))
                        people.current = portal[2]
                        people.x = portal[3]
                        people.y = portal[4]
                        print("{} of {} in universe {}".format(people.name,people.home,people.current))
                        print("    at ({:.1f},{:.1f}) speed ({:.1f},{:.1f}) with {} rewards and {} points".format\
                      (people.x,people.y,people.dx,people.dy,len(people.rewards),people.points))
                        print()    
    k+=1
    if len(stop)==len(individuals):
        break
print()
print("-"*40)#report the result
print("Simulation stopped at step {}".format(num))
print("{} individuals still moving".format(len(individuals)-len(stop)))
print("Winners:")
maxrewards = 0
winner = ''
for n in individuals:#Find the winner
    people=individuals[n]
    if people.points>maxrewards:
            maxrewards = people.points
            winner = people.name    
if winner=='':#if no winner
    for n in individuals:
        people=individuals[n]
        for x in names:
            if people.name==x:
                print("{} of {} in universe {}".format(n,people.home,people.current))
                print("    at ({:.1f},{:.1f}) speed ({:.1f},{:.1f}) with {} rewards and {} points".format\
                      (people.x,people.y,people.dx,people.dy,len(people.rewards),people.points)) 
                print("Rewards:")
                for x in people.rewards:
                    print(x[0][3])
                print()
                names.remove(x)
            
else:
    print("{} of {} in universe {}".format(winner,individuals[winner].current,individuals[winner].home))#PPrint out the winners
    print("    at ({:.1f},{:.1f}) speed ({:.1f},{:.1f}) with {} rewards and {} points".\
          format(individuals[winner].x,individuals[winner].y,individuals[winner].dx,individuals[winner].dy,len(individuals[winner].rewards),individuals[winner].points)) 
    print("Rewards:")
    for x in individuals[winner].rewards:
        print('    '+x[0][3])
    print()
            

