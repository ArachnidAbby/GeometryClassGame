import pygame,math
from Tools import *
pygame.init()


#my game

class game:
    def __init__(self):
        self.running = True
        self.start()
        self.SWidth = 600
        self.SHeight = 600
        self.display = pygame.display.set_mode((self.SWidth,self.SHeight))
        self.clock = pygame.time.Clock()
        self.display.fill((255,255,255))
        while self.running:
            self.clock.tick(60)
            self.events()
            self.display.fill((255,255,255))
            for x in range(int(self.SWidth/20)):
                pygame.draw.line(self.display, (200,200,255), [x*20,0], [x*20,self.SHeight],3)
            for y in range(int(self.SHeight/20)):
                pygame.draw.line(self.display, (200,200,255), [0,y*20], [self.SWidth,y*20],3)
            self.update()
            self.render()
            pygame.display.update()
        pygame.quit()
        quit()

    def start(self):
        Level = jsonLevel()
        self.map = Level.tiles
        print(self.map)
        self.player = Level.player
        self.goalImg = Level.goal
        self.spikes = Level.spikes
        self.translationButton = GameObject((0,0,0),1.25,1.5,2.5,2.5, image = "images/translation.png")
        self.rotationButton = GameObject((0,0,0),1.25,5.5,2.5,2.5, image = "images/rotation.png")
        self.reflectionButton = GameObject((0,0,0),1.25,9.75,2.5,2.5, image = "images/reflection.png")
        self.win =  GameObject((0,0,0),0,0,2.5,2.5, image = "images/WinScreen.png",show = False)
        self.rotButtons = [
            [GameObject((0,0,0),0.75,5.5,0.4,2.5),45],
            [GameObject((0,0,0),0.25,5.5,0.4,2.5),90],
            [GameObject((0,0,0),3.95,5.5,0.4,2.5),-45],
            [GameObject((0,0,0),4.45,5.5,0.4,2.5),-90]
        ]
        self.reflectionButtons = [
            [GameObject((0,0,0),0.75,9.75,0.4,2.5),[True, False]],
            [GameObject((0,0,0),1.25,12.5,2.5,0.4),[False, True]]
        ]
        self.translating = False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):

        if pygame.mouse.get_pressed()[0]==1 and self.translating and pygame.mouse.get_pos()[0]>100:
            mouseP = pygame.mouse.get_pos()
            xc = mouseP[0]-(self.player.x)
            yc = mouseP[1]-(self.player.y)
            if xc!=0: 
                yc = yc/(xc*(abs(xc)/xc))
                xc=1*(abs(xc)/xc)
            if xc==0: yc=1*(abs(yc)/yc)
            move = True
            x,y =self.player.x, self.player.y
            while mouseP[1]-y!=0 and mouseP[0]-x!=0:
                x+=xc
                y+=yc
                pygame.draw.rect(self.display,(255,0,0),[int(x),int(y),3,3])
                for tile in self.map:
                    if tile.IsCol(x,y,self.player.w-2,self.player.h-2):
                        move = False
                        break
                for tile in self.spikes:
                    if tile.IsCol(x,y, self.player.w, self.player.h):
                        self.running = False
                        break
            self.translating = False
            if move: self.player.setPos(int(mouseP[0]/20),int(mouseP[1]/20))

        if self.translationButton.isClicked():
            self.translating = not self.translating

        for x in self.rotButtons:
            if x[0].isClicked():
                self.player.rotate(x[1])
        
        for x in self.reflectionButtons:
            if x[0].isClicked():
                self.player.reflect(x[1][0],x[1][1])
                #print(x[1][1])
        
        # if self.player.x < 100:
        #     self.player.setX(100)
        # if self.player.x > self.SWidth:
        #     self.player.setX(self.SWidth)
        # if self.player.x < 0:
        #     self.player.setX(0)
        # if self.player.x > self.SWidth:
        #     self.player.setX(self.SWidth)

        if self.player.x == self.goalImg.x and self.player.y == self.goalImg.y:
            if self.player.refl == self.goalImg.refl:
                if self.player.rot == self.goalImg.rot:
                   self.win.setVisibility(True)

    def render(self):
        if self.translating:
            mouseP = pygame.mouse.get_pos()
            pygame.draw.line(self.display, (100,100,255), [self.player.x,self.player.y], [mouseP[0],mouseP[1]],3)

        pygame.draw.rect(self.display, (200,200,200),[0,0,100,self.SHeight])
        self.goalImg.draw(self.display)
        self.player.draw(self.display)
        for tile in self.map:
            tile.draw(self.display)
        for tile in self.spikes:
            tile.draw(self.display)
        self.translationButton.draw(self.display)
        self.rotationButton.draw(self.display)
        self.reflectionButton.draw(self.display)
        for x in self.rotButtons:
            x[0].draw(self.display)
        for x in self.reflectionButtons:
            x[0].draw(self.display)
        self.win.draw(self.display)

g = game()
