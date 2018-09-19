import json
def openfile(l):#import data
    a=open(l, 'r')
    b=json.loads(open(l).read())[0]
    x=b["universe_name"]
    y=b['rewards']
    z=b['portals']
    return x,y,z

class Universe(object):
    def __init__(self,name=str(),rewards=(),portals=()):
        self.name=name
        self.rewards=rewards
        self.portals=portals
        
    def __str__(self):
        return self.name
    def countrewards(self):
        return len(self.rewards)
    def countportals(self):
        return len(self.portals)
    
if __name__ == "__main__":#Test
    x,y,z=openfile('file1.txt')
    print(Universe(x,y,z),Universe(x,y,z).countrewards(),Universe(x,y,z).countportals())


