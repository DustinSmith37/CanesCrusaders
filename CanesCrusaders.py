#import the needed modules, pygame is obvious, time for tick speed,
#and os for leaving the game wihtout causing errors
import pygame, time, os
#initialize pygame, its font's and it's music player
pygame.init()
pygame.font.init()
pygame.mixer.init()
#set a variable called FPS that is just the clock function from time
fps = pygame.time.Clock()
#display the pygame window, set it to be 800 by 600 and be fullscreen (when not debugging)
gameDisplay = pygame.display.set_mode((800,600),)#pygame.FULLSCREEN)
#set its name to be Canes Crusaders
pygame.display.set_caption('Canes Crusaders')
#a master list of all entities that need to be displayed, listed in order of importance
entityDisplayList=[]
class Entity():
    #default stats every asset will have, like the file name, position, movement, and size
    def __init__(self,file,xPos=0,yPos=0,xMove=5,yMove=5,xLength=50,yLength=50):
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
    def moveRight(self):
        self.xPos+=self.xMove
    def moveUp(self):
        self.yPos-=self.yMove
    def moveDown(self):
        self.yPos+=self.yMove
    def __str__(self):
        return "{},xPos:{},yPos:{},xMove:{},yMove:{},xLength:{},yLength:{}".format(self.file,self.xPos,self.yPos,self.xMove,self.yMove,self.xLength,self.yLength)
Todd = Entity("ToddPNG.png",xLength=200,yLength=200)
print(entityDisplayList[0])

for i in range(len(entityDisplayList)):
    gameDisplay.blit(entityDisplayList[i].image,(entityDisplayList[i].xPos,entityDisplayList[i].yPos))
    

    
    

def mainGameLoop():
    gameEnd=False
    while not(gameEnd):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    gameEnd = True
                    os._exit(1)
                elif event.type ==pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        gameEnd = True
                        os._exit(1)
        fps.tick(30)
        for i in range(len(entityDisplayList)):
            gameDisplay.blit(entityDisplayList[i].image,(entityDisplayList[i].xPos,entityDisplayList[i].yPos))
        for i in range(len(entityDisplayList)):
            entityDisplayList[i].moveRight()
        pygame.display.flip()
mainGameLoop()

