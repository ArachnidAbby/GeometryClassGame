import pygame
import json
pygame.init()


class GameObject:
    def __init__(self, color,x,y,w,h, image = None, gridsize = 20, show = True):
        self.w = w*gridsize
        self.h = h*gridsize
        self.x = x*gridsize
        self.y = y*gridsize
        self.color = color
        self.rot =0
        self.shown = show
        self.refl = [False,False]
        self.image = image
        self.gridsize = gridsize
        self.previouslyPressed = False
        if image!= None:
            self.image = pygame.image.load(image)

    def draw(self,display):
        if not self.shown: return 0
        if self.image == None:
            pygame.draw.rect(display, self.color,[self.x,self.y,self.w,self.h])
        else:
            display.blit(pygame.transform.flip(pygame.transform.rotate(self.image,self.rot),self.refl[0],self.refl[1]), (self.x,self.y))
        
    def isClicked(self):
        mouseP = pygame.mouse.get_pos()
        mouseC = pygame.mouse.get_pressed()
        #print(mouseC)
        if mouseC[0] == 1 and self.previoslyPressed==False:
            #print(mouseP)
            if mouseP[0]>=self.x and mouseP[0] <= (self.x+self.w):
                #print(self.w)
                if mouseP[1]>=self.y and mouseP[1] <= (self.y+self.h):
                    self.previoslyPressed = True
                    return True
                else:
                    return False
            else:
                return False
        if mouseC[0] == 0:
            self.previoslyPressed = False   
            return False

    def setPos(self, x,y):
        self.x = x*self.gridsize
        self.y = y*self.gridsize

    def setX(self,x):
        self.x = x*self.gridsize

    def setY(self,y):
        self.x = y*self.gridsize

    def changePos(self, x,y):
        self.x += x*self.gridsize
        self.y += y*self.gridsize

    def IsCol(self, x,y,w,h):
        if (x+w)>=self.x and  x<= (self.x+self.w):
            if (y+h)>=self.y+1 and y <= (self.y+self.h):
                return True
            else:
                return False
        else:
            return False

    def rotate(self,angle):
        self.rot +=angle
        if self.rot == 360 or self.rot==-360: self.rot = 0
    
    def setVisibility(self, show):
        self.shown = show

    def reflect(self, x, y):
        if x: self.refl[0] = not self.refl[0]
        if y: self.refl[1] = not self.refl[1]


class jsonLevel:
    def __init__(self):
        content = ""
        with open("level.json",'r') as f:
            content = f.read()
        
        self.levelDict = json.loads(content)
        self.tiles = []
        self.spikes = []
        self.goal = None
        self.player = None

        self.MakeTileList()
        self.MakeGoal()
        self.MakePlayer()
    
    def MakeTileList(self):
        for x in self.levelDict["tiles"]:
            colour = [x["color"]['r'],x["color"]['g'],x["color"]['b']]
            current = GameObject(colour,x["x"]+5,x["y"],x["w"],x["h"])
            current.rotate(x["rot"])
            if x["type"] == "normal":
                self.tiles.append(current)
            if x["type"] == "spike":
                self.spikes.append(current)
    
    def MakeGoal(self):
        goal = self.levelDict["goal"]
        self.goal = GameObject((0,0,0),goal["x"]+5,goal["y"],goal["w"],goal["h"], image = "images/goal.png")
        self.goal.rotate(goal["rot"])
        self.goal.reflect(goal["xrefl"],goal["yrefl"])
    
    def MakePlayer(self):
        player = self.levelDict["player"]
        self.player = GameObject((0,0,0),player["x"]+5,player["y"],player["w"],player["h"], image = "images/player.png")
        self.player.rotate(player["rot"])
        self.player.reflect(player["xrefl"],player["yrefl"])
