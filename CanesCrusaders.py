#import the needed modules, pygame is obvious, time for tick speed,
#and os for leaving the game without causing errors
import pygame, time, os
#initialize pygame, its font's and it's music player
pygame.init()
pygame.font.init()
pygame.mixer.init()
#set a variable called FPS that is just the clock function from time
fps = pygame.time.Clock()
#display the pygame window, set it to be 800 by 600 and be fullscreen (when not debugging)
WIDTH = 800
HEIGHT = 600
TOPBORDER = 50
BOTTOMBORDER = HEIGHT-50
gameDisplay = pygame.display.set_mode((WIDTH,HEIGHT),)#pygame.FULLSCREEN)
#set its name to be Canes Crusaders
pygame.display.set_caption('Canes Crusaders')
#a master list of all entities that need to be displayed, listed in order of importance
entityDisplayList=[]
enemyList=[]
bulletList=[]
class Entity():
    #default stats every asset will have, like the file name, position, movement, and size
    def __init__(self,file,xPos=0,yPos=TOPBORDER,xMove=5,yMove=5,xLength=50,yLength=50):
        self.file=file
        self.xPos=xPos
        self.yPos=yPos
        self.xMove=xMove
        self.yMove=yMove
        self.xLength=xLength
        self.yLength=yLength
        self.image = pygame.transform.scale(pygame.image.load(file),(self.xLength,self.yLength))
        entityDisplayList.append(self)
    #movement controls. This allows any entity to move its set speed that direction
    def moveLeft(self):
        self.xPos-=self.xMove
        if self.xPos<0:
            self.xPos=0
    def moveRight(self):
        self.xPos+=self.xMove
        if self.xPos>WIDTH-self.xLength:
            self.xPos=WIDTH-self.xLength
    def moveUp(self):
        self.yPos-=self.yMove
        if self.yPos<TOPBORDER:
            self.yPos=TOPBORDER
    def moveDown(self):
        self.yPos+=self.yMove
        if self.yPos>BOTTOMBORDER-self.yLength:
            self.yPos=BOTTOMBORDER-self.yLength
    def remove(self):
        entityDisplayList.remove(self)
    def __str__(self):
        return "{},xPos:{},yPos:{},xMove:{},yMove:{},xLength:{},yLength:{}".format(self.file,self.xPos,self.yPos,self.xMove,self.yMove,self.xLength,self.yLength)
class Player(Entity):
    def __init__(self,file,xPos=0,yPos=TOPBORDER,xMove=5,yMove=5,xLength=50,yLength=50,health=3):
        Entity.__init__(self,file,xPos,yPos,xMove,yMove,xLength,yLength)
        self.health = health
        self.direction = {"up":False,"left":False,"down":False,"right":False}
    def shoot(self):
        pass
    def damaged(self):
        self.health-=1
    def movement(self,move,state):
        self.direction[move]=state
    def __str__(self):
        return Entity.__str__(self)+",health:{}".format(self.health)
class Enemy(Entity):
    def __init__(self,file,xPos=0,yPos=TOPBORDER,xMove=5,yMove=50,xLength=50,yLength=50,health=1,direction="right"):
        Entity.__init__(self,file,xPos,yPos,xMove,yMove,xLength,yLength)
        enemyList.append(self)
        self.health = health
        self.direction = direction
    def autoMove(self):
        if self.direction == "left":
            self.moveLeft()
        elif self.direction == "right":
            self.moveRight()
        if self.xPos == 0:
            self.direction = "right"
            self.moveDown()
        elif self.xPos == WIDTH-self.xLength:
            self.direction = "left"
            self.moveDown() 
    def fire(self):
        pass
    def remove(self):
        enemyList.remove(self)
        entityDisplayList.remove(self)
Background = Entity("CanesBack.jpg",xLength=WIDTH,yLength=BOTTOMBORDER-TOPBORDER)
Todd = Player("ToddPNG.png",xLength=125,yLength=175,xPos=200,yPos=300)
Aj = Player("AJPNG.png",xLength=125,yLength=175,xPos=600,yPos=300)
e1 = Enemy("Chick1.png")
e2 = Enemy("Chick1.png",xPos=60)

for i in range(len(entityDisplayList)):
    gameDisplay.blit(entityDisplayList[i].image,(entityDisplayList[i].xPos,entityDisplayList[i].yPos))
    
def playerMove(player):
    if player.direction["up"]==True:
        player.moveUp()
    if player.direction["left"]==True:
        player.moveLeft()
    if player.direction["down"]==True:
        player.moveDown()
    if player.direction["right"]==True:
        player.moveRight()
    
    

def mainGameLoop():
    gameEnd=False
    while not(gameEnd):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                gameEnd = True
                os._exit(1)
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    gameEnd = True
                    os._exit(1)
                #Todd's 4 directional movement engaged
                if event.key == pygame.K_w:
                    Todd.movement("up",True)
                if event.key == pygame.K_a:
                    Todd.movement("left",True)
                if event.key == pygame.K_s:
                    Todd.movement("down",True)
                if event.key == pygame.K_d:
                    Todd.movement("right",True)
                #AJ's 4 directional movement engaged
                if event.key == pygame.K_UP:
                    Aj.movement("up",True)
                if event.key == pygame.K_LEFT:
                    Aj.movement("left",True)
                if event.key == pygame.K_DOWN:
                    Aj.movement("down",True)
                if event.key == pygame.K_RIGHT:
                    Aj.movement("right",True)
            if event.type==pygame.KEYUP:
                #Todd's 4 directional movement disengaged
                if event.key == pygame.K_w:
                    Todd.movement("up",False)
                if event.key == pygame.K_a:
                    Todd.movement("left",False)
                if event.key == pygame.K_s:
                    Todd.movement("down",False)
                if event.key == pygame.K_d:
                    Todd.movement("right",False)
                #AJ's 4 directional movement disengaged
                if event.key == pygame.K_UP:
                    Aj.movement("up",False)
                if event.key == pygame.K_LEFT:
                    Aj.movement("left",False)
                if event.key == pygame.K_DOWN:
                    Aj.movement("down",False)
                if event.key == pygame.K_RIGHT:
                    Aj.movement("right",False)
        playerMove(Todd)
        playerMove(Aj)
        fps.tick(30)
        for enemy in enemyList:
            enemy.autoMove()
        for entity in entityDisplayList:
            gameDisplay.blit(entity.image,(entity.xPos,entity.yPos))
        pygame.display.flip()
mainGameLoop()

