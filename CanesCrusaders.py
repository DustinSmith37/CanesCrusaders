#import the needed modules, pygame is obvious, time for tick speed,
#and os for leaving the game without causing errors
import pygame, time, os
from random import randint
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
playerList=[]
enemyList=[]
bulletList=[]
shootList=[]


#entity class
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
        
#player class
class Player(Entity):
    def __init__(self,file,xPos=0,yPos=TOPBORDER,xMove=5,yMove=5,xLength=50,yLength=50,health=3):
        Entity.__init__(self,file,xPos,yPos,xMove,yMove,xLength,yLength)
        self.health = health
        self.invincibility = 0
        self.direction = {"up":False,"left":False,"down":False,"right":False}
        playerList.append(self)
    def shoot(self):
        Bullet(file="bulletColorPlayer.jpg",xPos=self.xPos+self.xLength/2,yPos=self.yPos)
    def damage(self):
        if(self.invincibility==0):
            self.health-=1
            self.invincibility = 30
        else:
            pass
        if(self.health==0):
            playerList.remove(self)
            entityDisplayList.remove(self)

    def tickdown(self):
        self.invincibility -=1
        
    def movement(self,move,state):
        self.direction[move]=state
    def __str__(self):
        return Entity.__str__(self)+",health:{}".format(self.health)

#enemy class
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
    def damage(self):
        self.health -=1
        if self.health < 0:
            self.remove()

    def remove(self):
        enemyList.remove(self)
        entityDisplayList.remove(self)

class speedEnemy(Enemy):
    def __init__(self,file,xPos=0,yPos=TOPBORDER,xMove=10,yMove=50,xLength=50,yLength=50,health=1,direction="right"):
        Enemy.__init__(self,file,xPos,yPos,xMove,yMove,xLength,yLength,health,direction)
 

class shootEnemy(Enemy):
    def __init__(self,file,xPos=0,yPos=TOPBORDER,xMove=5,yMove=50,xLength=50,yLength=50,health=1,direction="right",bulletSprite=""):
        Enemy.__init__(self,file,xPos,yPos,xMove,yMove,xLength,yLength,health,direction)
        shootList.append(self)

    def autoMove(self):
        if self.direction == "left":
            self.moveLeft()
        elif self.direction == "right":
            self.moveRight()
        if self.xPos == 0:
            self.direction = "right"
        elif self.xPos == WIDTH-self.xLength:
            self.direction = "left"
    def fire(self):
        shot = randint(0,30)
        if(shot==30):
            enemyBullet(file="bulletColorEnemy.jpg",xPos=self.xPos+self.xLength/2,yPos=self.yPos)
    def remove(self):
        enemyList.remove(self)
        shootList.remove(self)
        entityDisplayList.remove(self)

#bullet class
class Bullet(Entity):
    def __init__(self,file,xPos=0,yPos=TOPBORDER,xMove=5,yMove=5,xLength=5,yLength=10):
        Entity.__init__(self,file,xPos,yPos,xMove,yMove,xLength,yLength)
        bulletList.append(self)
    def autoMove(self):
        self.yPos-=self.yMove
    def hitDetect(self):
        for enemy in enemyList:
            if enemy.xPos+enemy.xLength>self.xPos and enemy.xPos<self.xPos:
                if enemy.yPos+enemy.yLength>self.yPos and enemy.yPos<self.yPos:
                    enemy.damage()
                    self.remove()
                    break
        if self.yPos<=TOPBORDER:
            self.remove()   
    def remove(self):
        bulletList.remove(self)
        entityDisplayList.remove(self)
#moves entities into level creator or main game loop
class enemyBullet(Entity):
    def __init__(self,file,xPos=0,yPos=TOPBORDER,xMove=5,yMove=-5,xLength=5,yLength=10):
        Entity.__init__(self,file,xPos,yPos,xMove,yMove,xLength,yLength)
        bulletList.append(self)
    def autoMove(self):
        self.yPos-=self.yMove
    def hitDetect(self):
        for player in playerList:
            if player.xPos+player.xLength>self.xPos and player.xPos<self.xPos:
                if player.yPos+player.yLength>self.yPos and player.yPos<self.yPos:
                    player.damage()
                    self.remove()
                    break
        if (self.yPos<=(self.yPos==BOTTOMBORDER-self.yLength)):
            self.remove()   
    def remove(self):
        bulletList.remove(self)
        entityDisplayList.remove(self)
    
def playerMove(player):
    if player.direction["up"]==True:
        player.moveUp()
    if player.direction["left"]==True:
        player.moveLeft()
    if player.direction["down"]==True:
        player.moveDown()
    if player.direction["right"]==True:
        player.moveRight()
def levelCreator(back,level):
    Background = Entity(back,xLength=WIDTH,yLength=BOTTOMBORDER-TOPBORDER)
    TopBorder = Entity("black.png",yPos=0,xLength=WIDTH,yLength=TOPBORDER)
    BotBorder = Entity("black.png",yPos=BOTTOMBORDER,yLength=HEIGHT-BOTTOMBORDER,xLength=WIDTH)
    if(level==1):
        for i in range(1,13):
            Enemy("Chick1.png", xPos=(60*i))
    if(level==2):
        for i in range(1,13):
            Enemy("SaladEnemy.png", xPos=(60*i))
    if(level==3):
        for i in range(1,13):
            Enemy("PopEnemy.png", xPos=(60*i))

def addEnemy(level):
    chance = randint(0,20)
    if(level==1):
        if(chance in [16,17]):
            speedEnemy("Chick1.png",xPos=0)
            Enemy("Chick1.png", xPos=0)
        elif(chance in [18,19]):
            shootEnemy("Chick1.png", xPos=0)
            Enemy("Chick1.png", xPos=0)
        else:
            Enemy("Chick1.png", xPos=0)
    if(level==2):
        if(chance in [16,17]):
            speedEnemy("SaladEnemy.png",xPos=0)
            Enemy("SaladEnemy.png", xPos=0)
        elif(chance in [18,19]):
            shootEnemy("SaladEnemy.png", xPos=0)
            Enemy("SaladEnemy.png", xPos=0)
        else:
            Enemy("SaladEnemy.png", xPos=0)
    if(level==3):
        if(chance in [16,17]):
            speedEnemy("PopEnemy.png",xPos=0)
            Enemy("PopEnemy.png", xPos=0)
        elif(chance in [18,19]):
            shootEnemy("PopEnemy.png", xPos=0)
            Enemy("PopEnemy.png", xPos=0)
        else:
            Enemy("PopEnemy.png", xPos=0)



def mainGameLoop():
    gameEnd=False
    topClear = False
    Multiplayer = True
    difficulty = 3
    enemies = difficulty*10
    level=2
    levelCreator("CanesBack.jpg",level)
    Todd = Player("ToddPNG.png",xLength=50,yLength=50,xPos=200,yPos=500)
    if(Multiplayer):
        Aj = Player("AJPNG.png",xLength=50,yLength=50,xPos=600,yPos=500)



    for i in range(len(entityDisplayList)):
        gameDisplay.blit(entityDisplayList[i].image,(entityDisplayList[i].xPos,entityDisplayList[i].yPos))
    while not(gameEnd):
        for enemy in enemyList:
            
            if(enemy.yPos<=TOPBORDER+enemy.yLength and enemy.yPos>= TOPBORDER and enemy.xPos<=enemy.xLength+10 and enemy.xPos>=0 ):
                topClear = False
            else:
                topClear = True
        
        if(enemyList==[]):
            topClear = True
            
        if(enemies>0):
            if(topClear):
                addEnemy(level)
                enemies-=1
                
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
                if(Todd.health>0):
                    if event.key == pygame.K_w:
                        Todd.movement("up",True)
                    if event.key == pygame.K_a:
                        Todd.movement("left",True)
                    if event.key == pygame.K_s:
                        Todd.movement("down",True)
                    if event.key == pygame.K_d:
                        Todd.movement("right",True)
                #AJ's 4 directional movement engaged
                if(Multiplayer):
                    if(Aj.health>0):
                        if event.key == pygame.K_UP:
                            Aj.movement("up",True)
                        if event.key == pygame.K_LEFT:
                            Aj.movement("left",True)
                        if event.key == pygame.K_DOWN:
                            Aj.movement("down",True)
                        if event.key == pygame.K_RIGHT:
                            Aj.movement("right",True)
                #Todd and AJ's firing (space and enter respectively)
                if(Todd.health>0):
                    if event.key == pygame.K_SPACE:
                        Todd.shoot()
                if(Multiplayer):
                    if(Aj.health>0):
                        if event.key == pygame.K_RETURN:
                            Aj.shoot()
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
                if(Multiplayer):
                    if event.key == pygame.K_UP:
                        Aj.movement("up",False)
                    if event.key == pygame.K_LEFT:
                        Aj.movement("left",False)
                    if event.key == pygame.K_DOWN:
                        Aj.movement("down",False)
                    if event.key == pygame.K_RIGHT:
                        Aj.movement("right",False)
        playerMove(Todd)
        if(Multiplayer):
            playerMove(Aj)
        fps.tick(30)
        for bullet in bulletList:
            bullet.autoMove()
            bullet.hitDetect()
        for enemy in enemyList:
            enemy.autoMove()
        for player in playerList:
            if(player.invincibility>0):
                player.tickdown()
        for enemy in shootList:
            shootEnemy.fire(enemy)
        for entity in entityDisplayList:
            gameDisplay.blit(entity.image,(entity.xPos,entity.yPos))
        
        
        pygame.display.flip()


mainGameLoop()

