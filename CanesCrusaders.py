#import the needed modules, pygame is obvious, time for tick speed,
#and os for leaving the game without causing errors
#THIS IS A TEST COMMENT TO MAKE SURE GITHUB NO GAY
#WHAT IF GITHUB GAY THO???
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
        if (self.xPos<0):
            self.xPos=0
    def moveRight(self):
        self.xPos+=self.xMove
        if (self.xPos>WIDTH-self.xLength):
            self.xPos=WIDTH-self.xLength
    def moveUp(self):
        self.yPos-=self.yMove
        if (self.yPos<TOPBORDER):
            self.yPos=TOPBORDER
    def moveDown(self):
        self.yPos+=self.yMove
        if (self.yPos>BOTTOMBORDER-self.yLength):
            self.yPos=BOTTOMBORDER-self.yLength
    def remove(self):
        entityDisplayList.remove(self)
    def __str__(self):
        return "{},xPos:{},yPos:{},xMove:{},yMove:{},xLength:{},yLength:{}".format(self.image,self.xPos,self.yPos,self.xMove,self.yMove,self.xLength,self.yLength)
        
#player class
class Player(Entity):
    def __init__(self,image,bulletSprite,xPos=0,yPos=TOPBORDER,xMove=7,yMove=5,xLength=50,yLength=50,health=3,healthLocation=5):
        Entity.__init__(self,image,xPos,yPos,xMove,yMove,xLength,yLength)
        self.bulletSprite=bulletSprite
        self.health = health
        self.invincibility = 0
        self.direction = {"up":False,"left":False,"down":False,"right":False}
        self.healthLocation = healthLocation
        playerList.append(self)
        self.alive = True
        self.upgrades = {"doubleShoot":False,"doubleDamage":False,"doubleDamage2":False,"doubleDamage3":False,"fastMove":False}
        self.specialActive = "shotgun"
        self.specialBought = {"shotgun":True,"laser":False,"minigun":False,"cannon":False,"superbreaker":False,"shield":False}
        #list of specials
        #shotgun: 3/6 shots based on upgrade
        #laser: continous beam, gets wider with double shot
        #minigun: lots of shots
        #cannon: aoe explosion
        #superbreaker: fires all the way to the top dealing damage as it goes
        #shield: I frames on demand
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
        if (self.health==0):
            self.alive = True
        self.health+=1

    def tickdown(self):
        self.invincibility -=1
        
    def movement(self,move,state):
        self.direction[move]=state
    
    def hitDetect(self):
        for enemy in enemyList:
            if (enemy.xPos+enemy.xLength>self.xPos and enemy.xPos<self.xPos):
                if (enemy.yPos+enemy.yLength>self.yPos and enemy.yPos<self.yPos):
                    self.damage()
                    enemy.remove()
                    break

    def __str__(self):
        return Entity.__str__(self)+",health:{}".format(self.health)

#enemy class
class Enemy(Entity):
    def __init__(self,image,xPos=0,yPos=TOPBORDER,xMove=5,yMove=50,xLength=50,yLength=50,health=2,direction="right"):
        Entity.__init__(self,image,xPos,yPos,xMove,yMove,xLength,yLength)
        enemyList.append(self)
        self.health = health
        self.direction = direction
    def autoMove(self):
        if (self.direction == "left"):
            self.moveLeft()
        elif (self.direction == "right"):
            self.moveRight()
        if (self.xPos == 0):
            self.direction = "right"
            self.moveDown()
        elif (self.xPos == WIDTH-self.xLength):
            self.direction = "left"
            self.moveDown() 
        if(self.yPos+self.yLength>=BOTTOMBORDER):
            self.remove()
            for player in playerList:
                player.damage()
    def damage(self):
        self.health -=1
        if (self.health <= 0):
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
        if (self.direction == "left"):
            self.moveLeft()
        elif (self.direction == "right"):
            self.moveRight()
        if (self.xPos == 0):
            self.direction = "right"
        elif (self.xPos == WIDTH-self.xLength):
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
            if (enemy.xPos+enemy.xLength>self.xPos and enemy.xPos<self.xPos):
                if (enemy.yPos+enemy.yLength>self.yPos and enemy.yPos<self.yPos):
                    enemy.damage()
                    self.remove()
                    global points
                    points +=10
                    break
        if (self.yPos<=TOPBORDER):
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
            if (player.xPos+player.xLength>self.xPos and player.xPos<self.xPos):
                if (player.yPos+player.yLength>self.yPos and player.yPos<self.yPos):
                    player.damage()
                    self.remove()
                    break
            elif (self.yPos+self.yLength>=BOTTOMBORDER):
                self.remove()   
    def remove(self):
        bulletList.remove(self)
        entityDisplayList.remove(self)
    
def playerMove(player):
    if (player.direction["up"]==True):
        player.moveUp()
    if (player.direction["left"]==True):
        player.moveLeft()
    if (player.direction["down"]==True):
        player.moveDown()
    if (player.direction["right"]==True):
        player.moveRight()

def levelCreator(back,level,border,DefEnemy):
    if (level == 1):
        Entity(back,xLength=WIDTH,yLength=BOTTOMBORDER-TOPBORDER)
        Entity(border,yPos=0,xLength=WIDTH,yLength=TOPBORDER)
        Entity(border,yPos=BOTTOMBORDER,yLength=HEIGHT-BOTTOMBORDER,xLength=WIDTH)
    else:
        entityDisplayList[0].image = back
    for i in range(0,13):
        Enemy(DefEnemy, xPos=(60*i))

def addEnemy(Def,Fast,Shooter,Large,bulletColorEnemy):
    chance = randint(0,30)
    if(chance in [14,15,16,17]):
        speedEnemy(Fast,xPos=0)
        Enemy(Def, xPos=0)
    elif(chance in [19,21,22]):
        shootEnemy(Shooter, xPos=0,bulletSprite=bulletColorEnemy)
    elif(chance in [20]):
        tankEnemy(Large,xPos=randint(0,700))
        Enemy(Def,xPos=0)
    else:
        Enemy(Def, xPos=0)

def purchase(buyer,buyerX,buyerY):
    global points
    buyGrid=[{"doubleShoot":250,"doubleDamage":500,"doubleDamage2":1000,"doubleDamage3":2000,"fastMove":500,"heal":100},{"shotgun":0, "laser":250}]
    upgrade = None
    special = None
    index = 0
    status = "What would you like to buy?"
    if buyerY == 0:
        for key in buyGrid[0].keys():
            if index == buyerX:
                upgrade = key
                break
            else:
                index+=1
    else:
        for key in buyGrid[1].keys():
            if index == buyerX:
                special = key
                break
            else:
                index+=1
    if upgrade != None:
        if points >= buyGrid[0][upgrade]:
            if upgrade == "heal":
                buyer.heal()
                points -= buyGrid[0]["heal"]
                status = "You have healed! Well done!"
            else:
                points -= buyGrid[0][upgrade]
                buyer.upgrades[upgrade]=True
                status = "You have bought an upgrade! Well done!"
        else:
            status = "You do not have enough points!"
    elif special != None:
        if points >= buyGrid[1][special]:
            if buyer.specialBought[special] ==False:
                points -= buyGrid[1][special]
                buyer.specialBought[special]=True
                buyer.specialActive = special
                status = "You have bought a special move! Well done!"
            if buyer.specialBought[special]==True:
                buyer.specialActive = special
                status = "You have swapped your active special. Well done!"
        else:
            status = "You do not have enough points!"
    return status

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
            if (event.type == pygame.QUIT):
                pygame.quit()
                gameStart = True
                os._exit(1)
            elif event.type == pygame.KEYDOWN:
                if ((event.key == pygame.K_RETURN or event.key == pygame.K_SPACE) and (stage == "guide")):
                    if (Multiplayer):
                        stage = "inform2"
                    else:
                        stage = "inform1"
                if ((event.key == pygame.K_e or event.key == pygame.K_BACKSLASH)and(stage == "inform1" or stage == "inform2")):
                    gameStart = True
                if (event.key == pygame.K_1):
                    stage = "guide"
                    Multiplayer = False
                elif (event.key == pygame.K_2):
                    stage = "guide"
                    Multiplayer = True
                #elif event.key
        gameDisplay.blit(background,(0,0))
        if (stage == "start"):
            line1 = bigText.render("CANES CRUSADERS",True,(255,255,255))
            gameDisplay.blit(line1,(100,150))
            line2 = medText.render("THE GREAT CHICKEN WARS",True,(255,0,0))
            gameDisplay.blit(line2,(160,220))
            gameDisplay.blit(toddTitle,(300,350))
            line2 = medText.render("SELECT NUMBER OF PLAYERS TO CONTINUE",True,(255,0,0))
            gameDisplay.blit(line2,(15,260))

        if (stage == "inform2"):
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
        
        if (stage == "inform1"):
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
        
        if (stage == "guide"):
            line1 = bigText.render("HOW TO PLAY",True,(255,255,255))
            gameDisplay.blit(line1,(120,50))
            gameDisplay.blit(guide,(100,100))
            
        pygame.display.update()
        fps.tick(30)
def shop():
    ToddShop = pygame.transform.scale(pygame.image.load("ToddPNG.png"),(50,50))
    AjShop = pygame.transform.scale(pygame.image.load("AJPNG.png"),(50,50))
    hp = pygame.transform.scale(pygame.image.load("Cane Heart.png"),(30,30))
    ToddPos = {"xPos":0,"yPos":0}
    AjPos = {"xPos":0,"yPos":0}
    shopping = True
    global points
    points += 1000
    status = "What would you like to buy?"
    shopFront = pygame.transform.scale(pygame.image.load("SpaceBack.jpg"),(WIDTH,BOTTOMBORDER-TOPBORDER))
    CoolCane = pygame.transform.scale(pygame.image.load("CoolCanePNG.png"),(100,100))
    TextBack = pygame.transform.scale(pygame.image.load("WhiteBorder.jpeg"),(500,100))
    Heal = pygame.transform.scale(pygame.image.load("Cane Heart.png"),(75,75))
    ownedText = tinyText.render("Owned",True,(255,255,255))
    activeText = tinyText.render("Active",True,(255,255,255))
    levelDisplay = medText.render("Level: Shop",True,(255,255,255))
    Border = pygame.transform.scale(pygame.image.load("black.png"),(WIDTH,50))
    DoubleDamage = pygame.transform.scale(pygame.image.load("DoubleDamage.png"),(75,75))
    TripleDamage = pygame.transform.scale(pygame.image.load("TripleDamage.png"),(75,75))



    while (shopping):
        gameDisplay.blit(shopFront,(0,TOPBORDER))
        gameDisplay.blit(Border,(0,0))
        gameDisplay.blit(Border,(0,BOTTOMBORDER))
        gameDisplay.blit(TextBack,(300,TOPBORDER))
        pointDisplay = medText.render("Points: "+str(points),True,(255,255,255))
        gameDisplay.blit(pointDisplay, (590,10))
        gameDisplay.blit(levelDisplay, (10,10))
        gameDisplay.blit(ownedText,(0,200))
        gameDisplay.blit(ownedText,(0,400))
        gameDisplay.blit(activeText,(0,450))
        gameDisplay.blit(Heal,(710,200))
        gameDisplay.blit(DoubleDamage,(220,200))
        gameDisplay.blit(TripleDamage,(340,200))

        gameDisplay.blit(CoolCane,(200,TOPBORDER))
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                shopping = False
                os._exit(1)
            if (event.type ==pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    shopping = False
                    os._exit(1)
                if (event.key == pygame.K_1 or event.key == pygame.K_2):
                    shopping  = False
                #Todd's selection
                if (event.key == pygame.K_a):
                    if (ToddPos["xPos"] >0):
                        ToddPos["xPos"] -= 1
                if (event.key == pygame.K_d):
                    if (ToddPos["xPos"]<5):
                        ToddPos["xPos"] += 1
                if (event.key == pygame.K_w):
                    if (ToddPos["yPos"] >0):
                        ToddPos["yPos"] -= 1
                if (event.key == pygame.K_s):
                    if (ToddPos["yPos"]<1):
                        ToddPos["yPos"] += 1
                    
                #AJ's selection
                if(Multiplayer):
                    if (event.key == pygame.K_LEFT):
                        if (AjPos["xPos"] >0):
                            AjPos["xPos"] -= 1
                    if (event.key == pygame.K_RIGHT):
                        if (AjPos["xPos"]<5):
                            AjPos["xPos"] += 1
                    if (event.key == pygame.K_UP):
                        if (AjPos["yPos"] >0):
                            AjPos["yPos"] -= 1
                    if (event.key == pygame.K_DOWN):
                        if (AjPos["yPos"]<1):
                            AjPos["yPos"] += 1
                #Todd and AJ's firing (space and enter respectively)
                if (event.key == pygame.K_SPACE):
                    status = purchase(playerList[0],ToddPos["xPos"],ToddPos["yPos"])
                if(Multiplayer):
                    if (event.key == pygame.K_RETURN):
                        status = purchase(playerList[1],AjPos["xPos"],AjPos["yPos"])
        fps.tick(30)
        gameDisplay.blit(ToddShop,(ToddPos["xPos"]*125+75,ToddPos["yPos"]*200+300))
        if Multiplayer:
            gameDisplay.blit(AjShop,(AjPos["xPos"]*125+130,AjPos["yPos"]*200+300))
        
        RC3Message = tinyText.render("RC3: "+str(status),True,(0,0,0))
        gameDisplay.blit(RC3Message,(320,100))
        for player in playerList:
            for i in range(player.health):
                gameDisplay.blit(hp,(player.healthLocation+i*50,BOTTOMBORDER+10))
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
    ChickFast = pygame.transform.scale(pygame.image.load("ChickFast.png"),(50,50))
    ChickShoot = pygame.transform.scale(pygame.image.load("ChickShoot.png"),(50,50))
    ChickLarge = pygame.transform.scale(pygame.image.load("ChickLarge.png"),(100,100))

    SaladDef = pygame.transform.scale(pygame.image.load("SaladEnemy.png"),(50,50))
    SaladFast = pygame.transform.scale(pygame.image.load("SaladFast.png"),(50,50))
    SaladShoot = pygame.transform.scale(pygame.image.load("SaladShoot.png"),(50,50))
    SaladLarge = pygame.transform.scale(pygame.image.load("SaladLarge.png"),(100,100))

    PopDef = pygame.transform.scale(pygame.image.load("PopEnemy.png"),(50,50))
    PopFast = pygame.transform.scale(pygame.image.load("PopFast.png"),(50,50))
    PopShoot = pygame.transform.scale(pygame.image.load("PopShoot.png"),(50,50))
    PopLarge = pygame.transform.scale(pygame.image.load("PopLarge.png"),(100,100))

    BBWDef = pygame.transform.scale(pygame.image.load("BDubsPNG.png"),(50,50))
    BBWFast = pygame.transform.scale(pygame.image.load("BDubsFast.png"),(50,50))
    BBWShoot = pygame.transform.scale(pygame.image.load("BDubsShoot.png"),(50,50))
    BBWLarge = pygame.transform.scale(pygame.image.load("BDubsLarge.png"),(100,100))

    ChurchDef = pygame.transform.scale(pygame.image.load("ChurchChick.png"),(50,50))
    ChurchFast = pygame.transform.scale(pygame.image.load("ChurchFast.png"),(50,50))
    ChurchShoot = pygame.transform.scale(pygame.image.load("ChurchShoot.png"),(50,50))
    ChurchLarge = pygame.transform.scale(pygame.image.load("ChurchLarge.png"),(100,100))

    ZaxbyDef = pygame.transform.scale(pygame.image.load("ZaxbyPNG.png"),(50,50))
    ZaxbyFast = pygame.transform.scale(pygame.image.load("ZaxbyFast.png"),(50,50))
    ZaxbyShoot = pygame.transform.scale(pygame.image.load("ZaxbyShoot.png"),(50,50))
    ZaxbyLarge = pygame.transform.scale(pygame.image.load("ZaxbyLarge.png"),(100,100))

    KFCDef = pygame.transform.scale(pygame.image.load("KFCEnemy.png"),(50,50))
    KFCFast = pygame.transform.scale(pygame.image.load("KFCFast.png"),(50,50))
    KFCShoot = pygame.transform.scale(pygame.image.load("KFCShoot.png"),(50,50))
    KFCLarge = pygame.transform.scale(pygame.image.load("KFCLarge.png"),(100,100))
    #Level Creation
    global level
    levelCreator(CanesBack,level,Border,ZaxbyDef)
    #Player Sprites and creation
    ToddPng = pygame.transform.scale(pygame.image.load("ToddPNG.png"),(50,50))
    AjPng = pygame.transform.scale(pygame.image.load("AJPNG.png"),(50,50))
    hp = pygame.transform.scale(pygame.image.load("Cane Heart.png"),(30,30))
    Todd = Player(ToddPng,xLength=50,yLength=50,xPos=200,yPos=500,bulletSprite=bulletColorPlayer)
    if(Multiplayer):
        Aj = Player(AjPng,xLength=50,yLength=50,xPos=600,yPos=500, healthLocation=500,bulletSprite=bulletColorPlayer)
    



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
                if(level ==1):
                    addEnemy(ZaxbyDef,ZaxbyFast,ZaxbyShoot,ZaxbyLarge,bulletColorEnemy)
                elif(level ==2):
                    addEnemy(SaladDef,SaladFast,SaladShoot,SaladLarge,bulletColorEnemy)
                elif(level ==3):
                    addEnemy(PopDef,PopFast,PopShoot,PopLarge,bulletColorEnemy)
                elif(level ==4):
                    addEnemy(BBWDef,BBWFast,BBWShoot,BBWLarge,bulletColorEnemy)
                elif(level ==5):
                    addEnemy(ChurchDef,ChurchFast,ChurchShoot,ChurchLarge,bulletColorEnemy)
                elif(level ==6):
                    addEnemy(KFCDef,KFCFast,KFCShoot,KFCLarge,bulletColorEnemy)
                elif(level ==7):
                    addEnemy(ChickDef,ChickFast,ChickShoot,ChickLarge,bulletColorEnemy)
                enemies-=1
                
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                gameEnd = True
                os._exit(1)
            if (event.type ==pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    gameEnd = True
                    os._exit(1)
                #Todd's 4 directional movement engaged
                if(Todd.alive):
                    if (event.key == pygame.K_w):
                        Todd.movement("up",True)
                    if (event.key == pygame.K_a):
                        Todd.movement("left",True)
                    if (event.key == pygame.K_s):
                        Todd.movement("down",True)
                    if (event.key == pygame.K_d):
                        Todd.movement("right",True)
                #AJ's 4 directional movement engaged
                if(Multiplayer):
                    if(Aj.alive):
                        if (event.key == pygame.K_UP):
                            Aj.movement("up",True)
                        if (event.key == pygame.K_LEFT):
                            Aj.movement("left",True)
                        if (event.key == pygame.K_DOWN):
                            Aj.movement("down",True)
                        if (event.key == pygame.K_RIGHT):
                            Aj.movement("right",True)
                #Todd and AJ's firing (space and enter respectively)
                if(Todd.alive):
                    if event.key == pygame.K_SPACE:
                        Todd.shoot()
                if(Multiplayer):
                    if(Aj.alive):
                        if (event.key == pygame.K_RETURN):
                            Aj.shoot()
            if (event.type==pygame.KEYUP):
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
                    if (event.key == pygame.K_UP):
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
            for player in playerList:
                for direct in player.direction.keys():
                    player.direction[direct]=False
            if(level==2):
                levelCreator(CanesBack,level,Border,SaladDef)
            if(level==3):
                levelCreator(CanesBack,level,Border,PopDef)
            if(level==4):
                levelCreator(CanesBack,level,Border,BBWDef)
            if(level==5):
                levelCreator(CanesBack,level,Border,ChurchDef)
            if(level==6):
                levelCreator(CanesBack,level,Border,KFCDef)
            if(level==7):
                levelCreator(CanesBack,level,Border,ChickDef)
            
            
        for entity in entityDisplayList:
            gameDisplay.blit(entity.image,(entity.xPos,entity.yPos))
            
        collectiveHealth = 0
        for player in playerList:
            for i in range(player.health):
                collectiveHealth += 1
                gameDisplay.blit(hp,(player.healthLocation+i*50,BOTTOMBORDER+10))
        if collectiveHealth <= 0:
            break
        if instakill:
            for enemy in enemyList:
                enemy.remove()
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
global instakill
instakill = True
#TEXT ASSETS, these will never change so are global usage (because screw passing these into every single game window)
global bigText
bigText = pygame.font.SysFont('Arial MS', 90)
global medText
medText = pygame.font.SysFont('Arial MS', 50)
global tinyText
tinyText = pygame.font.SysFont('Arial MS', 25)

#titleScreen()
mainGameLoop()
lose()
