#SETTINGS VARIABLES, CONTROLS VERY IMPORTANT ASPECTS OF THE GAME
global controls
controls = "keyboard" #either "keyboard" or "console" for running on pi
fullscreen = False #if true, pygame will fullscreen, otherwise 800x500
if (controls == "console"):
    import RPi.GPIO as GPIO
    player1 =[18,19,20,21]
    p1butts = [23,22]
    player2 = [17,16,13,12]
    p2butts = [6,5]
    playersel = [24,25]

    inputs = [24,25,18,19,20,21,22,23,12,13,17,16,6,5]
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(p1butts, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(p2butts, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(playersel, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(player1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(player2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
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
HEIGHT = 500
TOPBORDER = 50
BOTTOMBORDER = HEIGHT-50
if fullscreen:
    gameDisplay = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
else:
    gameDisplay = pygame.display.set_mode((WIDTH,HEIGHT))

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
    def __init__(self,normimage,invimage,bulletSprite,cannonSprite,superBreaker,xPos=0,yPos=TOPBORDER,xMove=7,yMove=5,xLength=50,yLength=50,health=3,healthLocation=5):
        Entity.__init__(self,normimage,xPos,yPos,xMove,yMove,xLength,yLength)
        self.bulletSprite=bulletSprite
        self.cannonSprite=cannonSprite
        self.superBreaker=superBreaker
        self.normimage=normimage
        self.invimage = invimage
        self.health = health
        self.invincibility = 0
        self.specialCooldown = 0
        self.bulletCooldown = 0
        self.bulletnumber = 1
        self.miniFire = 0
        self.direction = {"up":False,"left":False,"down":False,"right":False}
        self.healthLocation = healthLocation
        playerList.append(self)
        self.alive = True
        self.upgrades = {"doubleShoot":False,"doubleDamage":False,"doubleDamage2":False,"fastMove1":False,"fastMove2":False}
        self.specialActive = "shotgun"
        self.specialBought = {"shotgun":True,"laser":False,"minigun":False,"cannon":False,"superbreaker":False,"shield":False}
    def shoot(self):
        self.bulletCooldown = 5
        for i in range(0,self.bulletnumber):
            if(self.upgrades["doubleShoot"]):
                Bullet(image=self.bulletSprite,xPos=self.xPos+self.xLength-35,yPos=self.yPos)
                Bullet(image=self.bulletSprite,xPos=self.xPos+self.xLength-15,yPos=self.yPos)
            else:
                Bullet(image=self.bulletSprite,xPos=self.xPos+self.xLength/2,yPos=self.yPos)
        

    def special(self):
        if(self.specialActive=="shotgun"):
            for i in range(0,self.bulletnumber):
                if(self.upgrades["doubleShoot"]):
                    Bullet(image=self.bulletSprite,xPos=self.xPos+self.xLength-20,yPos=self.yPos)
                    Bullet(image=self.bulletSprite,xPos=self.xPos,yPos=self.yPos)
                    Bullet(image=self.bulletSprite,xPos=self.xPos+self.xLength,yPos=self.yPos)
                    Bullet(image=self.bulletSprite,xPos=self.xPos+self.xLength-30,yPos=self.yPos)
                    Bullet(image=self.bulletSprite,xPos=self.xPos+self.xLength-40,yPos=self.yPos)
                    Bullet(image=self.bulletSprite,xPos=self.xPos+self.xLength-10,yPos=self.yPos)
                else:
                    Bullet(image=self.bulletSprite,xPos=self.xPos+self.xLength-25,yPos=self.yPos)
                    Bullet(image=self.bulletSprite,xPos=self.xPos,yPos=self.yPos)
                    Bullet(image=self.bulletSprite,xPos=self.xPos+self.xLength,yPos=self.yPos)
            self.specialCooldown = 60
        elif(self.specialActive=="laser"):
            fired = 0
            for i in range(0,self.bulletnumber):
                if (self.upgrades["doubleShoot"]):
                    for y in range(self.yPos,TOPBORDER,-10):
                        fired += 2
                        Bullet(image=self.bulletSprite,xPos=self.xPos+self.xLength-35,yPos=y,yMove = 20)
                        Bullet(image=self.bulletSprite,xPos=self.xPos+self.xLength-15,yPos=y,yMove = 20)
                else:
                    for y in range(self.yPos,TOPBORDER,-10):
                        fired +=1
                        Bullet(image=self.bulletSprite,xPos=self.xPos+self.xLength/2,yPos=y,yMove = 20)
            print(fired)
            self.specialCooldown = 60
        elif(self.specialActive=="minigun"):
            for i in range(0,self.bulletnumber):
                if (self.upgrades["doubleShoot"]):
                    self.miniFire+=20
                else:
                    self.miniFire+10
            self.specialCooldown = 90
        elif(self.specialActive=="cannon"):
            CannonBullet(image=self.cannonSprite,radius=self.bulletnumber,xPos=self.xPos+self.xLength/2,yPos=self.yPos,yMove = 10)
            self.specialCooldown = 90
        elif(self.specialActive=="superbreaker"):
            SuperBullet(image=self.superBreaker,damage=self.bulletnumber,xPos=self.xPos,yPos=self.yPos-50,yMove = 5)
            self.specialCooldown = 150
        elif(self.specialActive=="shield"):
            self.invincibility = 60
            self.specialCooldown = 150 
           
    def minigunShoot(self):
        if (self.specialActive=="minigun"):
            if (self.miniFire>0):
                if (self.miniFire%2==0):
                    Bullet(image=self.bulletSprite,xPos=self.xPos+self.xLength/2,yPos=self.yPos,yMove = 20)
                self.miniFire-=1
    def damage(self):
        if(self.invincibility==0 and self.alive):
            self.health-=1
            self.invincibility = 45
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

    def specialtickdown(self):
        self.specialCooldown -= 1
    def bulletTickdown(self):
        self.bulletCooldown-=1
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
        if(self == playerList[0]):
            return "Todd"
        elif(self == playerList[1]):
            return "AJ"

    def remove(self):
        playerList.remove(self)
        entityDisplayList.remove(self)

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
    def __init__(self,image,xPos=0,yPos=TOPBORDER,xMove=5,yMove=1,xLength=100,yLength=100,health=10,direction="right"):
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
        global points
        for enemy in enemyList:
            if (enemy.xPos+enemy.xLength>self.xPos and enemy.xPos<self.xPos):
                if (enemy.yPos+enemy.yLength>self.yPos and enemy.yPos<self.yPos):
                    enemy.damage()
                    self.remove()
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
        if (self.yPos+self.yLength>=BOTTOMBORDER):
                self.remove()   
    def remove(self):
        bulletList.remove(self)
        entityDisplayList.remove(self)
class CannonBullet(Bullet):
    def __init__(self,image,radius = 1,xPos=0,yPos=TOPBORDER,xMove=5,yMove=5,xLength=5,yLength=10):
        Bullet.__init__(self,image,xPos,yPos,xMove,yMove,xLength,yLength)
        self.radius = radius*100
    def hitDetect(self):
        global points
        dead = False
        for enemy in enemyList:
            if (enemy.xPos+enemy.xLength>self.xPos and enemy.xPos<self.xPos):
                if (enemy.yPos+enemy.yLength>self.yPos and enemy.yPos<self.yPos):
                    dead = True
                    enemy.damage()
                    self.remove()
                    points +=10
                    break
        if (dead):
            for enemy in enemyList:
                if (enemy.xPos+enemy.xLength>self.xPos-self.radius and enemy.xPos<self.xPos+self.radius):
                    if (enemy.yPos+enemy.yLength>self.yPos-self.radius and enemy.yPos<self.yPos+self.radius):
                        for i in range(0,3):
                            if (enemy.health > 0):
                                enemy.damage()
                                points +=10
        elif (self.yPos<=TOPBORDER):
            self.remove()
class SuperBullet(Bullet):
    def __init__(self,image,damage,xPos=0,yPos=TOPBORDER,xMove=5,yMove=5,xLength=50,yLength=50):
        Bullet.__init__(self,image,xPos,yPos,xMove,yMove,xLength,yLength)
        self.damage = damage
    def hitDetect(self):
        global points
        for enemy in enemyList:
            if (enemy.xPos+enemy.xLength>self.xPos and enemy.xPos<self.xPos):
                if (enemy.yPos+enemy.yLength>self.yPos and enemy.yPos<self.yPos):
                    for i in range(0,5*self.damage):
                        if (enemy.health)>0:
                            enemy.damage()
                            points +=10
        if (self.yPos<=TOPBORDER):
            self.remove()

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
    jukebox("combat1.mp3")
    if (level == 1):
        Entity(back,xLength=WIDTH,yLength=BOTTOMBORDER-TOPBORDER)
        Entity(border,yPos=0,xLength=WIDTH,yLength=TOPBORDER)
        Entity(border,yPos=BOTTOMBORDER,yLength=HEIGHT-BOTTOMBORDER,xLength=WIDTH)
    else:
        entityDisplayList[0].image = back
    for i in range(0,13):
        Enemy(DefEnemy, xPos=(60*i))

def addEnemy(level,Def,Fast,Shooter,Large,bulletColorEnemy):
    chance = randint(0,30)
    if(chance in [14,15,16,17]):
        speedEnemy(Fast,xPos=0,health = level+level*2)
        Enemy(Def, xPos=0,health = level+1)
    elif(chance in [19,21,22]):
        shootEnemy(Shooter, xPos=0,bulletSprite=bulletColorEnemy,health = level+3)
    elif(chance in [20]):
        tankEnemy(Large,xPos=randint(0,700),health = 10 * level)
        Enemy(Def,xPos=0,health=level+1)
    else:
        Enemy(Def, xPos=0,health=level+1)

def purchase(buyer,buyerX,buyerY):
    global points
    buyGrid=[{"doubleShoot":250,"doubleDamage":500,"doubleDamage2":1000,"fastMove1":2000,"fastMove2":500,"heal":100},{"shotgun":0, "laser":250, "cannon":250, "superbreaker":250, "minigun":250, "shield":250}]
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
        if (upgrade == "heal" or buyer.upgrades[upgrade]==False):
            if points >= buyGrid[0][upgrade]:
                if (upgrade == "heal"):
                    buyer.heal()
                    points -= buyGrid[0]["heal"]
                    status = "You have healed! Well done!"
                elif(upgrade=="doubleDamage"):
                    buyer.bulletnumber*=2
                    buyer.upgrades["doubleDamage"]=True

                    points-=buyGrid[0]["doubleDamage"]
                    status = "You now deal double damage, {}.".format(buyer)
                elif(upgrade=="doubleDamage2"):
                    buyer.upgrades["doubleDamage2"]=True
                    buyer.bulletnumber*=2
                    points-=buyGrid[0]["doubleDamage"]
                    status = "You now deal double damage again, {}.".format(buyer)
                elif(upgrade =="doubleShoot"):
                    buyer.upgrades["doubleShoot"]=True
                    points -=buyGrid[0]["doubleShoot"]
                    status = "You now fire twice as many bullets, {}!".format(buyer)

                elif(upgrade == "fastMove"):
                    buyer.upgrades["fastMove"]=True
                    buyer.xMove = buyer.xMove *2
                    points -= buyGrid[0]["fastMove"]
                    status = "You have purchased double horizontal speed, {}!".format(buyer)
                elif(upgrade =="fastMove2"):
                    buyer.upgrades["fastMove2"]=True
                    buyer.yMove = buyer.yMove *2
                    points -= buyGrid[0]["fastMove2"]
                    status = "You have purchased double vertical speed, {}!".format(buyer)
                    
                else:

                    points -= buyGrid[0][upgrade]
                    buyer.upgrades[upgrade]=True
                    status = "You have bought an upgrade! Well done!"
            else:
                status = "You do not have enough points!"
        else:
            status = "You've already bought this upgrade!"
    elif special != None:
        if buyer.specialBought[special]==True:
                buyer.specialActive = special
                status = "You have swapped your active special to {}!".format(special)
        elif points >= buyGrid[1][special]:
            if buyer.specialBought[special] ==False:
                points -= buyGrid[1][special]
                buyer.specialBought[special]=True
                buyer.specialActive = special
                status = "You have bought {}!".format(special)
            
        else:
            status = "You do not have enough points!"
    return status
def jukebox(song,start=0.0):
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(-1, start)
def titleScreen():
    #assets for title screen
    global Multiplayer
    global points
    points = 0
    background = pygame.transform.scale(pygame.image.load("SpaceBack.jpg"),(WIDTH,HEIGHT))
    guide2 = pygame.transform.scale(pygame.image.load("GUIDE.png"),(WIDTH-200,HEIGHT-100))
    toddTitle = pygame.transform.scale(pygame.image.load("ToddPNG.png"),(200,200))
    ajTitle = pygame.transform.scale(pygame.image.load("AJPNG.png"),(200,200))
    coolCane = pygame.transform.flip(pygame.image.load("CoolCanePNG.png"),1,0)
    gameStart = False
    stage = "start"
    inputCooldown = 0
    jukebox("menu1.mp3")
    while(not gameStart):
        if (controls == "console"):
            for i in range(len(inputs)):
                if (inputCooldown == 0):
                    if(GPIO.input(inputs[i])):
                        inputCooldown=15
                        if (GPIO.input(inputs[0]) and GPIO.input(inputs[1])):
                            pygame.quit()
                            gameEnd = True
                            os._exit(1)
                        if ((GPIO.input(inputs[7]) or GPIO.input(inputs[12])) and (stage == "guide2")):
                            if (Multiplayer):
                                stage = "meet2"
                            else:
                                stage = "meet1"
                        if ((GPIO.input(inputs[6]) or GPIO.input(inputs[13]))and(stage == "meet1" or stage == "meet2")):
                            gameStart = True
                        if(GPIO.input(inputs[0])):
                            stage = "guide1"
                            Multiplayer = False
                        elif(GPIO.input(inputs[1])):
                            stage = "guide1"
                            Multiplayer = True
                        elif((GPIO.input(inputs[7]) or GPIO.input(inputs[12])) and (stage == "guide1")):
                            stage = "guide2"
        if (controls == "keyboard"):
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    gameStart = True
                    os._exit(1)
                elif event.type == pygame.KEYDOWN:
                    if ((event.key == pygame.K_RETURN or event.key == pygame.K_SPACE) and (stage == "guide2")):
                        if (Multiplayer):
                            stage = "meet2"
                        else:
                            stage = "meet1"
                    if ((event.key == pygame.K_e or event.key == pygame.K_BACKSLASH)and(stage == "meet1" or stage == "meet2")):
                        gameStart = True
                    if (event.key == pygame.K_1):
                        stage = "guide1"
                        Multiplayer = False
                    elif (event.key == pygame.K_2):
                        stage = "guide1"
                        Multiplayer = True
                    elif (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE) and (stage =="guide1"):
                        stage = "guide2"
        gameDisplay.blit(background,(0,0))
        if (inputCooldown>0):
            inputCooldown-=1
        if (stage == "start"):
            line1 = bigText.render("CANES CRUSADERS",True,(255,255,255))
            gameDisplay.blit(line1,(100,75))
            line2 = medText.render("THE GREAT CHICKEN WARS",True,(255,0,0))
            gameDisplay.blit(line2,(160,160))
            gameDisplay.blit(toddTitle,(200,350))
            gameDisplay.blit(coolCane,(350,300))
            line2 = medText.render("SELECT NUMBER OF PLAYERS TO CONTINUE",True,(255,0,0))
            gameDisplay.blit(line2,(15,210))

        if (stage == "meet2"):
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
            line8 = medText.render("PRESS SPECIAL TO CONTINUE",True,(255,0,0))
            gameDisplay.blit(line8,(130,120))
            gameDisplay.blit(toddTitle,(100,400))
            gameDisplay.blit(ajTitle,(500,400))
        
        if (stage == "meet1"):
            line1 = bigText.render("MEET YOUR HERO",True,(255,255,255))
            gameDisplay.blit(line1,(120,50))
            line2 = medText.render("TODD GRAVES",True,(255,255,255))
            gameDisplay.blit(line2,(280,200))
            line3 = medText.render("GOD KING OF",True,(255,255,255))
            gameDisplay.blit(line3,(300,250))
            line6 = medText.render("PRESS SPECIAL TO CONTINUE",True,(255,0,0))
            gameDisplay.blit(line6,(130,120))
            line7 = medText.render("MANKIND",True,(255,255,255))
            gameDisplay.blit(line7,(310,300))
            gameDisplay.blit(toddTitle,(300,350))
        if (stage == "guide1"):
            line1=bigText.render("HOW TO PLAY",True,(255,255,255))
            line2=medText.render("THE RED BUTTON IS SHOOT/FIRE",True,(255,0,0))
            line3=medText.render("THE BLACK BUTTON IS SPECIAL",True,(255,255,255))
            line4=medText.render("THE WHITE BUTTONS ARE PLAYER SELECT",True,(255,255,255))
            line5=medText.render("PRESSING BOTH WHITE CLOSES THE GAME",True,(255,255,255))
            line6=medText.render("PRESS FIRE TO CONTINUE",True,(255,0,0))
            gameDisplay.blit(line1,(120,50))
            gameDisplay.blit(line2,(120,150))
            gameDisplay.blit(line3,(120,200))
            gameDisplay.blit(line4,(30,250))
            gameDisplay.blit(line5,(30,300))
            gameDisplay.blit(line6,(150,350))


        if (stage == "guide2"):
            line1 = bigText.render("HOW TO PLAY CONT",True,(255,255,255))
            line2 = tinyText.render("PRESS FIRE TO CONTINUE",True,(255,0,0))
            gameDisplay.blit(line1,(100,50))
            gameDisplay.blit(guide2,(100,100))
            gameDisplay.blit(line2,(450,475))
            
        pygame.display.update()
        fps.tick(30)
    mainGameLoop()
def cutscene(scene):
    sceneStage = 1
    Todd = pygame.transform.scale(pygame.image.load("ToddPNG.png"),(200,200))
    Aj = pygame.transform.scale(pygame.image.load("AJPNG.png"),(200,200))
    SpaceBack = pygame.transform.scale(pygame.image.load("SpaceBack.jpg"),(WIDTH,BOTTOMBORDER-TOPBORDER))
    shopFront = pygame.transform.scale(pygame.image.load("StoreBack.png"),(WIDTH,BOTTOMBORDER-TOPBORDER))
    CoolCane = pygame.transform.scale(pygame.image.load("CoolCanePNG.png"),(200,200))
    TextBack = pygame.transform.scale(pygame.image.load("WhiteBorder.jpeg"),(WIDTH,100))
    Border = pygame.transform.scale(pygame.image.load("black.png"),(WIDTH,50))
    Inform = medText.render("PRESS PLAYER SELECT TO CONTINUE",True,(255,255,255))
    BabyCane = pygame.transform.scale(pygame.image.load("BabyCane.png"),(200,200))
    showtime = True
    inputCooldown = 0
    if (scene == "shop"):
        jukebox("menu1.mp3")
    elif (scene == "lose"):
        jukebox("death1.mp3")
    elif (scene == "levelEnd"):
        jukebox("bossIntro.mp3")
    while showtime:
        if (controls == "console"):
            for i in range(len(inputs)):
                if(GPIO.input(inputs[i])):
                    if (GPIO.input(inputs[0]) and GPIO.input(inputs[1])):
                        pygame.quit()
                        showtime = False
                        os._exit(1)
                    if (inputCooldown==0):
                        if (GPIO.input(inputs[0]) or GPIO.input(inputs[1])):
                            inputCooldown = 5
                            sceneStage +=1
        if (controls == "keyboard"):
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    showtime = False
                    os._exit(1)
                if (event.type ==pygame.KEYDOWN):
                    if (event.key == pygame.K_ESCAPE):
                        pygame.quit()
                        showtime = False
                        os._exit(1)
                    if (event.key == pygame.K_1 or event.key == pygame.K_2):
                        sceneStage+=1
        fps.tick(10)
        if (inputCooldown>0):
            inputCooldown-=1
        gameDisplay.blit(Border,(0,0))
        gameDisplay.blit(Border,(0,BOTTOMBORDER))
        gameDisplay.blit(Inform,(60,15))
        if (scene == "shop"):
            gameDisplay.blit(shopFront,(0,TOPBORDER))
            if (sceneStage == 1):
                gameDisplay.blit(Todd,(0,200))
                gameDisplay.blit(TextBack,(0,400))
                line1=medText.render("Todd: What is this place?",True,(0,0,0))
                gameDisplay.blit(line1,(25,425))
            if (sceneStage ==2):
                gameDisplay.blit(Todd,(0,200))
                gameDisplay.blit(TextBack,(0,400))
                gameDisplay.blit(CoolCane,(650,200))
                line1=medText.render("???: Oh, Todd, great to see you!",True,(0,0,0))
                gameDisplay.blit(line1,(25,425))
            if (sceneStage ==3):
                gameDisplay.blit(Todd,(0,200))
                gameDisplay.blit(TextBack,(0,400))
                gameDisplay.blit(CoolCane,(650,200))
                line1=medText.render("RC1: I'm Raising Cane the first,",True,(0,0,0))
                gameDisplay.blit(line1,(25,425))
            if (sceneStage ==4):
                gameDisplay.blit(Todd,(0,200))
                gameDisplay.blit(TextBack,(0,400))
                gameDisplay.blit(CoolCane,(650,200))
                line1=medText.render("RC1: and welcome to my shop!",True,(0,0,0))
                gameDisplay.blit(line1,(25,425))
            if (sceneStage ==5):
                gameDisplay.blit(Todd,(0,200))
                gameDisplay.blit(TextBack,(0,400))
                gameDisplay.blit(CoolCane,(650,200))
                line1=medText.render("RC1: I'm here to help you in your journey!",True,(0,0,0))
                gameDisplay.blit(line1,(25,425))
            if (sceneStage ==6):
                gameDisplay.blit(Todd,(0,200))
                gameDisplay.blit(TextBack,(0,400))
                gameDisplay.blit(CoolCane,(650,200))
                line1=medText.render("Todd: So, uh, why am I fighting these guys?",True,(0,0,0))
                gameDisplay.blit(line1,(25,425))
            if (sceneStage ==7):
                gameDisplay.blit(Todd,(0,200))
                gameDisplay.blit(TextBack,(0,400))
                gameDisplay.blit(CoolCane,(650,200))
                line1=medText.render("RC1: They are the evil chicken lords!",True,(0,0,0))
                gameDisplay.blit(line1,(25,425))
            if (sceneStage ==8):
                gameDisplay.blit(Todd,(0,200))
                gameDisplay.blit(TextBack,(0,400))
                gameDisplay.blit(CoolCane,(650,200))
                line1=medText.render("RC1: They despise your awesome chicken!",True,(0,0,0))
                gameDisplay.blit(line1,(25,425))
            if (sceneStage ==9):
                gameDisplay.blit(Todd,(0,200))
                gameDisplay.blit(TextBack,(0,400))
                gameDisplay.blit(CoolCane,(650,200))
                line1=medText.render("RC1: The spirits of the Canes have united,",True,(0,0,0))
                gameDisplay.blit(line1,(25,425))
            if (sceneStage ==10):
                gameDisplay.blit(Todd,(0,200))
                gameDisplay.blit(TextBack,(0,400))
                gameDisplay.blit(CoolCane,(650,200))
                line1=medText.render("RC1: in order to help you defeat them!",True,(0,0,0))
                gameDisplay.blit(line1,(25,425))
            if (sceneStage ==11):
                gameDisplay.blit(Todd,(0,200))
                gameDisplay.blit(TextBack,(0,400))
                gameDisplay.blit(CoolCane,(650,200))
                line1=medText.render("Todd: Dope! Lemme see what you got!",True,(0,0,0))
                gameDisplay.blit(line1,(25,425))
            if (sceneStage ==12):
                showtime=False
        elif (scene == "levelEnd"):
            gameDisplay.blit(SpaceBack,(0,TOPBORDER))
            if (sceneStage == 1):
                line1=bigText.render("LEVEL COMPLETE",True,(255,255,255))
                gameDisplay.blit(line1,(125,TOPBORDER+100))
            elif (sceneStage ==2):
                line1=bigText.render("LEVEL COMPLETE",True,(255,255,255))
                gameDisplay.blit(line1,(125,TOPBORDER+100))
                showtime = False
        elif (scene == "lose"):
            gameDisplay.blit(SpaceBack,(0,TOPBORDER))
            if (sceneStage == 1):
                gameDisplay.blit(TextBack,(0,400))
                gameDisplay.blit(BabyCane,(300,200))
                line1=medText.render("RC3: You have been defeated, Todd.",True,(0,0,0))
                gameDisplay.blit(line1,(25,425))
            elif (sceneStage == 2):
                gameDisplay.blit(TextBack,(0,400))
                gameDisplay.blit(BabyCane,(300,200))
                line1=medText.render("RC3: I cannot resurrect you, not again.",True,(0,0,0))
                gameDisplay.blit(line1,(25,425))
            elif (sceneStage == 3):
                gameDisplay.blit(TextBack,(0,400))
                gameDisplay.blit(BabyCane,(300,200))
                line1=medText.render("RC3: There is, however, another way.",True,(0,0,0))
                gameDisplay.blit(line1,(25,425))
            elif (sceneStage == 4):
                gameDisplay.blit(TextBack,(0,400))
                gameDisplay.blit(BabyCane,(300,200))
                line1=medText.render("RC3: A new timeline. One not yet doomed.",True,(0,0,0))
                gameDisplay.blit(line1,(25,425))
            elif (sceneStage == 5):
                gameDisplay.blit(TextBack,(0,400))
                gameDisplay.blit(BabyCane,(300,200))
                line1=medText.render("RC3: I will use all my strength to send you.",True,(0,0,0))
                gameDisplay.blit(line1,(25,425))
            elif (sceneStage == 6):
                gameDisplay.blit(TextBack,(0,400))
                gameDisplay.blit(BabyCane,(300,200))
                line1=medText.render("RC3: Please Todd, you are our only hope.",True,(0,0,0))
                gameDisplay.blit(line1,(25,425))
            elif (sceneStage ==7):
                showtime = False
        pygame.display.flip()
def shop():
    ToddShop = pygame.transform.scale(pygame.image.load("ToddPNG.png"),(50,50))
    AjShop = pygame.transform.scale(pygame.image.load("AJPNG.png"),(50,50))
    hp = pygame.transform.scale(pygame.image.load("Cane Heart.png"),(30,30))
    shopFront = pygame.transform.scale(pygame.image.load("StoreBack.png"),(WIDTH,BOTTOMBORDER-TOPBORDER))
    CoolCane = pygame.transform.scale(pygame.image.load("CoolCanePNG.png"),(100,100))
    TextBack = pygame.transform.scale(pygame.image.load("WhiteBorder.jpeg"),(500,100))
    Border = pygame.transform.scale(pygame.image.load("black.png"),(WIDTH,50))
    DoubleDamage = pygame.transform.scale(pygame.image.load("DoubleDamage.png"),(75,75))
    DoubleBullet = pygame.transform.scale(pygame.image.load("DoubleTap.png"),(75,75))
    DoubleSpeed = pygame.transform.scale(pygame.image.load("X2speed.png"),(75,75))
    ShotPower = pygame.transform.scale(pygame.image.load("Shotgun.png"),(100,50))
    LaserPower = pygame.transform.scale(pygame.image.load("Laser.png"),(100,50))
    Shield = pygame.transform.scale(pygame.image.load("Shield.png"),(75,75))
    Minigun = pygame.transform.scale(pygame.image.load("Minigun.png"),(75,75))
    SBreaker = pygame.transform.scale(pygame.image.load("SBreaker.png"),(75,75))
    Cannon = pygame.transform.scale(pygame.image.load("Cannon.png"),(75,75))
    Heal = pygame.transform.scale(pygame.image.load("Cane Heart.png"),(75,75))
    upgradeText = tinyText.render("Upgrades",True,(255,255,255))
    specialText = tinyText.render("Specials",True,(255,255,255))
    levelDisplay = medText.render("Level: Shop",True,(255,255,255))
    ToddPos = {"xPos":0,"yPos":0}
    AjPos = {"xPos":0,"yPos":0}
    shopping = True
    global points
    points = points
    status = "What would you like to buy?"
    ToddBuyCooldown = 0
    AjBuyCooldown = 0
    noSkip = 30
    
    if (level == 1):
        cutscene("shop")
    songSelect = randint(1,11)
    if (songSelect>=1 and songSelect <=5):
        jukebox("shop1.mp3")
    elif (songSelect>=6 and songSelect <=10):
        jukebox("shop2.mp3")
    elif (songSelect>10):
        jukebox("shopRare.mp3")
    while(shopping):
        gameDisplay.blit(shopFront,(0,TOPBORDER))
        gameDisplay.blit(Border,(0,0))
        gameDisplay.blit(Border,(0,BOTTOMBORDER))
        gameDisplay.blit(TextBack,(300,TOPBORDER))
        pointDisplay = medText.render("Points: "+str(points),True,(255,255,255))
        gameDisplay.blit(pointDisplay, (590,10))
        gameDisplay.blit(levelDisplay, (10,10))
        gameDisplay.blit(upgradeText,(0,225))
        gameDisplay.blit(specialText,(0,375))
        gameDisplay.blit(Heal,(710,200))
        gameDisplay.blit(DoubleBullet,(90,200))
        gameDisplay.blit(DoubleDamage,(220,200))
        gameDisplay.blit(DoubleDamage,(340,200))
        gameDisplay.blit(DoubleSpeed,(465,200))
        gameDisplay.blit(DoubleSpeed,(590,200))
        gameDisplay.blit(ShotPower,(80,375))
        gameDisplay.blit(LaserPower,(210,375))
        gameDisplay.blit(CoolCane,(200,TOPBORDER))
        gameDisplay.blit(Shield,(710,350))
        gameDisplay.blit(Minigun,(590,350))
        gameDisplay.blit(Cannon,(340,350))
        gameDisplay.blit(SBreaker,(465,350))
        if (controls == "console"):
            for i in range(len(inputs)):
                if(GPIO.input(inputs[i])):
                    if (GPIO.input(inputs[0]) and GPIO.input(inputs[1])):
                        pygame.quit()
                        shopping = False
                        os._exit(1)
                    if (noSkip==0):
                        if (GPIO.input(inputs[0]) or GPIO.input(inputs[1])):
                            shopping  = False
                    #Todd's selection
                    if (GPIO.input(inputs[4])):
                        if (ToddPos["xPos"] >0):
                            ToddPos["xPos"] -= 1
                    if (GPIO.input(inputs[5])):
                        if (ToddPos["xPos"]<5):
                            ToddPos["xPos"] += 1
                    if (GPIO.input(inputs[2])):
                        if (ToddPos["yPos"] >0):
                            ToddPos["yPos"] -= 1
                    if (GPIO.input(inputs[3])):
                        if (ToddPos["yPos"]<1):
                            ToddPos["yPos"] += 1
                        
                    #AJ's selection
                    if(Multiplayer):
                        if (GPIO.input(inputs[9])):
                            if (AjPos["xPos"] >0):
                                AjPos["xPos"] -= 1
                        if (GPIO.input(inputs[8])):
                            if (AjPos["xPos"]<5):
                                AjPos["xPos"] += 1
                        if (GPIO.input(inputs[10])):
                            if (AjPos["yPos"] >0):
                                AjPos["yPos"] -= 1
                        if (GPIO.input(inputs[11])):
                            if (AjPos["yPos"]<1):
                                AjPos["yPos"] += 1
                    #Todd and AJ's firing (space and enter respectively)
                    if (ToddBuyCooldown == 0):
                        if (GPIO.input(inputs[7])):
                            ToddBuyCooldown = 5
                            status = purchase(playerList[0],ToddPos["xPos"],ToddPos["yPos"])
                    if(Multiplayer):
                        if(AjBuyCooldown == 0):
                            if (GPIO.input(inputs[12])):
                                AjBuyCooldown = 5
                                status = purchase(playerList[1],AjPos["xPos"],AjPos["yPos"])
        if (controls == "keyboard"):
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
                    if (noSkip == 0):
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
                
                    if (event.key == pygame.K_SPACE):
                        status = purchase(playerList[0],ToddPos["xPos"],ToddPos["yPos"])
                    if(Multiplayer):
                        if (event.key == pygame.K_RETURN):
                            status = purchase(playerList[1],AjPos["xPos"],AjPos["yPos"])
        fps.tick(15)
        gameDisplay.blit(ToddShop,(ToddPos["xPos"]*125+75,ToddPos["yPos"]*100+300))
        if Multiplayer:
            gameDisplay.blit(AjShop,(AjPos["xPos"]*125+130,AjPos["yPos"]*100+300))
        if (ToddBuyCooldown>0):
            ToddBuyCooldown-=1
        if (AjBuyCooldown>0):
            AjBuyCooldown-=1
        if (noSkip > 0):
            noSkip -=1
        RCMessage = tinyText.render("RC: "+str(status),True,(0,0,0))
        gameDisplay.blit(RCMessage,(320,100))
        for player in playerList:
            lives = medText.render("x {}".format(player.health),True,(255,255,255))
            if (controls == "console"):
                gameDisplay.blit(hp,(player.healthLocation,BOTTOMBORDER))
                gameDisplay.blit(lives,(player.healthLocation+30,BOTTOMBORDER))
            elif (controls == "keyboard"):
                gameDisplay.blit(hp,(player.healthLocation,BOTTOMBORDER+10))
                gameDisplay.blit(lives,(player.healthLocation+30,BOTTOMBORDER+10))
        pygame.display.flip()
def lose():
    global points
    for shooter in range(len(shootList)):
        shootList[0].remove()
    for enemy in range(len(enemyList)):
        enemyList[0].remove()
    for player in range(len(playerList)):
        playerList[0].remove()
    for bullet in range(len(bulletList)):
        bulletList[0].remove()
    for entity in range(len(entityDisplayList)):
        entityDisplayList[0].remove()

    background = pygame.transform.scale(pygame.image.load("SpaceBack.jpg"),(WIDTH,HEIGHT))
    gameOver = bigText.render("Game Over",True,(255,255,255))
    score = medText.render("Your score: {}".format(points),True,(255,255,255))
    inform = medText.render("Press fire to continue",True,(255,0,0))
    inputCooldown = 5
    action = False
    while(not action):
        gameDisplay.blit(background,(0,0))
        gameDisplay.blit(gameOver,(200,200))
        gameDisplay.blit(score,(260,300))
        gameDisplay.blit(inform,(200,350))
        if (controls == "console"):
            for i in range(len(inputs)):
                if(GPIO.input(inputs[i])):
                    if (GPIO.input(inputs[0]) and GPIO.input(inputs[1])):
                        pygame.quit()
                        action = True
                        os._exit(1)
                        return False
                    if (inputCooldown == 0):
                        if(GPIO.input(inputs[7]) or GPIO.input(inputs[12])):
                            action = True
                            points = 0
        if (controls == "keyboard"):
            for event in pygame.event.get():
                    if (event.type == pygame.QUIT):
                        pygame.quit()
                        action = True
                        os._exit(1)
                        return False
                    if (event.type ==pygame.KEYDOWN):
                        if (event.key == pygame.K_ESCAPE):
                            pygame.quit()
                            action = True
                            os._exit(1)
                            return False
                        if(event.key == pygame.K_SPACE or event.key ==pygame.K_RETURN):
                            action = True
        pygame.display.flip()
        fps.tick(15)
        if (inputCooldown>0):
            inputCooldown-=1
    titleScreen()
                    
def mainGameLoop():
    global points
    global difficulty
    gameEnd=False
    topClear = False
    enemies = 13
    #Bullet Sprites
    bulletColorEnemy=pygame.transform.scale(pygame.image.load("toast.png"),(30,45))
    bulletColorTodd=pygame.transform.scale(pygame.image.load("Finger.png"),(20,30))
    bulletColorAj=pygame.transform.scale(pygame.image.load("Fries.png"),(20,30))
    bulletColorCannon=pygame.transform.scale(pygame.image.load("SpicyFinger.png"),(20,30))
    bulletColorSuper=pygame.transform.scale(pygame.image.load("Finger.png"),(50,50))
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
    ToddShield = pygame.transform.scale(pygame.image.load("ToddShield.png"),(50,50))
    AjPng = pygame.transform.scale(pygame.image.load("AJPNG.png"),(50,50))
    AjShield = pygame.transform.scale(pygame.image.load("AJShield.png"),(50,50))
    hp = pygame.transform.scale(pygame.image.load("Cane Heart.png"),(30,30))
    Todd = Player(ToddPng, ToddShield, xLength=50,yLength=50,xPos=200,yPos=400,bulletSprite=bulletColorTodd,cannonSprite=bulletColorCannon,superBreaker=bulletColorSuper)
    if(Multiplayer):
        Aj = Player(AjPng, AjShield, xLength=50,yLength=50,xPos=600,yPos=400, healthLocation=500,bulletSprite=bulletColorAj,cannonSprite=bulletColorCannon,superBreaker=bulletColorSuper)
    



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
                    addEnemy(level,ZaxbyDef,ZaxbyFast,ZaxbyShoot,ZaxbyLarge,bulletColorEnemy)
                elif(level ==2):
                    addEnemy(level,SaladDef,SaladFast,SaladShoot,SaladLarge,bulletColorEnemy)
                elif(level ==3):
                    addEnemy(level,PopDef,PopFast,PopShoot,PopLarge,bulletColorEnemy)
                elif(level ==4):
                    addEnemy(level,BBWDef,BBWFast,BBWShoot,BBWLarge,bulletColorEnemy)
                elif(level ==5):
                    addEnemy(level,ChurchDef,ChurchFast,ChurchShoot,ChurchLarge,bulletColorEnemy)
                elif(level ==6):
                    addEnemy(level,KFCDef,KFCFast,KFCShoot,KFCLarge,bulletColorEnemy)
                elif(level ==7):
                    addEnemy(level,ChickDef,ChickFast,ChickShoot,ChickLarge,bulletColorEnemy)
                enemies-=1
        if (controls == "console"):
            for i in range(len(inputs)):
                
                if(GPIO.input(inputs[i])):
                    if (GPIO.input(inputs[0]) and GPIO.input(inputs[1])):
                        pygame.quit()
                        gameEnd = True
                        os._exit(1)
                    #Todd's 4 directional movement engaged
                    if(Todd.alive):
                        if (GPIO.input(inputs[2])):
                            Todd.movement("up",True)
                        else:
                            Todd.movement("up",False)
                        if (GPIO.input(inputs[4])):
                            Todd.movement("left",True)
                        else:
                            Todd.movement("left",False)
                        if (GPIO.input(inputs[3])):
                            Todd.movement("down",True)
                        else:
                            Todd.movement("down",False)
                        if (GPIO.input(inputs[5])):
                            Todd.movement("right",True)
                        else:
                            Todd.movement("right",False)
                    #AJ's 4 directional movement engaged
                    if(Multiplayer):
                        if(Aj.alive):
                            if (GPIO.input(inputs[10])):
                                Aj.movement("up",True)
                            else:
                                Aj.movement("up",False)
                            if (GPIO.input(inputs[9])):
                                Aj.movement("left",True)
                            else:
                                Aj.movement("left",False)
                            if (GPIO.input(inputs[11])):
                                Aj.movement("down",True)
                            else:
                                Aj.movement("down",False)
                            if (GPIO.input(inputs[8])):
                                Aj.movement("right",True)
                            else:
                                Aj.movement("right",False)
                    
                    #Todd and AJ's firing (space and enter respectively)
                    if(Todd.alive):
                        if (GPIO.input(inputs[7])):
                            if(Todd.bulletCooldown == 0):
                                Todd.shoot()
                        if(Todd.specialCooldown == 0):
                            if (GPIO.input(inputs[6])):
                                Todd.special()
                    if(Multiplayer):
                        if(Aj.alive):
                            if (GPIO.input(inputs[12])):
                                if(Aj.bulletCooldown == 0):
                                    Aj.shoot()
                            if(Aj.specialCooldown == 0):
                                if(GPIO.input(inputs[13])):
                                    Aj.special()   
            
        # for keyboard inputs    
        if (controls == "keyboard"): 
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
                        if (event.key == pygame.K_SPACE):
                            Todd.shoot()
                        if(Todd.specialCooldown == 0):
                            if (event.key == pygame.K_e):
                                Todd.special()
                    if(Multiplayer):
                        if(Aj.alive):
                            if (event.key == pygame.K_RETURN):
                                Aj.shoot()
                            if(Aj.specialCooldown == 0):
                                if(event.key == pygame.K_BACKSLASH):
                                    Aj.special()
                    
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
        for enemy in shootList:
            shootEnemy.fire(enemy)
        if enemyList == []:
            for bullet in range(len(bulletList)):
                bulletList[0].remove()
            cutscene("levelEnd")
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
        for player in playerList:
            if(player.specialCooldown):
                player.specialtickdown()
            if(player.invincibility>0):
                player.tickdown()
            if(player.bulletCooldown>0):
                player.bulletTickdown()
            if (player.invincibility>0):
                player.image=player.invimage
            else:
                player.image=player.normimage
            player.hitDetect()
            player.minigunShoot()
            
        for entity in entityDisplayList:
            gameDisplay.blit(entity.image,(entity.xPos,entity.yPos))
            
        collectiveHealth = 0
        for player in playerList:
            collectiveHealth += player.health
            lives = medText.render("x {}".format(player.health),True,(255,255,255))
            if (controls == "console"):
                gameDisplay.blit(hp,(player.healthLocation,BOTTOMBORDER))
                gameDisplay.blit(lives,(player.healthLocation+30,BOTTOMBORDER))
            elif (controls == "keyboard"):
                gameDisplay.blit(hp,(player.healthLocation,BOTTOMBORDER+10))
                gameDisplay.blit(lives,(player.healthLocation+30,BOTTOMBORDER+10))
        if collectiveHealth <= 0:
            cutscene("lose")
            lose()
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
instakill = False
#TEXT ASSETS, these will never change so are global usage (because screw passing these into every single game window)
global bigText
bigText = pygame.font.SysFont('Arial MS', 90)
global medText
medText = pygame.font.SysFont('Arial MS', 50)
global tinyText
tinyText = pygame.font.SysFont('Arial MS', 25)

titleScreen()
