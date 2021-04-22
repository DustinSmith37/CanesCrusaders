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
    def __init__(self,image,xPos=0,yPos=TOPBORDER,xMove=5,yMove=5,xLength=50,yLength=50):
        self.xPos=xPos
        self.yPos=yPos
        self.xMove=xMove
        self.yMove=yMove
        self.xLength=xLength
        self.yLength=yLength
        self.image = image
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
        return "{},xPos:{},yPos:{},xMove:{},yMove:{},xLength:{},yLength:{}".format(self.image,self.xPos,self.yPos,self.xMove,self.yMove,self.xLength,self.yLength)
        
#player class
class Player(Entity):
    def __init__(self,image,bulletSprite,xPos=0,yPos=TOPBORDER,xMove=5,yMove=5,xLength=50,yLength=50,health=3,healthLocation=5):
        Entity.__init__(self,image,xPos,yPos,xMove,yMove,xLength,yLength)
        self.bulletSprite=bulletSprite
        self.health = health
        self.invincibility = 0
        self.direction = {"up":False,"left":False,"down":False,"right":False}
        self.healthLocation = healthLocation
        playerList.append(self)
        self.alive = True
    def shoot(self):
        Bullet(image=self.bulletSprite,xPos=self.xPos+self.xLength/2,yPos=self.yPos)
    def damage(self):
        if(self.invincibility==0 and self.alive):
            self.health-=1
            self.invincibility = 30
        else:
            pass
        if(self.health==0 and self.alive):
            playerList.remove(self)
            entityDisplayList.remove(self)
            self.alive = False
    def heal(self):
        if self.health==0:
            self.alive = True
        self.health+=1

    def tickdown(self):
        self.invincibility -=1
        
    def movement(self,move,state):
        self.direction[move]=state
    
    def hitDetect(self):
        for enemy in enemyList:
            if enemy.xPos+enemy.xLength>self.xPos and enemy.xPos<self.xPos:
                if enemy.yPos+enemy.yLength>self.yPos and enemy.yPos<self.yPos:
                    self.damage()
                    enemy.remove()
                    break

    def __str__(self):
        return Entity.__str__(self)+",health:{}".format(self.health)

#enemy class
class Enemy(Entity):
    def __init__(self,image,xPos=0,yPos=TOPBORDER,xMove=5,yMove=50,xLength=50,yLength=50,health=1,direction="right"):
        Entity.__init__(self,image,xPos,yPos,xMove,yMove,xLength,yLength)
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
        if(self.yPos+self.yLength>=BOTTOMBORDER):
            self.remove()
            for player in playerList:
                player.damage()
    def damage(self):
        self.health -=1
        if self.health <= 0:
            self.remove()

    def remove(self):
        enemyList.remove(self)
        entityDisplayList.remove(self)

class speedEnemy(Enemy):
    def __init__(self,image,xPos=0,yPos=TOPBORDER,xMove=10,yMove=50,xLength=50,yLength=50,health=2,direction="right"):
        Enemy.__init__(self,image,xPos,yPos,xMove,yMove,xLength,yLength,health,direction)
 

class shootEnemy(Enemy):
    def __init__(self,image,bulletSprite,xPos=0,yPos=TOPBORDER,xMove=5,yMove=50,xLength=50,yLength=50,health=2,direction="right"):
        Enemy.__init__(self,image,xPos,yPos,xMove,yMove,xLength,yLength,health,direction)
        shootList.append(self)
        self.bulletSprite=bulletSprite

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
            enemyBullet(image=self.bulletSprite,xPos=self.xPos+self.xLength/2,yPos=self.yPos)
    def remove(self):
        enemyList.remove(self)
        shootList.remove(self)
        entityDisplayList.remove(self)

class tankEnemy(Enemy):
    def __init__(self,image,xPos=0,yPos=TOPBORDER,xMove=5,yMove=2,xLength=100,yLength=100,health=10,direction="right"):
        Enemy.__init__(self,image,xPos,yPos,xMove,yMove,xLength,yLength,health,direction)
    def autoMove(self):
        self.moveDown()
        if(self.yPos+self.yLength>=BOTTOMBORDER):
            self.remove()
            for player in playerList:
                player.damage()
#bullet class
class Bullet(Entity):
    def __init__(self,image,xPos=0,yPos=TOPBORDER,xMove=5,yMove=5,xLength=5,yLength=10):
        Entity.__init__(self,image,xPos,yPos,xMove,yMove,xLength,yLength)
        bulletList.append(self)
    def autoMove(self):
        self.yPos-=self.yMove
    def hitDetect(self):
        for enemy in enemyList:
            if enemy.xPos+enemy.xLength>self.xPos and enemy.xPos<self.xPos:
                if enemy.yPos+enemy.yLength>self.yPos and enemy.yPos<self.yPos:
                    enemy.damage()
                    self.remove()
                    global points
                    points +=10
                    break
        if self.yPos<=TOPBORDER:
            self.remove()   
    def remove(self):
        bulletList.remove(self)
        entityDisplayList.remove(self)
#moves entities into level creator or main game loop
class enemyBullet(Entity):
    def __init__(self,image,xPos=0,yPos=TOPBORDER,xMove=5,yMove=-5,xLength=5,yLength=10):
        Entity.__init__(self,image,xPos,yPos,xMove,yMove,xLength,yLength)
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
        if self.yPos+self.yLength>=BOTTOMBORDER:
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

def levelCreator(back,level,border,ChickDef,SaladDef,PopDef):
    if level == 1:
        Entity(back,xLength=WIDTH,yLength=BOTTOMBORDER-TOPBORDER)
        Entity(border,yPos=0,xLength=WIDTH,yLength=TOPBORDER)
        Entity(border,yPos=BOTTOMBORDER,yLength=HEIGHT-BOTTOMBORDER,xLength=WIDTH)
    else:
        entityDisplayList[0].image = back
    if(level==1):
        for i in range(1,13):
            Enemy(ChickDef, xPos=(60*i))
    if(level==2):
        for i in range(1,13):
            Enemy(SaladDef, xPos=(60*i))
    if(level==3):
        for i in range(1,13):
            Enemy(PopDef, xPos=(60*i))

def addEnemy(level,ChickDef,ChickFast,ChickShoot,ChickLarge,SaladDef,SaladFast,SaladShoot,SaladLarge,PopDef,PopFast,PopShoot,PopLarge,bulletColorEnemy):
    chance = randint(0,20)
    if(level==1):
        if(chance in [16,17]):
            speedEnemy(ChickFast,xPos=0)
            Enemy(ChickDef, xPos=0)
        elif(chance in [18,19]):
            shootEnemy(ChickShoot, xPos=0,bulletSprite=bulletColorEnemy)
            Enemy(ChickDef, xPos=0)
        elif(chance in [20]):
            tankEnemy(ChickLarge,xPos=randint(0,700))
            Enemy(ChickDef,xPos=0)
        else:
            Enemy(ChickDef, xPos=0)
    if(level==2):
        if(chance in [16,17]):
            speedEnemy(SaladFast,xPos=0)
            Enemy(SaladDef, xPos=0)
        elif(chance in [18,19]):
            shootEnemy(SaladShoot, xPos=0,bulletSprite=bulletColorEnemy)
            Enemy(SaladDef, xPos=0)
        elif(chance in [20]):
            tankEnemy(SaladLarge,xPos=randint(0,700))
            Enemy(SaladDef,xPos=0)
        else:
            Enemy(SaladDef, xPos=0)
    if(level==3):
        if(chance in [16,17]):
            speedEnemy(PopFast,xPos=0)
            Enemy(PopDef, xPos=0)
        elif(chance in [18,19]):
            shootEnemy(PopShoot, xPos=0,bulletSprite=bulletColorEnemy)
            Enemy(PopDef, xPos=0)
        elif(chance in [20]):
            tankEnemy(PopLarge,xPos=randint(0,700))
            Enemy(PopDef,xPos=0)
        else:
            Enemy(PopDef, xPos=0)
def titleScreen():
    #assets for title screen
    global Multiplayer
    background = pygame.transform.scale(pygame.image.load("SpaceBack.jpg"),(WIDTH,HEIGHT))
    guide = pygame.transform.scale(pygame.image.load("CanesBack.jpg"),(WIDTH-200,HEIGHT-200))
    toddTitle = pygame.transform.scale(pygame.image.load("ToddPNG.png"),(200,200))
    ajTitle = pygame.transform.scale(pygame.image.load("AJPNG.png"),(200,200))
    gameStart = False
    stage = "start"
    while not gameStart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                gameStart = True
                os._exit(1)
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE) and (stage == "guide") :
                    if Multiplayer:
                        stage = "inform2"
                    else:
                        stage = "inform1"
                if (event.key == pygame.K_e or event.key == pygame.K_BACKSLASH)and(stage == "inform1" or stage == "inform2"):
                    gameStart = True
                if event.key == pygame.K_1:
                    stage = "guide"
                    Multiplayer = False
                elif event.key == pygame.K_2:
                    stage = "guide"
                    Multiplayer = True
                #elif event.key
        gameDisplay.blit(background,(0,0))
        if stage == "start":
            line1 = bigText.render("CANES CRUSADERS",True,(255,255,255))
            gameDisplay.blit(line1,(100,150))
            line2 = medText.render("THE GREAT CHICKEN WARS",True,(255,0,0))
            gameDisplay.blit(line2,(160,220))
            gameDisplay.blit(toddTitle,(300,350))
            line2 = medText.render("SELECT NUMBER OF PLAYERS TO CONTINUE",True,(255,0,0))
            gameDisplay.blit(line2,(15,260))

        if stage == "inform2":
            line1 = bigText.render("MEET YOUR HEROES",True,(255,255,255))
            gameDisplay.blit(line1,(90,50))
            line2 = medText.render("TODD GRAVES",True,(255,255,255))
            gameDisplay.blit(line2,(70,250))
            line3 = medText.render("GOD KING OF",True,(255,255,255))
            gameDisplay.blit(line3,(80,300))
            line4 = medText.render("AJ",True,(255,255,255))
            gameDisplay.blit(line4,(600,250))
            line5 = medText.render("ANGEL OF",True,(255,255,255))
            gameDisplay.blit(line5,(550,300))
            line6 = medText.render("CHICKEN",True,(255,255,255))
            gameDisplay.blit(line6,(550,350))
            line7 = medText.render("MANKIND",True,(255,255,255))
            gameDisplay.blit(line7,(110,350))
            line8 = medText.render("PRESS ANY BUTTON TO CONTINUE",True,(255,0,0))
            gameDisplay.blit(line8,(100,120))
            gameDisplay.blit(toddTitle,(100,400))
            gameDisplay.blit(ajTitle,(500,400))
        
        if stage == "inform1":
            line1 = bigText.render("MEET YOUR HERO",True,(255,255,255))
            gameDisplay.blit(line1,(120,50))
            line2 = medText.render("TODD GRAVES",True,(255,255,255))
            gameDisplay.blit(line2,(70,250))
            line3 = medText.render("GOD KING OF",True,(255,255,255))
            gameDisplay.blit(line3,(80,300))
            line6 = medText.render("PRESS ANY BUTTON TO CONTINUE",True,(255,0,0))
            gameDisplay.blit(line6,(100,120))
            line7 = medText.render("MANKIND",True,(255,255,255))
            gameDisplay.blit(line7,(110,350))
            gameDisplay.blit(toddTitle,(100,400))
        
        if stage == "guide":
            line1 = bigText.render("HOW TO PLAY",True,(255,255,255))
            gameDisplay.blit(line1,(120,50))
            gameDisplay.blit(guide,(100,100))
            
        pygame.display.update()
        fps.tick(15)
def shop():
    ToddShop = pygame.transform.scale(pygame.image.load("ToddPNG.png"),(100,100))
    AjShop = pygame.transform.scale(pygame.image.load("AJPNG.png"),(100,100))
    ToddNum = 0
    AjNum = 0
    shopping = True
    while shopping:
        shopFront = pygame.transform.scale(pygame.image.load("SpaceBack.jpg"),(WIDTH,BOTTOMBORDER-TOPBORDER))
        gameDisplay.blit(shopFront,(0,TOPBORDER))
        Border = pygame.transform.scale(pygame.image.load("black.png"),(WIDTH,50))
        gameDisplay.blit(Border,(0,0))
        gameDisplay.blit(Border,(0,BOTTOMBORDER))
        pointDisplay = medText.render("Points: "+str(points),True,(255,255,255))
        levelDisplay = medText.render("Level: Shop",True,(255,255,255))
        gameDisplay.blit(pointDisplay, (590,10))
        gameDisplay.blit(levelDisplay, (10,10))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                shopping = False
                os._exit(1)
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    shopping = False
                    os._exit(1)
                if event.key == pygame.K_c:
                    shopping  = False
                #Todd's selection
                if event.key == pygame.K_a:
                    if ToddNum >0:
                        ToddNum -= 1
                if event.key == pygame.K_d:
                    if ToddNum<((WIDTH//100)-1):
                        ToddNum += 1
                #AJ's selection
                if(Multiplayer):
                    if event.key == pygame.K_LEFT:
                        if AjNum >0:
                            AjNum -= 1
                    if event.key == pygame.K_RIGHT:
                        if AjNum<((WIDTH//100)-1):
                            AjNum += 1
                #Todd and AJ's firing (space and enter respectively)
                if event.key == pygame.K_SPACE:
                    pass
                if(Multiplayer):
                    if event.key == pygame.K_RETURN:
                        pass
        fps.tick(30)
        gameDisplay.blit(ToddShop,(ToddNum*100,250))
        if Multiplayer:
            gameDisplay.blit(AjShop,(AjNum*100,450))
        pygame.display.flip()
def lose():
    pass
def mainGameLoop():
    global points
    global difficulty
    gameEnd=False
    topClear = False
    enemies = 13
    #Bullet Sprites
    bulletColorEnemy=pygame.transform.scale(pygame.image.load("bulletColorEnemy.jpg"),(5,10))
    bulletColorPlayer=pygame.transform.scale(pygame.image.load("bulletColorPlayer.jpg"),(5,10))
    #Background Sprites
    CanesBack = pygame.transform.scale(pygame.image.load("CanesBack.jpg"),(WIDTH,BOTTOMBORDER-TOPBORDER))
    Border = pygame.transform.scale(pygame.image.load("black.png"),(WIDTH,50))
    
    #Enemy Sprites
    ChickDef = pygame.transform.scale(pygame.image.load("Chick1.png"),(50,50))
    ChickFast = pygame.transform.scale(pygame.image.load("Chick1.png"),(50,50))
    ChickShoot = pygame.transform.scale(pygame.image.load("Chick1.png"),(50,50))
    ChickLarge = pygame.transform.scale(pygame.image.load("Chick1.png"),(100,100))
    SaladDef = pygame.transform.scale(pygame.image.load("SaladEnemy.png"),(50,50))
    SaladFast = pygame.transform.scale(pygame.image.load("SaladEnemy.png"),(50,50))
    SaladShoot = pygame.transform.scale(pygame.image.load("SaladEnemy.png"),(50,50))
    SaladLarge = pygame.transform.scale(pygame.image.load("SaladEnemy.png"),(100,100))
    PopDef = pygame.transform.scale(pygame.image.load("PopEnemy.png"),(50,50))
    PopFast = pygame.transform.scale(pygame.image.load("PopEnemy.png"),(50,50))
    PopShoot = pygame.transform.scale(pygame.image.load("PopEnemy.png"),(50,50))
    PopLarge = pygame.transform.scale(pygame.image.load("PopEnemy.png"),(100,100))
    #Level Creation
    global level
    levelCreator(CanesBack,level,Border,ChickDef,SaladDef,PopDef)
    #Player Sprites and creation
    ToddPng = pygame.transform.scale(pygame.image.load("ToddPNG.png"),(50,50))
    AjPng = pygame.transform.scale(pygame.image.load("AJPNG.png"),(50,50))
    hp = pygame.transform.scale(pygame.image.load("SpaceBack.jpg"),(30,30))
    if level == 1:
        Todd = Player(ToddPng,xLength=50,yLength=50,xPos=200,yPos=500,bulletSprite=bulletColorPlayer)
        if(Multiplayer):
            Aj = Player(AjPng,xLength=50,yLength=50,xPos=600,yPos=500, healthLocation=500,bulletSprite=bulletColorPlayer)
    else:
        Todd = playerList[0]
        if Multiplayer:
            Aj = playerList[1]
    



    for i in range(len(entityDisplayList)):
        gameDisplay.blit(entityDisplayList[i].image,(entityDisplayList[i].xPos,entityDisplayList[i].yPos))
    while not(gameEnd):
        print (points)
        for enemy in enemyList:
            
            if(enemy.yPos<=TOPBORDER+enemy.yLength and enemy.yPos>= TOPBORDER and enemy.xPos<=enemy.xLength+10 and enemy.xPos>=0 ):
                topClear = False
            else:
                topClear = True
        
        if(enemyList==[]):
            topClear = True
            
        if(enemies>0):
            if(topClear):
                addEnemy(level,ChickDef,ChickFast,ChickShoot,ChickLarge,SaladDef,SaladFast,SaladShoot,SaladLarge,PopDef,PopFast,PopShoot,PopLarge,bulletColorEnemy)
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
                if(Todd.alive):
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
                    if(Aj.alive):
                        if event.key == pygame.K_UP:
                            Aj.movement("up",True)
                        if event.key == pygame.K_LEFT:
                            Aj.movement("left",True)
                        if event.key == pygame.K_DOWN:
                            Aj.movement("down",True)
                        if event.key == pygame.K_RIGHT:
                            Aj.movement("right",True)
                #Todd and AJ's firing (space and enter respectively)
                if(Todd.alive):
                    if event.key == pygame.K_SPACE:
                        Todd.shoot()
                if(Multiplayer):
                    if(Aj.alive):
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
        for player in playerList:
            player.hitDetect()
        if enemyList == []:
            for bullet in range(len(bulletList)):
                bulletList[0].remove()
            shop()
            level += 1
            difficulty += 1
            enemies = difficulty * 13
            print(level)
            levelCreator(CanesBack, level, Border, ChickDef, SaladDef, PopDef)
            
            
        for entity in entityDisplayList:
            gameDisplay.blit(entity.image,(entity.xPos,entity.yPos))
            
        collectiveHealth = 0
        for player in playerList:
            for i in range(player.health):
                collectiveHealth += 1
                gameDisplay.blit(hp,(player.healthLocation+i*50,BOTTOMBORDER+10))
        if collectiveHealth <= 0:
            break
        
        pointDisplay = medText.render("Points: "+str(points),True,(255,255,255))
        levelDisplay = medText.render("Level: " +str(level), True,(255,255,255))
        gameDisplay.blit(pointDisplay, (590,10))
        gameDisplay.blit(levelDisplay, (10,10))
        pygame.display.flip()
        
#IMPORT DATA: GOVERNS ENTIRE GAME, BOTH IN LEVEL, SHOP, AND LOSE SCREEN
global Multiplayer 
Multiplayer = True
global difficulty 
difficulty= 3
global level 
level = 1
global points 
points = 0
#TEXT ASSETS, these will never change so are global usage (because screw passing these into every single game window)
global bigText
bigText = pygame.font.SysFont('Arial MS', 90)
global medText
medText = pygame.font.SysFont('Arial MS', 50)
global tinyText
tinyText = pygame.font.SysFont('Arial MS', 25)

titleScreen()
mainGameLoop()
lose()
