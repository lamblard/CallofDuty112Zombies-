"""

15-112 Term Project: Call of Duty: 112 - Zombies 
    
Name: Luca Amblard
Andrew ID: lamblard
Section: D
   
"""

import pygame
import random
import copy

# I learned basic pygame from Lukas Peraza's website
# http://blog.lukasperaza.com/getting-started-with-pygame/

# Pygame syntax learned from the pygame website
# https://www.pygame.org/docs/ref/sprite.html
# https://www.pygame.org/docs/ref/mixer.html

# Other citations are located next to code

# PygameGame class below from
# https://github.com/LBPeraza/Pygame-Asteroids/blob/master/pygamegame.py

class PygameGame(object):
    
    def init(self):
        pass
    
    def mousePressed(self, x, y):
        pass
    
    def mouseReleased(self, x, y):
        pass
    
    def mouseMotion(self, x, y):
        pass
    
    def mouseDrag(self, x, y):
        pass
    
    def keyPressed(self, keyCode, modifier):
        pass
    
    def keyReleased(self, keyCode, modifier):
        pass
    
    def timerFired(self, dt):
        pass
    
    def redrawAll(self, screen):
        pass
    
    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)
    
    def __init__(self, width=600, height=400, fps=200, title
        ="Call of Duty: 112 - Zombies"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()
    
    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)
        
        # stores all the keys currently being held down
        self._keys = dict()
        
        # call game-specific initialization
        self.init()
        self.playing = True
        while self.playing:
            time = clock.tick(self.fps)
            
            self.timerFired(time)
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
               
                elif event.type == pygame.QUIT:
                    self.playing = False     
             
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()

# TA Nikolai Lenney advised me to use the Game and Mode classes below
# He explained to me how these classes would work but I wrote both classes 
# on my own

class Game(PygameGame):
    def __init__(self, width, height):
        self.width, self.height = width, height
        super().__init__(self.width, self.height)
        self.mode = StartGame(self) 
        
    def init(self):
        self.mode.init()

    def mousePressed(self, x, y):
        self.mode.mousePressed(x, y)

    def keyPressed(self, keyCode, modifier):
        self.mode.keyPressed(keyCode, modifier)
    
    def keyReleased(self, keyCode, modifier):
        self.mode.keyReleased(keyCode, modifier)
    
    def timerFired(self, dt):
        self.mode.timerFired(dt)

    def redrawAll(self, screen):
        self.mode.redrawAll(screen)
    

class Mode(object):
    def __init__(self, game):
        self.game = game
 

class StartGame(Mode):
    def __init__(self, game):
        super().__init__(game)
        self.width, self.height = self.game.width, self.game.height

    def init(self):
        w, h = self.width, self.height
        self.mode = "Start"
        # rects of the different buttons
        incr = 40
        self.playBot = (w*0.1, h*0.8, 160, 45) 
        self.instBot = (w*0.25+incr, h*0.8, 160, 45)
        self.backBot = (w*(56/135), h*0.9, 160, 45)
        self.soloBot = (w*0.1, h*0.8, 160, 45)
        self.coopBot = (w*0.25, h*0.8, 160, 45)
        size = 100
        self.font = pygame.font.SysFont(None, size, True)
        # click sound from http://soundbible.com/1705-Click2.html
        self.click = pygame.mixer.Sound("click.wav")
        self.loadImages()
        
    def loadImages(self):
        self.loadBackgroundImage()
        self.loadStartScreenCoDImage()
        self.loadStartScreenZombiesImage()
        self.loadPlayBottonImage()
        self.loadInstructionsBottonImage()
        self.loadBackBottonImage()
        self.loadSoloBottonImage()
        self.loadCoopBottonImage()
        self.loadInstructionsImage()

    def getCoords(self, bot):
        x0, y0 = bot[0], bot[1]
        x1, y1 = (x0 + bot[2]), (y0 + bot[-1])
        return x0, y0, x1, y1

    def mousePressed(self, x, y):
        
        if (self.mode == "Start"):
            playX0, playY0, playX1, playY1 = self.getCoords(self.playBot)
            instX0, instY0, instX1, instY1 = self.getCoords(self.instBot)
            
            # we check whether or not the play button was pressed
            if (playX0<=x<=playX1) and (playY0<=y<=playY1):
                self.click.play()
                self.mode = "SoloOrCoop"
                
            # we check whether or not the instructions button was pressed   
            elif (instX0<=x<=instX1) and (instY0<=y<=instY1):
                self.click.play()
                self.mode = "Instructions"

        elif (self.mode == "Instructions"):
            bX0, bY0, bX1, bY1 = self.getCoords(self.backBot)

            # we check whether or not the back button was pressed
            if (bX0<=x<=bX1) and (bY0<=y<=bY1):
                self.click.play()
                self.mode = "Start"
        
        elif (self.mode == "SoloOrCoop"):
            soloX0, soloY0, soloX1, soloY1 = self.getCoords(self.soloBot)
            coopX0, coopY0, coopX1, coopY1 = self.getCoords(self.coopBot)
            
            # we check whether or not the solo button was pressed
            if (soloX0<=x<=soloX1) and (soloY0<=y<=soloY1):
                self.click.play()
                self.game.mode = PlaceSoldier(self.game, False)
                self.game.init()

            # we check whether or not theb cooop button was pressed
            elif (coopX0<=x<=coopX1) and (coopY0<=y<=coopY1):
                self.click.play()
                self.game.mode = PlaceSoldier(self.game, True)
                self.game.init()

    def keyPressed(self, keyCode, modifier):
        pass

    def keyReleased(self, keyCode, modifier):
        pass
    
    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        if (self.mode == "Start"):
            self.drawStartScreen(screen)
            
        elif (self.mode == "Instructions"):
            self.drawInstructionsScreen(screen)

        elif (self.mode == "SoloOrCoop"):
            self.drawSoloOrCoopScreen(screen)

    def drawStartScreen(self, screen):
        screen.blit(self.background, (0, 0))
        xRatio, yRatio = (7/24), (1/3)
        x0, y0 = (xRatio * self.width), (yRatio * self.height)
        screen.blit(self.startScreenCoD, (x0, y0))
        
        xRatio, yRatio = (11/30), (46/75)
        x0, y0 = (xRatio * self.width), (yRatio * self.height)
        screen.blit(self.startScreenZombies, (x0, y0))
        self.draw112(screen)
        self.drawStartScreenBottons(screen)

    def draw112(self, screen):
        white = (204, 195, 195)
        xRatio, yRatio = (13/30), (74/150)  
        text = "112"
        text = self.font.render(text, True, white)
        left, top = (xRatio * self.width), (yRatio * self.height)
        screen.blit(text, [left, top])

    def drawStartScreenBottons(self, screen):
        screen.blit(self.playBotton, (self.playBot[0], self.playBot[1]))
        screen.blit(self.instructionsBotton, (self.instBot[0], self.instBot[1]))
    
    def drawInstructionsScreen(self, screen):
        x0, y0 = 0, 0
        screen.blit(self.background, (x0, y0))
        screen.blit(self.backBotton, (self.backBot[0], self.backBot[1]))
        xRatio, yRatio = (6/25), (1/40)  #(9/71) (1/ 20)
        incr = 40
        x0, y0 = (xRatio * self.width - incr), (yRatio * self.height)
        screen.blit(self.instructions, (x0, y0))

    def drawSoloOrCoopScreen(self, screen):
        x0, y0 = 0, 0
        screen.blit(self.background, (x0, y0))
        screen.blit(self.soloBotton, (self.soloBot[0], self.soloBot[1]))
        screen.blit(self.coopBotton, (self.coopBot[0], self.coopBot[1]))

    def loadBackgroundImage(self):
        # background image from http://www.meristation.com/noticias/la-historia
        # -de-call-of-duty-zombies-acabara-con-el-proximo-dlc/2139143
        background = pygame.image.load("background.png").convert_alpha()
        w, h = self.width, self.height
        self.background = pygame.transform.scale(background, (w, h))
    
    def loadStartScreenCoDImage(self):
        # startScreenCoD image from 
        # http://gearnuke.com/top-5-perks-call-duty-zombies/
        startScreenCoD = (pygame.image.load("startScreenCoD.png").
            convert_alpha())
        wRatio, hRatio = (49/120), (3/25)
        w, h = int(wRatio * self.width), int(hRatio * self.height)
        self.startScreenCoD =  pygame.transform.scale(startScreenCoD, (w, h))

    def loadStartScreenZombiesImage(self):
        # startScreenZombies image from 
        # http://gearnuke.com/top-5-perks-call-duty-zombies/
        startScreenZombies = (pygame.image.load("startScreenZombies.png").
            convert_alpha())
        wRatio, hRatio = (31/120), (7/75)
        w, h = int(wRatio * self.width), int(hRatio * self.height)
        self.startScreenZombies =  pygame.transform.scale(startScreenZombies,
         (w, h))

    def loadPlayBottonImage(self):
        # background of image is from
        # http://gearnuke.com/top-5-perks-call-duty-zombies/
        playBotton = pygame.image.load("playBotton.png").convert_alpha()
        w, h = self.playBot[2], self.playBot[-1]
        self.playBotton = pygame.transform.scale(playBotton, (w, h))

    def loadInstructionsBottonImage(self):
        # background of image is from
        # http://gearnuke.com/top-5-perks-call-duty-zombies/
        instructionsBotton = (pygame.image.load("instructionsBotton.png").
        convert_alpha())
        w, h = self.instBot[2], self.instBot[-1]
        self.instructionsBotton = pygame.transform.scale(instructionsBotton,
         (w, h))

    def loadBackBottonImage(self):
        # background of image is from
        # http://gearnuke.com/top-5-perks-call-duty-zombies/
        backBotton = pygame.image.load("backBotton.png").convert_alpha()
        w, h = self.backBot[2], self.backBot[-1]
        self.backBotton = pygame.transform.scale(backBotton, (w, h))
    
    def loadSoloBottonImage(self):
        # background of image is from
        # http://gearnuke.com/top-5-perks-call-duty-zombies/
        soloBotton = pygame.image.load("soloBotton.png").convert_alpha()
        w, h = self.soloBot[2], self.soloBot[-1]
        self.soloBotton = pygame.transform.scale(soloBotton, (w, h))
    
    def loadCoopBottonImage(self):
        # background of image is from
        # http://gearnuke.com/top-5-perks-call-duty-zombies/
        coopBotton = pygame.image.load("coopBotton.png").convert_alpha()
        w, h = self.coopBot[2], self.coopBot[-1]
        self.coopBotton = pygame.transform.scale(coopBotton, (w, h))

    def loadInstructionsImage(self):
        # background of image is from
        # http://gearnuke.com/top-5-perks-call-duty-zombies/
        self.instructions = (pygame.image.load("instructions.png").
        convert_alpha())


class PlaceSoldier(Mode):
    def __init__(self, game, coop):
        super().__init__(game)
        # screen width and screen height
        self.width, self.height = self.game.width, self.game.height
        # coop is a boolean that determines whether we are in 
        # solo mode or coop mode
        self.coop = coop

    def init(self):
        divisor = 30
        self.cellSize = self.width // divisor
        self.rows = self.height // self.cellSize
        self.cols = self.width // self.cellSize
        self.blockGroup = pygame.sprite.Group(Block(0, 0, self.cellSize))
        self.screenX0, self.screenY0 = 0, 0
        self.soldierGroup = None
        size = 40
        self.font = pygame.font.SysFont(None, size, True)
        leftSideMult = 8
        lengthMult = 14
        self.scoreBar = (leftSideMult * self.cellSize, 0, lengthMult *
         self.cellSize, self.cellSize)

        self.board = [[(1),(1),(1),(1),(1),(1),(1),(1),(1),(1),(1),(1),(1),
        (1),(1),(1),(1),(1),(1),(1),(1),(1),(1),(1),(1),(1),(1),(1),(1),(1)],
        [(1), -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1,(1),(1), -1, -1, -1, -1, -1, -1, -1, -1,(1)], 
        [(1), -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1,(1),(1), -1, -1, -1, -1, -1, -1, -1, -1,(1)], 
        [(1),(1),(1), -1, -1,(1),(1), -1, -1,(1),(1),(1),(1),(1),(1), -1, -1,
        (1),(1),(1),(1),(1),(1), -1, -1,(1),(1), -1, -1,(1)], 
        [(1),(1),(1), -1, -1,(1),(1), -1, -1,(1),(1),(1),(1),(1),(1), -1, -1,
        (1),(1),(1),(1),(1),(1), -1, -1,(1),(1), -1, -1,(1)],
        [(1), -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,(1),(1), -1, -1,
         -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,(1)], 
        [(1), -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,(1),(1), -1, -1,
         -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,(1)], 
        [(1), -1, -1,(1),(1),(1),(1),(1),(1),(1),(1), -1, -1, -1, -1, -1, -1,
        (1),(1), -1, -1,(1),(1),(1),(1),(1),(1), -1, -1,(1)],
        [(1), -1, -1,(1),(1),(1),(1),(1),(1),(1),(1), -1, -1, -1, -1, -1, -1,
        (1),(1), -1, -1,(1),(1),(1),(1),(1),(1), -1, -1,(1)], 
        [(1), -1, -1,(1),(1), -1, -1, -1, -1, -1, -1, -1, -1,(1),(1), -1, -1,
         -1, -1, -1, -1,(1),(1), -1, -1, -1, -1, -1, -1,(1)],
        [(1), -1, -1,(1),(1), -1, -1, -1, -1, -1, -1, -1, -1,(1),(1), -1, -1,
         -1, -1, -1, -1,(1),(1), -1, -1, -1, -1, -1, -1,(1)],
        [(1), -1, -1,(1),(1), -1, -1,(1),(1),(1),(1), -1, -1,(1),(1), -1, -1,
        (1),(1), -1, -1, -1, -1, -1, -1,(1),(1), -1, -1,(1)], 
        [(1), -1, -1,(1),(1), -1, -1,(1),(1),(1),(1), -1, -1,(1),(1), -1, -1,
        (1),(1), -1, -1, -1, -1, -1, -1,(1),(1), -1, -1,(1)],
        [(1), -1, -1, -1, -1, -1, -1,(1),(1), -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1,(1),(1), -1, -1, -1, -1, -1, -1,(1)],
        [(1), -1, -1, -1, -1, -1, -1,(1),(1), -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1,(1),(1), -1, -1, -1, -1, -1, -1,(1)],
        [(1),(1),(1),(1),(1),(1),(1),(1),(1),(1),(1),(1),(1),(1),(1),(1),(1),
        (1),(1),(1),(1),(1),(1),(1),(1),(1),(1),(1),(1),(1)]]
        
        self.placeBlocks()
        self.loadFloorImage()
        
    def placeBlocks(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] == 1:
                    x0, y0, = self.getCellTopLeft(row, col)
                    self.blockGroup.add(Block(x0, y0, self.cellSize)) 

    def loadFloorImage(self):
        # floor image from https://minecraft.novaskin.me/search?q=sand%20block
        floor = pygame.image.load("floor.png").convert_alpha()
        w, h = self.cellSize, self.cellSize
        self.image = pygame.transform.scale(floor, (w, h))
    
    def getCellTopLeft(self, row, col):
        x0 = (col * self.cellSize) - self.screenX0
        y0 = (row * self.cellSize) - self.screenY0
        return x0, y0

    def mousePressed(self, x, y):
        placeable = True
        for block in iter(self.blockGroup):
            if block.rect.collidepoint(x,y):
                # prevents user from blacing soldier on a block
                placeable = False
        if placeable:
            row, col = (y // self.cellSize), (x // self.cellSize)
            x0, y0 = self.getCellTopLeft(row, col)
            self.placeSoldier(x0, y0)       

    def placeSoldier(self, x0, y0):
        self.soldierGroup = (pygame.sprite.Group(Soldier(x0, y0, 
                    self.cellSize)))
        # when the soldier is placed, the game starts
        self.game.mode = PlayGame(self.game, self.blockGroup, 
                    self.cellSize, self.rows, self.cols, self.screenX0,  
                    self.screenY0, self.soldierGroup, self.coop)
        self.game.init()

    def keyPressed(self, keyCode, modifier):
        pass
          
    def keyReleased(self, keyCode, modifier):
        pass
    
    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        self.drawFloor(screen)
        self.blockGroup.draw(screen)
        self.drawPlaceSoldierBar(screen)

    def drawFloor(self, screen):
        for row in range(1, self.rows-1):
            for col in range(1, self.cols-1):
                x0, y0 = self.getCellTopLeft(row, col)
                screen.blit(self.image, (x0, y0))

    def drawPlaceSoldierBar(self, screen):
        black = (0, 0, 0)
        red = (250, 40, 40)
        pygame.draw.rect(screen, black, pygame.Rect(self.scoreBar))
        text = "Click on the map to place soldier"
        text = self.font.render(text, True, red)
        mult = 17/2
        left =  self.cellSize * mult
        top = self.cellSize/2**2
        screen.blit(text, [left, top])


class PlayGame(Mode):
    def __init__(self, game, blockGroup, cellSize, rows, cols, screenX0,
        screenY0, soldierGroup, coop):
        super().__init__(game)
        self.width, self.height = self.game.width, self.game.height  
        self.blockGroup = blockGroup
        self.cellSize = cellSize
        self.rows, self.cols = rows, cols
        self.screenX0 = screenX0 
        self.screenY0 = screenY0 
        self.soldierGroup = soldierGroup
        self.coop = coop
        self.decreased = False
        
        zombMult = 2
        botMult = 2
        foodMult = 2
        self.spawningZombieLimit = zombMult * self.cellSize
        self.spawningFoodLimit = foodMult * self.cellSize
        self.spawningBotLimit = botMult * self.cellSize

        self.spriteVariableInit()                                                          

        # gunshot sound from http://soundbible.com/2120-9mm-Gunshot.html
        self.gunshot = pygame.mixer.Sound("gunshot.wav")
        # new round sound from http://soundbible.com/2108-Shoot-Arrow.html
        self.newRound = pygame.mixer.Sound("newRound.wav")
        # game over sound from http://soundbible.com/1771-Laser-Cannon.html
        self.gameOverSound = pygame.mixer.Sound("gameOver.wav")

        self.powerUpNum = 1
        self.powerUpList = ["nuke", "penetration", "invinsibility", "speed",
        "instaKill", "decoy"]

        self.powerUpGroupsInit()               
        self.powerUpInit()

        self.round = 1
        # indicates whether or not the round is transitioning
        self.roundTrans = False
        self.roundDelay = 0
        self.roundBegin = 50

        self.time = 0 
        self.timeLimit = 900
        self.secs = 60
        
        self.minDistIncreased = False
        self.minDistIncreasedSecond = False
        
        leftSideMult = 9
        lengthMult = 12
        self.scoreBar = (leftSideMult * self.cellSize, 0, lengthMult *
         self.cellSize, self.cellSize)
        
        size = 40
        self.font = pygame.font.SysFont(None, size, True)

        self.moveBoard = [ [ -1, -1, -1, -1, -1, -1, -1, -1, -1,(1), -1, -1,
        -1, -1],
        [(1), -1,(1), -1,(1),(1),(1), -1,(1),(1),(1), -1,(1), -1],
        [ -1, -1, -1, -1, -1, -1,(1), -1, -1, -1, -1, -1, -1, -1],
        [ -1,(1),(1),(1),(1), -1, -1, -1,(1), -1,(1),(1),(1), -1],
        [ -1,(1), -1, -1, -1, -1,(1), -1, -1, -1,(1), -1, -1, -1],
        [ -1,(1), -1,(1),(1), -1,(1), -1,(1), -1, -1, -1,(1), -1],
        [ -1, -1, -1,(1), -1, -1, -1, -1, -1, -1,(1), -1, -1, -1] ]

        self.botGroup = pygame.sprite.Group()
        self.botNum = 2
        if self.coop:
            for i in range(self.botNum):
                self.placeBot()
        self.placeFoodAndZombies()

    def init(self):
        self.loadFloorImage()

    def placeFoodAndZombies(self):
        for i in range(self.foodNumber):
            self.placeFood()
        for i in range(self.zombieNum):
            self.placeZombie()

    def loadFloorImage(self):
        # floor image from https://minecraft.novaskin.me/search?q=sand%20block
        floor = pygame.image.load("floor.png").convert_alpha()
        w, h = self.cellSize, self.cellSize
        self.image = pygame.transform.scale(floor, (w, h))

    def powerUpGroupsInit(self):
        self.nukeGroup = pygame.sprite.GroupSingle()
        self.penetrationGroup = pygame.sprite.GroupSingle()
        self.invinsibilityGroup = pygame.sprite.GroupSingle()
        self.speedGroup = pygame.sprite.GroupSingle()
        self.instaKillGroup = pygame.sprite.GroupSingle()
        self.decoyPowerUpGroup = pygame.sprite.GroupSingle()
        self.decoyGroup = pygame.sprite.GroupSingle()

    def powerUpInit(self):
        self.nuke = False

        self.penetration = False
        self.penetrationCount = 0
        self.penetrationLimit = 200
        
        self.invinsibilityCount = 0
        self.invinsibilityLimit = 200
        self.invinsibility = False
        
        self.speedCount = 0
        self.speedLimit = 200
        self.speed = False

        self.instaKillCount = 0
        self.instaKillLimit = 200
        self.instaKill = False

        self.decoyCount = 0
        self.decoyLimit = 200
        self.decoy = False
        self.decoyPos = (None, None)

    def spriteVariableInit(self):
        self.zombieGroup = pygame.sprite.Group()
        self.bulletsToKillRange = 1
        # number of zombies on the map at a certain round
        self.zombieNum = 4
        self.zombieSpeed = 2
        # maximum number of zombies on the map
        self.zombieMax = 6
        
        self.bulletGroup = pygame.sprite.Group()
        self.bulletSize = 10
        
        self.foodGroup = pygame.sprite.Group()
        mult = 0.6
        self.foodSize = int(mult * self.cellSize)
        self.foodNumber = 3
        
    def mousePressed(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        # if the round is not in the phase of changing
        if not(self.roundTrans):
            for soldier in iter(self.soldierGroup):
                # moves soldier and rotates the image of the soldier
                # in the direction corresponding to the arrow key pressed
                soldier.direct(keyCode, self.invinsibility)
                angle = soldier.getAngle()
            if (keyCode ==  pygame.K_c):
                # bullet is shot by soldier
                x0, y0 = self.getBulletCoords(angle)
                self.gunshot.play()
                self.bulletGroup.add(Bullet(x0, y0, angle, self.bulletSize,
                 False, self.penetration, self.instaKill))

    def getBulletCoords(self, angle):
        # function positions bullet on screen in a location such 
        # that it looks like the bullet is coming out 
        # of the soldier's gun
        top, left, right, bottom = 0, 90, 270, 180
        offset = self.cellSize // 2 
        incr = 10
        for soldier in iter(self.soldierGroup):
            x0, y0 = soldier.rect.left, soldier.rect.top
            x1, y1 = soldier.rect.right, soldier.rect.bottom
            if (angle == top):
                bulletX0 = x0 + offset
                bulletY0 = y0 - self.bulletSize
            elif (angle == right):
                bulletX0 = x1
                bulletY0 = y0 + offset
            elif (angle == left):
                bulletX0 = x0 - self.bulletSize
                bulletY0 = y0 + (self.cellSize - offset) - incr
            elif (angle == bottom):
                bulletX0 = x0 + (self.cellSize - offset) - incr
                bulletY0 = y1
            return bulletX0, bulletY0

    def keyReleased(self, keyCode, modifier):
        for soldier in iter(self.soldierGroup):
            soldier.stop(keyCode)
    
    def getFoodCoords(self, x0Cell, y0Cell):
        divisor = 3/2
        x0Food = x0Cell + (self.cellSize + self.foodSize)//divisor
        y0Food = y0Cell + (self.cellSize + self.foodSize)//divisor
        return x0Food, y0Food

    def getPowerUpCoords(self, x0Cell, y0Cell):
        x0powerUp = x0Cell + (self.cellSize - self.foodSize) // 2
        y0powerUp = y0Cell + (self.cellSize - self.foodSize) // 2
        return x0powerUp, y0powerUp
       
    def placeBot(self):
        works = False
        while not(works):
            works = True
            moveBoardRow = random.randint(0, len(self.moveBoard) - 1)
            moveBoardCol = random.randint(0, len(self.moveBoard[0]) - 1)
            if (self.moveBoard[moveBoardRow][moveBoardCol] == 1):
                # prevents the bot from being placed on a wall
                works = False
            else:
                # realRow and realCol are on the grid on which
                # the outer blocks lie 
                realRow = 1 + 2 * moveBoardRow
                realCol = 1 + 2 * moveBoardCol
                x0Cell, y0Cell = self.getCellTopLeft(realRow, realCol)
                x0Bot, y0Bot = self.getZombieCoords(x0Cell, y0Cell)
                for zomb in iter(self.zombieGroup):
                    if ((abs(x0Bot - zomb.rect.left) < 
                        self.spawningZombieLimit) or 
                        (abs(y0Bot - zomb.rect.top) <
                        self.spawningZombieLimit)):
                        works = False
               
        self.botGroup.add(Bot(x0Bot, y0Bot, self.cellSize))
        
        # this prevents the bot from being placed on food, on a zombie
        # or on the soldier
        if ((pygame.sprite.groupcollide(self.zombieGroup, self.botGroup,
        False, True))
        or (pygame.sprite.groupcollide(self.soldierGroup, self.botGroup,
        False, True))):
            self.placeBot()

    def placeFood(self):
        works = False
        while not(works):
            works = True
            moveBoardRow = random.randint(0, len(self.moveBoard) - 1)
            moveBoardCol = random.randint(0, len(self.moveBoard[0]) - 1)
            if (self.moveBoard[moveBoardRow][moveBoardCol] == 1):
                works = False
            else:
                # realRow and realCol are on the grid on which
                # the outer blocks lie 
                realRow = 1 + 2 * moveBoardRow
                realCol = 1 + 2 * moveBoardCol
                x0Cell, y0Cell = self.getCellTopLeft(realRow, realCol)
                x0Food, y0Food = self.getFoodCoords(x0Cell,y0Cell)
                for soldier in iter(self.soldierGroup):
                    if ((abs(x0Food - soldier.rect.left) < 
                        self.spawningFoodLimit) or 
                        (abs(y0Food - soldier.rect.top) <
                        self.spawningFoodLimit)):
                        works = False
                        # this prevents the food from spawning within a certain
                        # distance of the soldier
                        # if the food spawned right next to the solier, 
                        # the game would be too easy
        self.foodGroup.add(Food(x0Food, y0Food,
             self.foodSize))

    def timerFired(self, dt):
        if not(self.roundTrans):
            self.time += 1
            minute = 15
            if (self.time % minute == 0) and (self.secs > 1): 
                self.secs -= 1
            # the time allowed to get all the apples in a round is limited
            if (self.time == self.timeLimit):
                self.gameOver()
            
            # ensures the number of zombies in the map at a given round
            # stays constant
            if not(self.nuke): 
                while (len(self.zombieGroup) != self.zombieNum):
                    self.placeZombie()

            target = 1
            maximum = 200
            result = random.randint(1, maximum)
            # chances of a power up spawning are 1/maximum
            if result == target:
                self.spawnPowerUp()

            self.powerUpTimer()
            self.checkPowerUpCollisions()

            for soldier in iter(self.soldierGroup):
                soldier.move()
                if pygame.sprite.groupcollide(self.blockGroup,
                 self.soldierGroup, False, False, pygame.sprite.collide_rect):
                    for soldier in iter(self.soldierGroup):
                        # prevents soldier from moving through walls
                        soldier.unmove()

            for soldier in iter(self.soldierGroup):
                soldierCoords = (soldier.rect.left + self.cellSize/2,
                 soldier.rect.top + self.cellSize/2)
                soldierCenterRowCol = soldier.getSoldierCenterRowCol()
                soldierBoardRowCol = (int((soldierCenterRowCol[0] - 1) // 2),
                 int((soldierCenterRowCol[1] - 1) // 2))
              
            moveBoard = copy.deepcopy(self.moveBoard)
            self.zombieGroup.update(soldierBoardRowCol, moveBoard,
             soldierCoords, self.decoy, self.decoyPos)
            
            self.bulletGroup.update()
            
            if not(self.penetration):
                # prevents bullets from going through walls
                pygame.sprite.groupcollide(self.blockGroup, self.bulletGroup, 
                    False, True)

            if not(self.instaKill):
                # this allows the number of bullets required to kill a 
                # zombie to be increased
                for zomb in iter(self.zombieGroup):
                    bulletList = (pygame.sprite.spritecollide(zomb, 
                    self.bulletGroup, False))
                    if len(bulletList) != 0:
                        for bullet in bulletList:
                            bullet.kill()
                            zomb.damage()
            else:
                pygame.sprite.groupcollide(self.zombieGroup, self.bulletGroup, 
                    True, True)

            if (self.invinsibility):
                pygame.sprite.groupcollide(self.zombieGroup, self.soldierGroup,
                 True, False)
            
            # collision of a zombie with the soldier ends the game
            elif pygame.sprite.groupcollide(
                self.zombieGroup, self.soldierGroup, False, True):
                self.gameOverSound.play()
                self.gameOver()

            pygame.sprite.groupcollide(self.soldierGroup, self.foodGroup, False,
         True)
            # allows the bots to also get the food
            pygame.sprite.groupcollide(self.botGroup, self.foodGroup, False,
         True)

            if (len(self.foodGroup) == 0):
                # when the soldier gets all the food, we move to the next round
                self.roundTrans = True
            
            # allows zombies to kill bots
            pygame.sprite.groupcollide(self.botGroup, self.zombieGroup, True,
                False)
            
            self.botGroup.update(self.moveBoard, self.zombieGroup,
                 self.bulletSize, self.bulletGroup, self.nuke, self.penetration,
                 self.decoy, self.instaKill)

        else:
            self.nextRound()
            
    def powerUpTimer(self):
        if self.penetration:
            self.penetrationCount += 1
            if (self.penetrationCount == self.penetrationLimit):
                self.penetration = False
                self.penetrationCount = 0
        
        elif self.invinsibility:
            self.invinsibilityCount += 1
            if (self.invinsibilityCount == self.invinsibilityLimit):
                self.invinsibility = False
                self.invinsibilityCount = 0
                for soldier in iter(self.soldierGroup):
                    soldier.updateImage(self.invinsibility)

        elif self.speed:
            self.speedCount += 1
            if (self.speedCount == self.speedLimit):
                self.speed = False
                self.speedCount = 0
                for soldier in iter(self.soldierGroup):
                    soldier.resetSpeed()

        elif self.instaKill:
            self.instaKillCount += 1
            if (self.instaKillCount  == self.instaKillLimit):
                self.instaKill = False
                self.instaKillCount = 0

        elif self.decoy:
            self.decoyCount += 1
            if (self.decoyCount == self.decoyLimit):
                self.decoy = False
                self.decoyCount = 0
                self.decoyGroup.empty()

    def checkPowerUpCollisions(self):
        # each statement indicates what happens if a given power up is picked up
        if (pygame.sprite.groupcollide(self.soldierGroup, self.nukeGroup, False,
            True) or 
        pygame.sprite.groupcollide(self.botGroup, self.nukeGroup, False, True)):
            self.nuke = True
            self.zombieGroup.empty()
        
        elif (pygame.sprite.groupcollide(self.soldierGroup,
            self.penetrationGroup, False, True) or 
        pygame.sprite.groupcollide(self.botGroup, self.penetrationGroup, False,
         True)):
            self.penetration = True
        
        elif (pygame.sprite.groupcollide(self.soldierGroup,
            self.invinsibilityGroup, False, True) or 
        pygame.sprite.groupcollide(self.botGroup, self.invinsibilityGroup,
         False, True)):
            self.invinsibility = True
            for soldier in iter(self.soldierGroup):
                    soldier.updateImage(self.invinsibility)
        
        elif (pygame.sprite.groupcollide(self.soldierGroup,
            self.speedGroup, False, True) or 
        pygame.sprite.groupcollide(self.botGroup, self.speedGroup,
         False, True)):
            self.speed = True
            for soldier in iter(self.soldierGroup):
                soldier.increaseSpeed()
        
        elif (pygame.sprite.groupcollide(self.soldierGroup,
            self.instaKillGroup, False, True) or 
        pygame.sprite.groupcollide(self.botGroup, self.instaKillGroup,
         False, True)):
            self.instaKill = True

        elif (pygame.sprite.groupcollide(self.soldierGroup,
            self.decoyPowerUpGroup, False, True) or 
        pygame.sprite.groupcollide(self.botGroup, self.decoyPowerUpGroup,
         False, True)):
            self.decoy = True
            self.placeDecoy()

    def placeDecoy(self):
        works = False
        while not(works):
            works = True
            moveBoardRow = random.randint(0, len(self.moveBoard) - 1)
            moveBoardCol = random.randint(0, len(self.moveBoard[0]) - 1)
            if (self.moveBoard[moveBoardRow][moveBoardCol] == 1):
                # prevents the bot from being placed on a wall
                works = False
            else:
                # realRow and realCol are on the grid on which
                # the outer blocks lie 
                realRow = 1 + 2 * moveBoardRow
                realCol = 1 + 2 * moveBoardCol
                x0Cell, y0Cell = self.getCellTopLeft(realRow, realCol)
                x0Decoy, y0Decoy = self.getZombieCoords(x0Cell, y0Cell)

        self.decoyPos = (moveBoardRow, moveBoardCol)
        self.decoyGroup.add(Decoy(x0Decoy, y0Decoy, self.cellSize))
        
    def spawnPowerUp(self):
        # ensures that a power up is spawned only if there aren't any
        # other power ups in the map already
        if ((len(self.nukeGroup) == 0) and (len(self.penetrationGroup) == 0)
        and (len(self.invinsibilityGroup) == 0) and (len(self.speedGroup) == 0)
        and (len(self.instaKillGroup) == 0) and
         (len(self.decoyPowerUpGroup) == 0)):
            self.spawnPowerUpHelper()

    def spawnPowerUpHelper(self):
        powerUp = random.choice(self.powerUpList)
        works = False
        while not(works):
            works = True
            moveBoardRow = random.randint(0, len(self.moveBoard) - 1)
            moveBoardCol = random.randint(0, len(self.moveBoard[0]) - 1)
            if (self.moveBoard[moveBoardRow][moveBoardCol] == 1):
                works = False
            else:
                # realRow and realCol are on the grid on which
                # the outer blocks lie 
                realRow = 1 + 2 * moveBoardRow
                realCol = 1 + 2 * moveBoardCol
                x0Cell, y0Cell = self.getCellTopLeft(realRow, realCol)
                x0powerUp, y0powerUp = self.getPowerUpCoords(x0Cell,y0Cell)

        # one of the following power ups is spawned
        if (powerUp == "nuke") and (len(self.nukeGroup) == 0):
            self.nukeGroup.add(Nuke(x0powerUp, y0powerUp, self.foodSize,
             "nuke"))
        
        elif (powerUp == "penetration") and (len(self.penetrationGroup) == 0):
            self.penetrationGroup.add(Penetration(x0powerUp, y0powerUp, 
                self.foodSize, "penetration"))
        
        elif ((powerUp == "invinsibility") and
         (len(self.invinsibilityGroup) == 0)):
            self.invinsibilityGroup.add(Invinsibility(x0powerUp, y0powerUp, 
                self.foodSize, "invinsibility"))

        elif (powerUp == "speed") and (len(self.speedGroup) == 0):
            self.speedGroup.add(Speed(x0powerUp, y0powerUp, 
                self.foodSize, "speed"))

        elif (powerUp == "instaKill") and (len(self.instaKillGroup) == 0):
            self.instaKillGroup.add(InstaKill(x0powerUp, y0powerUp, 
                self.foodSize, "instaKill"))

        elif (powerUp == "decoy") and (len(self.decoyPowerUpGroup) == 0):
            self.decoyPowerUpGroup.add(DecoyPowerUp(x0powerUp, y0powerUp, 
                self.foodSize, "decoyPowerUp"))

    def nextRound(self):
        self.zombieGroup.empty()
        
        if (len(self.bulletGroup) != 0):
            # kills all bullet sprites when round is changing
            self.bulletGroup.empty()
        if self.nuke:
            self.botGroup.empty()
        self.roundDelay += 1
        self.clearPowerUps()
        # delay between moment when round ends and food of the next round 
        # is placed
        if (self.roundDelay == self.roundBegin // 2):
            for i in range(self.foodNumber):
                self.placeFood()

            self.resetPowerUps()

        # delay between moment when food spawns and zombies appear
        # so the user has time to see where all the food has been placed      
        elif (self.roundDelay == self.roundBegin):
            threshold = 3
            thirteen = 13
            self.roundDelay = 0
            self.round += 1
            # the number of zombies and the zombie speed are updated
            self.getZombieNum()
            self.getZombieSpeed()
            if (((self.round > threshold) and
             (self.bulletsToKillRange <= (2**2))) or (self.round > thirteen)):
                self.bulletsToKillRange += 1
            self.roundTrans = False
            self.time = 0
            minute = 60
            self.secs = minute
            if (self.coop):  
                while (len(self.botGroup)!= self.botNum):
                    self.placeBot()
            self.newRound.play()
    
    def resetPowerUps(self):
        self.nuke = False
        self.invinsibility = False
        self.invinsibilityCount = 0
        self.penetration = False
        self.instaKill = False
        self.penetrationCount = 0
        self.instaKillCount = 0

        self.speed = False
        self.speedCount = 0
        self.decoy = False
        self.decoyCount = 0   

    def clearPowerUps(self):
        self.nukeGroup.empty()
        self.penetrationGroup.empty()
        self.invinsibilityGroup.empty()
        for soldier in iter(self.soldierGroup):
            soldier.updateImage(self.invinsibility)
        self.speedGroup.empty()
        for soldier in iter(self.soldierGroup):
            soldier.resetSpeed()
        self.instaKillGroup.empty()
        self.decoyPowerUpGroup.empty()
        self.decoyGroup.empty()

    def getZombieNum(self):
        # every round, the number of zombies increases by one,
        # unless the limit for the number of zombies has been reached
        three = 3
        if ((self.round > three) and not(self.decreased) and 
        (self.bulletsToKillRange == 2**2 + 1)):
            self.zombieNum = 1
            self.decreased = True

        if (self.zombieNum < self.zombieMax):
            self.zombieNum += 1
        
    def getZombieSpeed(self):
        three, four, five, eight = 3, 4, 5, 8
        if (self.round <= three):
            self.zombieSpeed = 2

        elif (self.round > three) and (self.bulletsToKillRange <= 2**2):
            self.zombieSpeed = five
            if not(self.minDistIncreased):
                self.minDistIncreased = True
                for bot in iter(self.botGroup):
                    bot.increaseMinDistanceFromZombToMove()
        else:
            eight = 8
            if (self.round == eight) and not(self.minDistIncreasedSecond):
                self.minDistIncreasedSecond = True
                for bot in iter(self.botGroup):
                    # this makes the bot not move if a zombie is within 
                    # a certain distance from it, making the bot less likely to 
                    # collide with a zombie and die
                    bot.increaseMinDistanceFromZombToMove()
            self.zombieSpeed = eight
           
    def gameOver(self):
        self.game.mode = GameOver(self.game, self.round)
        self.game.init()

    def placeZombie(self):
        works = False
        while not(works):
            works = True
            moveBoardRow = random.randint(0, len(self.moveBoard) - 1)
            moveBoardCol = random.randint(0, len(self.moveBoard[0]) - 1)
            if (self.moveBoard[moveBoardRow][moveBoardCol] == 1):
                works = False
            else:
                # realRow and realCol are on the grid on which
                # the outer blocks lie
                realRow = 1 + 2 * moveBoardRow
                realCol = 1 + 2 * moveBoardCol
                x0Cell, y0Cell = self.getCellTopLeft(realRow, realCol)
                x0Zomb, y0Zomb = self.getZombieCoords(x0Cell,y0Cell)
                # this prevents the zombie from spawning too close
                # to the soldier, which would make the game too hard
                for soldier in iter(self.soldierGroup):
                    if ((abs(x0Zomb - soldier.rect.left) < 
                        self.spawningZombieLimit) or 
                        (abs(y0Zomb - soldier.rect.top) <
                        self.spawningZombieLimit)):
                        works = False
                
                for bot in iter(self.botGroup):
                    if ((abs(x0Zomb - bot.rect.left) < 
                        self.spawningBotLimit) or 
                        (abs(y0Zomb - bot.rect.top) <
                        self.spawningBotLimit)):
                        works = False
                
        typ = "zombie"
        maximum = 15  
        randNum = random.randint(1, maximum)
        threshold = 3
        if ((self.round > threshold) and (randNum == 1) and
         (len(self.zombieGroup) != 0)): 
            typ = "wallZombie"
            zombie = Zombie(1,1,1,1,1,"zombie")
            count = 0
            # ensures that there is always at least one regular zombie
            for zomb in iter(self.zombieGroup):
                if type(zomb) == type(zombie):
                    count += 1
            if (count == 0):
                typ = "zombie"

        if (typ == "wallZombie"):
            self.zombieGroup.add(WallZombie(x0Zomb, y0Zomb,
             self.cellSize, self.zombieSpeed, self.bulletsToKillRange, typ))
        
        else:
            self.zombieGroup.add(Zombie(x0Zomb, y0Zomb,
             self.cellSize, self.zombieSpeed, self.bulletsToKillRange, typ))

        if pygame.sprite.groupcollide(self.botGroup, self.zombieGroup, False,
         True):
            self.placeZombie()

    def getCellTopLeft(self, row, col):
        x0 = (col * self.cellSize) - self.screenX0
        y0 = (row * self.cellSize) - self.screenY0
        return x0, y0

    def getZombieCoords(self, x0Cell, y0Cell):
        x0Zomb = x0Cell + self.cellSize * (1/2)
        y0Zomb = y0Cell + self.cellSize * (1/2)
        return x0Zomb, y0Zomb

    def redrawAll(self, screen):
        self.drawFloor(screen)
        self.blockGroup.draw(screen)
        self.drawPowerUps(screen)
        self.foodGroup.draw(screen)
        self.decoyGroup.draw(screen)
        self.zombieGroup.draw(screen)
        self.bulletGroup.draw(screen)
        self.botGroup.draw(screen)
        self.soldierGroup.draw(screen)
        self.drawScore(screen)
    
    def drawFloor(self, screen):
        for row in range(1, self.rows-1):
            for col in range(1, self.cols-1):
                x0, y0 = self.getCellTopLeft(row, col)
                screen.blit(self.image, (x0, y0))
    
    def drawPowerUps(self, screen):
        self.nukeGroup.draw(screen)
        self.penetrationGroup.draw(screen)
        self.invinsibilityGroup.draw(screen)
        self.speedGroup.draw(screen)
        self.instaKillGroup.draw(screen)
        self.decoyPowerUpGroup.draw(screen)

    def drawScore(self, screen):
        black = (0, 0, 0)
        red = (250, 40, 40)
        pygame.draw.rect(screen, black, pygame.Rect(self.scoreBar))
    
        rounds = "Round %s" % self.round
        text = self.font.render(rounds, True, red)
        left = self.scoreBar[0] + self.cellSize / 2
        top = self.cellSize/2**2
        screen.blit(text, [left, top])

        starv = "Starving in %s" % self.secs
        text =  self.font.render(starv, True, red)
        mult = 13/2
        left = self.scoreBar[0] + self.cellSize * mult
        top = self.cellSize/2**2
       
        screen.blit(text, [left, top])

class Block(pygame.sprite.Sprite):
    def __init__(self, x0, y0, cellSize):
        super().__init__()
        self.x0, self.y0, self.cellSize = x0, y0, cellSize
        self.loadBlockSprite()
        
    def loadBlockSprite(self):
        # block image from http://mashthosebuttons.com/review/angry-video-game-
        # nerd-adventures-review/
        block = pygame.image.load("block.png").convert_alpha()
        w, h = self.cellSize, self.cellSize
        self.image = pygame.transform.scale(block, (w, h))
        self.rect = pygame.Rect(self.x0, self.y0, w,h)
        

class Soldier(pygame.sprite.Sprite):
    def __init__(self, x0, y0, cellSize):
        super().__init__()
        self.x0, self.y0, self.cellSize = x0, y0, cellSize
        self.angle = 0
        ratio = 3 / 4
        self.loadSoldierSprite()
        self.speedX = 0
        self.speedY = 0
        self.originalSpeed = 8
        self.speed = self.originalSpeed
        self.fasterSpeed = 20
        self.image = self.originalImage

    def loadSoldierSprite(self):
        # soldier image from
        # http://www.2dgameartguru.com/2012/04/top-down-view-soldier.html
        soldier = pygame.image.load("soldier.png").convert_alpha()
        invinsibleSoldier = (pygame.image.load("invinsibleSoldier.png").
        convert_alpha())
        w, h = self.cellSize, self.cellSize
        self.originalImage = pygame.transform.scale(soldier, (w, h))
        self.invinsibleSoldier = pygame.transform.scale(invinsibleSoldier,
         (w, h))
        self.rect = pygame.Rect(self.x0, self.y0, w, h)
    
    def updateImage(self, invinsibility):
        if invinsibility:
            self.image = pygame.transform.rotate(self.invinsibleSoldier,
             self.angle)
        else:
            self.image = pygame.transform.rotate(self.originalImage,
             self.angle)
            
    # the two functions below are used when the soldier takes the speed 
    # power up
    def resetSpeed(self):
        self.speed = self.originalSpeed

    def increaseSpeed(self):
        self.speed = self.fasterSpeed

    def rotate(self, invinsibility):
        # the original image is rotated every time, instead of the rotated image 
        # previously used, so the quality of the image is not lost
        if invinsibility:
            self.image = pygame.transform.rotate(self.invinsibleSoldier,
             self.angle)
        else:
            self.image = pygame.transform.rotate(self.originalImage, 
                self.angle)

    def getAngle(self):
        return self.angle

    def getSoldierCenter(self):
        halfSize = (self.rect.right- self.rect.left) / 2
        x = self.rect.left + halfSize
        y = self.rect.top + halfSize
        return x, y

    def getSoldierCenterRowCol(self):
        x, y = self.getSoldierCenter()
        row, col = int(y // self.cellSize), int(x // self.cellSize)
        return row, col

    def direct(self, keyCode, invinsibility):
        # moves soldier and rotates image of soldier in direction
        # that corresponds to the arrow key pressed
        if (keyCode == pygame.K_UP):
            self.angle = 0
            self.rotate(invinsibility)
            self.speedY = -self.speed
            self.speedX = 0
            
        elif (keyCode == pygame.K_DOWN):
            self.angle = 180
            self.rotate(invinsibility)
            self.speedY = self.speed
            self.speedX = 0

        elif (keyCode == pygame.K_LEFT):
            self.angle = 90
            self.rotate(invinsibility)
            self.speedX = -self.speed
            self.speedY = 0
            
        elif (keyCode == pygame.K_RIGHT):
            self.angle = 270
            self.rotate(invinsibility)
            self.speedX = self.speed
            self.speedY = 0
            
    def stop(self, keyCode):
        # when an arrow key is released, the soldier stops moving in 
        # the direction it was moving
        if (keyCode == pygame.K_UP) or (keyCode == pygame.K_DOWN):
            self.speedY = 0
        elif (keyCode == pygame.K_LEFT) or (keyCode == pygame.K_RIGHT):
            self.speedX = 0
       
    def move(self):
        self.rect = self.rect.move(self.speedX, self.speedY)
        
    def unmove(self):
        # called when the soldier runs into a wall
        self.rect = self.rect.move(-self.speedX, -self.speedY)


class Decoy(pygame.sprite.Sprite):
    def __init__(self, x0, y0, cellSize):
        super().__init__()
        self.x0, self.y0, self.cellSize = x0, y0, cellSize
        self.loadDecoySprite()
    
    def loadDecoySprite(self):
        # decoy image from 
        # http://www.2dgameartguru.com/2012/04/top-down-view-soldier.html
        decoy = pygame.image.load("decoy.png").convert_alpha()
        w, h = self.cellSize, self.cellSize
        self.image = pygame.transform.scale(decoy, (w, h))
        self.rect = pygame.Rect(self.x0, self.y0, w, h)


class Bot(pygame.sprite.Sprite):
    def __init__(self, x0, y0, cellSize):
        super().__init__()
        self.x0, self.y0, self.cellSize = x0, y0, cellSize
        self.angle = 0
        self.loadBotSprite()
        self.speedX = 0
        self.speedY = 0
        self.speed = 8
        self.image = self.originalImage
        self.moveCounter = 0
        self.count = 0
        self.moveLimit = 2 * self.cellSize / self.speed
        self.minDistanceFromZombToMove = (((2 * self.cellSize) ** 2 +
         (2* self.cellSize) ** 2) ** (1/2))

        # gunshot sound from http://soundbible.com/2120-9mm-Gunshot.html
        self.gunshot = pygame.mixer.Sound("gunshot.wav")

    def increaseMinDistanceFromZombToMove(self):
        self.count += 1
        if self.count == 1:
            self.minDistanceFromZombToMove = (((2**2 * self.cellSize) ** 2 +
         (2**2 * self.cellSize) ** 2) ** (1/2))
        else:
            six = 6
            self.minDistanceFromZombToMove = (((six * self.cellSize) ** 2 +
         (six * self.cellSize) ** 2) ** (1/2))

    def loadBotSprite(self):
        # bot image from 
        # http://www.2dgameartguru.com/2012/04/top-down-view-soldier.html
        bot = pygame.image.load("bot.png").convert_alpha()
        w, h = self.cellSize, self.cellSize
        self.originalImage = pygame.transform.scale(bot, (w, h))
        self.rect = pygame.Rect(self.x0, self.y0, w, h)

    def getBotCenter(self):
        halfSize = (self.rect.right- self.rect.left) / 2
        x = self.rect.left + halfSize
        y = self.rect.top + halfSize
        return x, y

    def getBotCenterRowCol(self):
        x, y = self.getBotCenter()
        row, col = int(y // self.cellSize), int(x // self.cellSize)
        return row, col    

    def getAngle(self, direct):
        up, down, left, right = 0, 180, 90, 270
        if direct == (1, 0):
            return down
        elif direct == (-1, 0):
            return up
        elif direct == (0, 1):
            return right
        elif direct == (0, -1):
            return left
       
    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.originalImage, angle)
    
    def getBulletCoords(self, angle, bulletSize):
        # function positions bullets in the right place when bot shoots
        top, left, right, bottom = 0, 90, 270, 180
        offset = self.cellSize // 2 
        incr = 10
        x0, y0 = self.rect.left, self.rect.top
        x1, y1 = self.rect.right, self.rect.bottom
        if (angle == top):
            bulletX0 = x0 + offset
            bulletY0 = y0 - bulletSize
        elif (angle == right):
            bulletX0 = x1
            bulletY0 = y0 + offset
        elif (angle == left):
            bulletX0 = x0 - bulletSize
            bulletY0 = y0 + (self.cellSize - offset) - incr
        elif (angle == bottom):
            bulletX0 = x0 + (self.cellSize - offset) - incr
            bulletY0 = y1
        return bulletX0, bulletY0
    
    def shoot(self, direct, bulletSize, bulletGroup, penetration, instaKill):
        angle = self.getAngle(direct)
        # bot image is rotated in the direction the bot is about to shoot
        self.rotate(angle)
        x0, y0 = self.getBulletCoords(angle, bulletSize)
        self.gunshot.play()
        bulletGroup.add(Bullet(x0, y0, angle, bulletSize, True,
         penetration, instaKill))

    def isTooClose(self, zombieGroup, decoy):
        # determines whether at least one zombie is within a certain distance
        # of the bot
        # if a zombie is within a certain distance of the bot, the bot doesn't 
        # move, which makes it less likely for the bot to collide with the
        # zombie and die
        xCenter = self.rect.left + self.cellSize / 2
        yCenter = self.rect.top + self.cellSize / 2
        if not(decoy):
            for zomb in iter(zombieGroup):
                zombX0, zombY0 = zomb.rect.left, zomb.rect.top
                zombCenterX, zombCenterY = (zombX0 + self.cellSize / 2, zombY0 +
                 self.cellSize / 2)
                distance = (((zombCenterX - xCenter)**2 +
                 (zombCenterY - yCenter)**2)**(1/2))
                if (distance < self.minDistanceFromZombToMove):
                    return True
            return False

    def update(self, brd, zombieGroup, bulletSize, bulletGroup, nuke,
     penetration, decoy, instaKill):
        botCenterRowCol = self.getBotCenterRowCol()
        botBoardRowCol = (int((botCenterRowCol[0] - 1) // 2),
                 int((botCenterRowCol[1] - 1) // 2)) 
        board = copy.deepcopy(brd)

        # if nuke is True, there are no zombies to shoot
        if (self.speedX == 0) and (self.speedY == 0) and not(nuke):
            shoot = False

            shoot, direct = self.isZombieInRange(botBoardRowCol, board, 
                zombieGroup, penetration)
         
            # shoot is True if there a zombie in line with the bot
            # (without walls in the way)
            if shoot == True:
                self.shoot(direct, bulletSize, bulletGroup, penetration,
                 instaKill)
            
            # if nuke is true, there are no zombies for the bot to find
            elif not(self.isTooClose(zombieGroup, decoy) or nuke):
                moves = self.getMoves(botBoardRowCol, board, zombieGroup)

                if moves != None and moves != []:
                    move = moves[0]
                    if (move == (-1, 0)):
                        angle = self.getAngle(move)
                        self.speedY = -self.speed
                        self.rotate(angle)
                    elif (move == (1, 0)):
                        angle = self.getAngle(move)
                        self.rotate(angle)
                        self.speedY = self.speed
                    elif (move == (0, -1)):
                        angle = self.getAngle(move)
                        self.rotate(angle)
                        self.speedX = -self.speed
                    elif (move == (0, 1)):
                        angle = self.getAngle(move)
                        self.rotate(angle)
                        self.speedX = self.speed     
        else:
            self.moveCounter += 1
            # ensures that bot only shoots or executes the backtracking
            # algorithm when it is at an intersection of the grid model
            # (the zombies and bots are modelled as moving on a grid)
            self.rect = self.rect.move(self.speedX, self.speedY)
            if (self.moveCounter == self.moveLimit):
                self.speedX, self.speedY, self.moveCounter = 0, 0, 0

    def isZombieInRange(self, botBoardRowCol, board, zombieGroup, penetration):
        directions = [(-1,0), (1, 0), (0, -1), (0, 1)]
        for direct in directions:
            # bot checks all directions to determine if there is a zombie it can
            # shoot
            shoot = self.isZombieInRangeHelper(botBoardRowCol, board,
             direct, zombieGroup, penetration)
            if shoot != None:
                return shoot, direct
        return None, None

    def isZombieInRangeHelper(self, botBoardRowCol, board, direct, zombieGroup,
     penetration):
        dRow, dCol = direct[0], direct[1]
        botBoardRow, botBoardCol = botBoardRowCol[0], botBoardRowCol[1]
        row, col = (botBoardRow + dRow, botBoardCol + dCol)
        # we loop through all the cells in the grid, from the bot, in the
        # direction direct, until we find a zombie
        # if we hit a block the function returns None
        # if (row, col) is off the board, the function returns None
        while self.isInBoard(row, col, board):
            if not(penetration) and (board[row][col] == 1):
                break  
            else:
                # realRow and realCol are on the grid on which
                # the outer blocks lie 
                realRow = 1 + 2 * row
                realCol = 1 + 2 * col
                incr = self.cellSize / (2*2)
                x0 = realCol * self.cellSize + incr
                y0 = realRow * self.cellSize + incr

                x1 = x0 + 2 * self.cellSize - incr
                y1 = y0 + 2 * self.cellSize - incr

                for zomb in iter(zombieGroup):
                    zombX0, zombY0 = zomb.rect.left, zomb.rect.top
                    zombX1, zombY1 = zomb.rect.right, zomb.rect.bottom                    
                    # the two lines of code below are from my 15-112 lab 1
                    # problem 2
                    # they check whether or not a given cell collides with 
                    # any zombie in the zombieGroup
                    if  (((x0 <= zombX0 <= x1) or (zombX0 <= x0 <= zombX1)) and
                   ((y0 <= zombY0 <= y1) or (zombY0 <= y0 <= zombY1))):
                        return True
            
            row, col = (row + dRow, col + dCol)
        return None
            
    def isInBoard(self, row, col, board):
        rows, cols = len(board), len(board[0])
        return not((row < 0) or (col < 0) or (row >= rows) or (col >= cols))

    def getCenterPointRowCol(self, row, col):
        x = (col + 1) * self.cellSize
        y = (row + 1) * self.cellSize
        return x, y    

    def getClosestZombieRowCol(self, zombieGroup):
        zomb = self.getClosestZombie(zombieGroup)
        if zomb == None:
            return None, None
        zombieRowCol = zomb.getZombieRowCol()
        return zombieRowCol

    def getClosestZombie(self, zombieGroup):
        # finds the zombie closest to the bot
        closestZomb = None
        closestZombDist = None
        zombie = Zombie(1,1,1,1,1,"zombie")
        for zomb in iter(zombieGroup):
            if type(zomb) == type(zombie):
                # this ensures that the bot only finds regular zombies
                # and not wall zombies
                # we don't want the bot to find wall zombies because 
                # they are not always at a legal location for the bot
                # (in the walls)
                # the bots can still detect and shoot wall zombies
                distance = self.getDistance(zomb)
                if closestZomb == None:
                    closestZomb = zomb
                    closestZombDist = distance
                elif (distance < closestZombDist):
                    closestZomb = zomb
                    closestZombDistance = distance
        return closestZomb

    def getDistance(self, zomb):
        zombX0, zombY0 = zomb.rect.left, zomb.rect.top
        botX0, botY0 = self.rect.left, self.rect.top
        distance = ((zombX0 - botX0) ** 2 + (zombY0 - botY0) ** 2)**(1/2)
        return distance

    def getMoves(self, botLoc, brd, zombieGroup):
        board = copy.deepcopy(brd)
        zombRow, zombCol = self.getClosestZombieRowCol(zombieGroup)
        if (zombRow, zombCol) == (None, None):
            return None

        zombieLoc = ((zombRow - 1)//2, (zombCol - 1)//2) 
        # in the backtracking algorithm, the bot tries to find a path
        # leading to the closest zombie
        
        directions = [(-1,0), (1, 0), (0, -1), (0, 1)]
        moves = []
        
        def getDirectionList(zombieLoc, botLoc):
            # functon returns a list with directions in order of priority 
            # that the backtracking algorithm should check

            # line below finds the direction of the zombie from the 
            # bot's location
            direct = getDirection(zombieLoc, botLoc)
            
            if direct == (1,1):
                first = [(1,0),(0,1)]
                rest = [(-1,0),(0,-1)]
                randInd = random.randint(0,1)
                directionList = [first[randInd], first[abs(randInd-1)], 
                rest[randInd], rest[abs(randInd-1)]] 
            
            elif direct == (-1,1):
                first = [(-1,0),(0,1)]
                rest = [(1,0),(0,-1)]
                randInd = random.randint(0,1)
                directionList = [first[randInd], first[abs(randInd-1)], 
                rest[randInd], rest[abs(randInd-1)]]

            elif direct == (-1,-1):
                first = [(-1,0),(0,-1)]
                rest = [(1,0), (0,1)]
                randInd = random.randint(0,1)
                directionList = [first[randInd], first[abs(randInd-1)], 
                rest[randInd], rest[abs(randInd-1)]]
            
            elif direct == (1,-1):
                first = [(1,0),(0,-1)]
                rest = [(-1,0),(0,1)]
                randInd = random.randint(0,1)
                directionList = [first[randInd], first[abs(randInd-1)],
                 rest[randInd], rest[abs(randInd-1)]]

            elif direct == (1,0):
                rest = [(0,-1),(0,1),(-1,0)]
                randInd = random.randint(0,1)
                directionList = [(1,0)]+ [rest[randInd], rest[abs(randInd-1)]]
            
            elif direct == (-1,0):
                rest = [(0,-1),(0,1),(1,0)]
                randInd = random.randint(0,1)
                directionList = [(-1,0)]+[rest[randInd], rest[abs(randInd-1)]]
            
            elif direct == (0,1):
                rest = [(1,0),(-1,0),(0,-1)]
                randInd = random.randint(0,1)
                directionList = [(0,1)]+ [rest[randInd], rest[abs(randInd-1)]]
            
            elif direct == (0,-1):
                rest = [(1,0),(-1,0),(0,1)]
                randInd = random.randint(0,1)
                directionList = [(0,-1)]+[rest[randInd], rest[abs(randInd-1)]]
            return directionList

        def getDirection(zombieLoc, botLoc):
            moveVector = (zombieLoc[0]-botLoc[0], zombieLoc[1]-botLoc[1])
            moveVectorX = moveVector[0]
            moveVectorY = moveVector[1]
            if moveVectorX != 0:
                unitVectorX = int(moveVectorX / abs(moveVectorX))
            else:
                unitVectorX = 0
            if moveVectorY != 0:
                unitVectorY = int(moveVectorY / abs(moveVectorY))
            else:
                unitVectorY = 0
            return (unitVectorX, unitVectorY)
      
        def isLegal(row, col):
            if ((row < 0 ) or (col < 0) or (row >= len(board)) or 
            (col >= len(board[0]))):
                return False
            else: 
                return (board[row][col] == -1)

        def solve(botLoc):
            if (botLoc == zombieLoc):
                return moves
        
            else:
                # directions are ordered in order of priority that are
                # most likely to be in the direction of the soldier
                # ordering the directions to loop through optimizes the 
                # efficiency of the function
                directions = getDirectionList(zombieLoc, botLoc)
                
                for direct in range(len(directions)):
                    drow, dcol = directions[direct]
                    
                    pRow, pCol = (botLoc[0] + drow), (botLoc[1] + dcol)
                    if isLegal(pRow, pCol):
                        moves.append(directions[direct])
                        board[pRow][pCol] = 0
                        solution = solve((pRow, pCol))
                        if solution != None:
                            return solution
                        moves.pop()
                        board[pRow][pCol] = -1
                
                return None
        
        return solve(botLoc)

class Zombie(pygame.sprite.Sprite):
    def __init__(self, x0, y0, cellSize, zombieSpeed, bulletsToKillRange, typ):
        super().__init__()
        self.x0, self.y0, = x0, y0
        self.cellSize = cellSize
        self.typ = typ
        self.loadZombieSprite()
        self.image = self.originalImage
        self.speed = zombieSpeed
        self.speedX = 0
        self.speedY = 0
        self.moveCounter = 0
        self.moveLimit = 2 * self.cellSize / self.speed
        self.bulletsToKillRange = bulletsToKillRange
        # self.life is the number of bullets a zombie will require
        # to be killed
        self.life = random.randint(1, self.bulletsToKillRange)
     
    def loadZombieSprite(self):
        # zombie image from 
        # https://opengameart.org/content/animated-top-down-zombie
        angle = 90
        x = "%s.png" % self.typ
        zombie = pygame.image.load("%s.png" % self.typ).convert_alpha()
        w, h = self.cellSize, self.cellSize
        zombie = pygame.transform.scale(zombie, (w, h))
        self.originalImage = pygame.transform.rotate(zombie, angle)
        self.rect = pygame.Rect(self.x0, self.y0, w, h)

    def damage(self):
        self.life -= 1
        if self.life <= 0:
            self.kill()

    def getZombieRowCol(self):
        halfSize = (self.rect.left - self.rect.right) / 2
        x = self.rect.left + halfSize
        y = self.rect.top + halfSize
        row, col = int(y // self.cellSize), int(x // self.cellSize)
        return row, col

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.originalImage, angle)

    def update(self, soldierBoardRowCol, brd, soldierCoords, decoy, decoyPos):
        board = copy.deepcopy(brd)
        if (self.speedX == 0) and (self.speedY == 0):
            moves = self.getMoves(soldierBoardRowCol, board, decoy, decoyPos)
            if moves != None and moves != []:
                move = moves[0]
                if (move == (-1, 0)):
                    angle = 0
                    self.speedY = -self.speed
                    self.rotate(angle)
                elif (move == (1, 0)):
                    angle = 180
                    self.rotate(angle)
                    self.speedY = self.speed
                elif (move == (0, -1)):
                    angle = 90
                    self.rotate(angle)
                    self.speedX = -self.speed
                elif (move == (0, 1)):
                    angle = 270
                    self.rotate(angle)
                    self.speedX = self.speed
    
        else:
            self.moveCounter += 1
            # ensures that zombie only executes the backtracking
            # algorithm when it is at an intersection of the grid model
            # (the zombies and bots are modelled as moving on a grid)
            self.rect = self.rect.move(self.speedX, self.speedY)
            if (self.moveCounter == self.moveLimit):
                self.speedX, self.speedY, self.moveCounter = 0, 0, 0
    
    def getMoves(self, soldierLoc, brd, decoy, decoyPos):
        board = copy.deepcopy(brd)
        zombRow, zombCol = self.getZombieRowCol()
        zombieLoc =  ((zombRow - 1)//2, (zombCol - 1)//2) 
        if decoy:
            soldierLoc = decoyPos
        
        directions = [(-1,0), (1, 0), (0, -1), (0, 1)]
        moves = []
        
        def getDirectionList(soldierPos, zombiePos):
            # functon returns a list with directions in order of priority 
            # that the backtracking algorithm should check
           
            # line below finds the direction of the soldier from the 
            # zombie's location
            direct = getDirection(soldierPos, zombiePos)
            
            if direct == (1,1):
                first = [(1,0),(0,1)]
                rest = [(-1,0),(0,-1)]
                randInd = random.randint(0,1)
                directionList = [first[randInd], first[abs(randInd-1)], 
                rest[randInd], rest[abs(randInd-1)]] 
            
            elif direct == (-1,1):
                first = [(-1,0),(0,1)]
                rest = [(1,0),(0,-1)]
                randInd = random.randint(0,1)
                directionList = [first[randInd], first[abs(randInd-1)], 
                rest[randInd], rest[abs(randInd-1)]]
        
            elif direct == (-1,-1):
                first = [(-1,0),(0,-1)]
                rest = [(1,0), (0,1)]
                randInd = random.randint(0,1)
                directionList = [first[randInd], first[abs(randInd-1)], 
                rest[randInd], rest[abs(randInd-1)]]
            
            elif direct == (1,-1):
                first = [(1,0),(0,-1)]
                rest = [(-1,0),(0,1)]
                randInd = random.randint(0,1)
                directionList = [first[randInd], first[abs(randInd-1)],
                 rest[randInd], rest[abs(randInd-1)]]

            elif direct == (1,0):
                rest = [(0,-1),(0,1),(-1,0)]
                randInd = random.randint(0,1)
                directionList = [(1,0)]+ [rest[randInd], rest[abs(randInd-1)]]
            
            elif direct == (-1,0):
                rest = [(0,-1),(0,1),(1,0)]
                randInd = random.randint(0,1)
                directionList = [(-1,0)]+[rest[randInd], rest[abs(randInd-1)]]
            
            elif direct == (0,1):
                rest = [(1,0),(-1,0),(0,-1)]
                randInd = random.randint(0,1)
                directionList = [(0,1)]+ [rest[randInd], rest[abs(randInd-1)]]
            
            elif direct == (0,-1):
                rest = [(1,0),(-1,0),(0,1)]
                randInd = random.randint(0,1)
                directionList = [(0,-1)]+[rest[randInd], rest[abs(randInd-1)]]
            
            return directionList

        def getDirection(soldierPos, zombiePos):
            moveVector = (soldierPos[0]-zombiePos[0],soldierPos[1]-zombiePos[1])
            moveVectorX = moveVector[0]
            moveVectorY = moveVector[1]
            if moveVectorX != 0:
                unitVectorX = int(moveVectorX / abs(moveVectorX))
            else:
                unitVectorX = 0
            if moveVectorY != 0:
                unitVectorY = int(moveVectorY / abs(moveVectorY))
            else:
                unitVectorY = 0
            return (unitVectorX, unitVectorY)
      

        def isLegal(row, col):
            if ((row < 0 ) or (col < 0) or (row >= len(board)) or 
            (col >= len(board[0]))):
                return False
            else: 
                return (board[row][col] == -1)


        def solve(zombLoc):
            if (zombLoc == soldierLoc):
                return moves
        
            else:
                # directions are ordered in order of priority that are
                # most likely to be in the direction of the soldier
                # ordering the directions to loop through optimizes the 
                # efficiency of the function
                directions = getDirectionList(soldierLoc, zombLoc)
                
                for direct in range(len(directions)):
                    drow, dcol = directions[direct]
                    pRow, pCol = (zombLoc[0] + drow), (zombLoc[1] + dcol)
                    if isLegal(pRow, pCol):
                        moves.append(directions[direct])
                        board[pRow][pCol] = 0
                        solution = solve((pRow, pCol))
                        if solution != None:
                            return solution
                        moves.pop()
                        board[pRow][pCol] = -1

                return None

        return solve(zombieLoc)


class WallZombie(Zombie):
    def __init__(self, x0, y0, cellSize, zombieSpeed, bulletsToKillRange, typ):
        super().__init__(x0, y0, cellSize, zombieSpeed, bulletsToKillRange, typ)
        # so the components combined make the resultant speed the same
        # as self.speed
        self.diagSpeed = self.speed * (2)**(1/2) / 2
        mult = 3
        self.moveCounter = mult * self.moveCounter
        
    # wallZombie image from
    # https://www.pinterest.com/pin/349943833527272089/
    
    def getCellTopLeft(self, row, col):
        x0 = (col * self.cellSize) 
        y0 = (row * self.cellSize) 
        return x0, y0

    def update(self, soldierBoardRowCol, brd, soldierPos, decoy, decoyPos):
        if (self.speedX == 0) and (self.speedY == 0):
            zombiePos = (self.rect.left + self.cellSize/2, self.rect.top +
             self.cellSize/2)
            
            if decoy:
                realRow = 1 + 2 * decoyPos[0]
                realCol = 1 + 2 * decoyPos[1]

                x0Cell, y0Cell = self.getCellTopLeft(realRow, realCol)
                
                soldierPos = (x0Cell + self.cellSize), (y0Cell + self.cellSize) 
               
            direct = self.getDirection(soldierPos, zombiePos)
            if (direct == (1, 1)):
                angle = 225
                self.speedX = self.diagSpeed
                self.speedY = self.diagSpeed
                self.rotate(angle)
            elif (direct == (-1, 1)):
                angle = 315
                self.speedX = self.diagSpeed
                self.speedY = -self.diagSpeed
                self.rotate(angle)
            elif (direct == (1, -1)):
                angle = 135
                self.speedX = -self.diagSpeed
                self.speedY = self.diagSpeed
                self.rotate(angle)
            elif (direct == (-1, -1)):
                angle = 45
                self.speedX = -self.diagSpeed
                self.speedY = -self.diagSpeed
                self.rotate(angle)
            elif (direct == (-1, 0)):
                angle = 0
                self.speedX = 0
                self.speedY = -self.speed
                self.rotate(angle)
            elif (direct == (1, 0)):
                angle = 180
                self.rotate(angle)
                self.speedX = 0
                self.speedY = self.speed
            elif (direct == (0, -1)):
                angle = 90
                self.rotate(angle)
                self.speedX = -self.speed
                self.speeY = 0
            elif (direct == (0, 1)):
                angle = 270
                self.rotate(angle)
                self.speedX = self.speed
                self.speedY = 0
            
            self.rect = self.rect.move(int(self.speedX), int(self.speedY))
    
        else:
            self.moveCounter += 1
            self.rect = self.rect.move(self.speedX, self.speedY)
            self.x0 += self.speedX
            self.y0 += self.speedY
            if (self.moveCounter == self.moveLimit):
                self.speedX, self.speedY, self.moveCounter = 0, 0, 0

    def getDirection(self, soldierPos, zombiePos):
        moveVector = (soldierPos[0]-zombiePos[0],soldierPos[1]-zombiePos[1])
        moveVectorX = moveVector[0]
        moveVectorY = moveVector[1]
        if (abs(moveVectorX) < self.cellSize/2):
            unitVectorX = 0
        else:
            unitVectorX = int(moveVectorX / abs(moveVectorX))
        if (abs(moveVectorY) < self.cellSize/2):
            unitVectorY = 0  
        else:
            unitVectorY = int(moveVectorY / abs(moveVectorY))
        return (unitVectorY, unitVectorX)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x0, y0, angle, bulletSize, botBullet, penetration,
     instaKill):
        super().__init__()
        self.x0 = x0
        self.y0 = y0
        self.bulletSize = bulletSize
        self.angle = angle
        self.speed = 40
        self.speedX, self.speedY = self.getSpeeds()
        self.botBullet = botBullet
        self.penetration = penetration
        self.instaKill = instaKill
        self.loadBulletSprite()

    def loadBulletSprite(self):
        # bullet image from
        # https://code.tutsplus.com/tutorials/build-a-stage3d-shoot-em-up-
        # interaction--active-11054
        if self.penetration:
            bullet = pygame.image.load("penetrationBullet.png").convert_alpha()
        elif self.instaKill:
            bullet = pygame.image.load("instaKillBullet.png").convert_alpha()
        elif self.botBullet:
            bullet = pygame.image.load("botBullet.png").convert_alpha()
        else:
            bullet = pygame.image.load("bullet.png").convert_alpha()
        bullet = pygame.transform.scale(bullet, (self.bulletSize,
         self.bulletSize))
        self.image = pygame.transform.rotate(bullet, self.angle)
        self.rect = pygame.Rect(self.x0, self.y0, self.bulletSize,
         self.bulletSize)

    def getSpeeds(self):
        up, down, left, right = 0, 180, 90, 270
        if (self.angle == up):
            self.speedX = 0
            self.speedY = -self.speed
        elif (self.angle == down):
            self.speedX = 0
            self.speedY = self.speed
        elif (self.angle == left):
            self.speedX = -self.speed
            self.speedY = 0
        elif (self.angle == right):
            self.speedX = self.speed
            self.speedY = 0
        return self.speedX, self.speedY

    def update(self):
        self.rect = self.rect.move(self.speedX, self.speedY)
        

class Food(pygame.sprite.Sprite):
    def __init__(self, x0, y0, foodSize):
        super().__init__()
        self.x0 = x0
        self.y0 = y0
        self.foodSize = foodSize
        self.loadSprite()

    def loadSprite(self):
        # food image from 
        # https://www.gamedevmarket.net/asset/fruits-pack-6027/
        food = pygame.image.load("food.png").convert_alpha()
        w, h = self.foodSize, self.foodSize
        self.image = pygame.transform.scale(food, (w, h))
        self.rect = pygame.Rect(self.x0, self.y0, w,h)


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x0, y0, size, typ):
        super().__init__()
        self.x0 = x0
        self.y0 = y0
        self.size = size
        self.typ = typ
        self.loadSprite()

    def loadSprite(self):
        fileName = "%s.png" % self.typ
        powerUp = pygame.image.load(fileName).convert_alpha()
        w, h = self.size, self.size
        self.image = pygame.transform.scale(powerUp, (w, h))
        self.rect = pygame.Rect(self.x0, self.y0, w,h)


class Nuke(PowerUp):
    def __init__(self, x0, y0, nukeSize, typ):
        super().__init__(x0, y0, nukeSize, typ)
        # nuke image from https://www.shutterstock.com/image-vector/set-vector-
        #icons-radiation-hazardnuclear-135299120?src=Uh5xW6FIA8UGBQalWRlqLA-1-3


class Penetration(PowerUp):
    def __init__(self, x0, y0, nukeSize, typ):
        super().__init__(x0, y0, nukeSize, typ)
        # penetration image from 
        # http://callofduty.wikia.com/wiki/Weapon_Proficiency


class Invinsibility(PowerUp):
    def __init__(self, x0, y0, nukeSize, typ):
        super().__init__(x0, y0, nukeSize, typ)
    # invinsibility image from
    # https://forum.blockland.us/index.php?topic=227785.0


class Speed(PowerUp):
    def __init__(self, x0, y0, nukeSize, typ):
        super().__init__(x0, y0, nukeSize, typ)
    # speed image from
    # http://cyrildavies.weebly.com/home/archives/03-2014


class InstaKill(PowerUp):
    def __init__(self, x0, y0, nukeSize, typ):
        super().__init__(x0, y0, nukeSize, typ)
    # instaKill image from
    # https://www.youtube.com/watch?v=UmqPbQpRcfQ


class DecoyPowerUp(PowerUp):
    def __init__(self, x0, y0, nukeSize, typ):
        super().__init__(x0, y0, nukeSize, typ)
    # decoy power up image from 
    # http://www.rw-designer.com/icon-detail/5211


class GameOver(Mode):
    def __init__(self, game, rnd):
        super().__init__(game)
        self.width, self.height = self.game.width, self.game.height
        self.round = rnd
        size = 100
        self.gameOverFont = pygame.font.SysFont(None, size, True)
        size = 40
        self.roundsFont = pygame.font.SysFont(None, size, True)
        self.white = (204, 195, 195)

    def init(self):
        self.counter = 0
        self.time = 120 
        self.loadBackgroundImage()

    def loadBackgroundImage(self):
        # background image from http://www.meristation.com/noticias/la-historia
        # -de-call-of-duty-zombies-acabara-con-el-proximo-dlc/2139143
        background = pygame.image.load("background.png").convert_alpha()
        w, h = self.width, self.height
        self.background = pygame.transform.scale(background, (w, h))
        
    def mousePressed(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        pass
    
    def keyReleased(self, keyCode, modifier):
        pass
    
    def timerFired(self, dt):
        self.counter += 1
        # the gameover screen is displayed for a certain amount of time
        if (self.counter == self.time):
            self.game.mode = StartGame(self.game)
            self.game.init()

    def redrawAll(self, screen):
        screen.blit(self.background, (0, 0))
        self.drawGameOver(screen)
        self.drawRounds(screen)
    
    def drawGameOver(self, screen):
        xRatio, yRatio = (1/3), (1/3)
        text = "Game Over"
        text = self.gameOverFont.render(text, True, self.white)
        left, top = (xRatio * self.width), (yRatio * self.height)
        screen.blit(text, [left, top])

    def drawRounds(self, screen):
        xRatio, yRatio = (9/24), (38/75)
        incr = 18
        if (self.round == 1):
            text = "You Survived 1 Round"
        else:
            text = "You Survived %s Rounds" % self.round

        text = self.roundsFont.render(text, True, self.white)
        left, top = (xRatio * self.width - incr), (yRatio * self.height)
        screen.blit(text, [left, top])


def runGame():
    ratio = 8/15
    width = 1200
    height = int(width * ratio)
    Game(width, height).run()

runGame()