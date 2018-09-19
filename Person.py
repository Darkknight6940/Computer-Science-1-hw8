import json
def openfile2(l):
    data=json.loads(open(l).read())[0]
    x=data["individuals"]
    dictdata=dict()
    for n in x:
        dictdata[n[0]]=[n[1],n[2],n[3],n[4],n[5],data["universe_name"]]
    return dictdata   

class Person(object):
    def __init__(self,name=str(),radius=0,x=0,y=0,dx=0,dy=0,current='',home='',rewards=[],points=0):
        self.name=name
        self.home=home
        self.radius=radius
        self.x=x
        self.y=y
        self.dx=dx
        self.dy=dy
        self.current=current
        self.rewards=rewards.copy()
        self.points=points
    
    def __str__(self):#print out its name
        return self.name
    
if __name__ == "__main__":#for test
    y=openfile2('file1.txt')
    for line in y:
        print(Person(line,y[line][0],y[line][1],y[line][2],\
               y[line][3],y[line][4]))
               
        