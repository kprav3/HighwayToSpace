from itertools import cycle
import random
import sys
import pygame
from pygame.locals import *

FPS = 30    #Frame Rate per second
SCREENWIDTH  = 288
SCREENHEIGHT = 512
PLANETGAPSIZE  = 125 # gap between upper and lower planet                   ##
BASEY        = SCREENHEIGHT * 0.90                                          
HEAD       = SCREENHEIGHT * -0.10                                           ##
# image, sound and hitmask  dicts
IMAGES, SOUNDS, HITMASKS = {}, {}, {}

# list of all possible players
PLAYERS_LIST = (                                                            ##
    # ufo
    (                                                                       ##
        'assets/sprites/ufo.png',                                           ##
        'assets/sprites/ufo1.png',                                          ##
        'assets/sprites/ufo2.png',                                          ##
    ),                                                                      ##
    # medium ufo
    (                                                                       ##
        'assets/sprites/ufo3.png',                                          ##
        'assets/sprites/ufo4.png',                                          ##
        'assets/sprites/ufo5.png',                                          ##
    ),                                                                      ##

)

# list of Backgrounds
BACKGROUNDS_LIST = (                                                        ##
    'assets/sprites/nightsky.png',                                          ##
    'assets/sprites/nightsky2.png',                                         ##            
)

# list of Planets
PLANETS_LIST = (                                                            ##
    'assets/sprites/asteroid2.png',                                         ##
    'assets/sprites/asteroid.png',                                          ##
    'assets/sprites/asteroid2.png',                                         ##        
    #'assets/sprites/brownasteroid.png',
    )

#Since Xrange is not available in python 3
try:  
    xrange
except NameError:
    range = range


def main():
    global SCREEN, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('HighwayToSpace')                            ##

    # numbers sprites for score display
    IMAGES['numbers'] = (                                                   ##
        pygame.image.load('assets/sprites/0.png').convert_alpha(),          ##
        pygame.image.load('assets/sprites/1.png').convert_alpha(),          ##
        pygame.image.load('assets/sprites/2.png').convert_alpha(),          ##
        pygame.image.load('assets/sprites/3.png').convert_alpha(),          ##
        pygame.image.load('assets/sprites/4.png').convert_alpha(),          ##
        pygame.image.load('assets/sprites/5.png').convert_alpha(),          ##
        pygame.image.load('assets/sprites/6.png').convert_alpha(),          ##
        pygame.image.load('assets/sprites/7.png').convert_alpha(),          ##
        pygame.image.load('assets/sprites/8.png').convert_alpha(),          ##
        pygame.image.load('assets/sprites/9.png').convert_alpha()           ##
    )

    # Game Over image
    IMAGES['gameover'] = pygame.image.load('assets/sprites/gameover.png').convert_alpha()   ##
    # Display image for Welcome Screen
    IMAGES['message'] = pygame.image.load('assets/sprites/message.png').convert_alpha()     ##
    # base sprite
    IMAGES['base'] = pygame.image.load('assets/sprites/base.png').convert_alpha()           ##
    # head sprite
    IMAGES['head'] = pygame.image.load('assets/sprites/head.png').convert_alpha()           ##

    # sounds
    #Checking the OS 
    if 'win' in sys.platform:
        soundExt = '.wav'
    else:
        soundExt = '.ogg'

    SOUNDS['die']    = pygame.mixer.Sound('assets/audio/die' + soundExt)
    SOUNDS['hit']    = pygame.mixer.Sound('assets/audio/hit' + soundExt)
    SOUNDS['point']  = pygame.mixer.Sound('assets/audio/point' + soundExt)
    SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh' + soundExt)
    SOUNDS['wing']   = pygame.mixer.Sound('assets/audio/wing' + soundExt)

    while True:
        # select random background sprites
        randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()

        # select random player sprites
        randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
        IMAGES['player'] = (
            pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha(),
        )

        # select random planet sprites
        planetindex = random.randint(0, len(PLANETS_LIST) - 1)                              ##
        planetindex2 = random.randint(0, len(PLANETS_LIST) - 1)                             ##
        planetindex3 = random.randint(0, len(PLANETS_LIST) - 1)                             ##
        planetindex4 = random.randint(0, len(PLANETS_LIST) - 1)                             ##
        planetindex5 = random.randint(0, len(PLANETS_LIST) - 1)                             ##

        #randomly assigning planets 
        Planets = [                                                                         ##
            pygame.image.load(PLANETS_LIST[planetindex2]).convert_alpha(),                  ##
            pygame.image.load(PLANETS_LIST[planetindex]).convert_alpha(),                   ##
            pygame.image.load(PLANETS_LIST[planetindex3]).convert_alpha(),                  ##
            pygame.image.load(PLANETS_LIST[planetindex4]).convert_alpha(),                  ##    
            pygame.image.load(PLANETS_LIST[planetindex5]).convert_alpha()                   ##    
            ]                                                                               ##


        IMAGES['planet'] = (                                                                ##
            Planets[random.randint(0, len(Planets) - 1)],                                   ##    
            Planets[random.randint(0, len(Planets) - 1)],                                   ##
            Planets[random.randint(0, len(Planets) - 1)],                                   ##
            Planets[random.randint(0, len(Planets) - 1)],                                   ##
            Planets[random.randint(0, len(Planets) - 1)],                                   ##
        )                                                                                   ##

        # hismask for Planets
        HITMASKS['planet'] = (
            getHitmask(IMAGES['planet'][0]),
            getHitmask(IMAGES['planet'][1]),
            getHitmask(IMAGES['planet'][2]),                                                ##
        )

        # hitmask for player
        HITMASKS['player'] = (
            getHitmask(IMAGES['player'][0]),
            getHitmask(IMAGES['player'][1]),
            getHitmask(IMAGES['player'][2]),                                                ##
        )

        movementInfo = showWelcomeAnimation()
        crashInfo = mainGame(movementInfo)
        showGameOverScreen(crashInfo)


def showWelcomeAnimation():
    """Shows welcome screen animation of Highway To Space"""
    # index of player to blit on screen
    playerIndex = 0
    playerIndexGen = cycle([0, 1, 2, 1])
    # iterator used to change playerIndex after every 5th iteration
    loopIter = 0

    playerx = int(SCREENWIDTH * 0.2)
    playery = int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2)

    messagex = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.12)

    basex = 0                                                                           
    headx = 0                                                                                       ##

    # amount by which base can maximum shift to left
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()
    headshift = IMAGES['head'].get_width() - IMAGES['background'].get_width()                       ##

    # player shm(simple harmonic motion) for up-down motion on welcome screen
    playerShmVals = {'val': 0, 'dir': 1}                                                            ##

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                # make first Boost sound and return values for mainGame
                SOUNDS['wing'].play()
                return {
                    'playery': playery + playerShmVals['val'],
                    'basex': basex,
                    'headx':headx,                                                                  ##
                    'playerIndexGen': playerIndexGen,
                }

        # adjust playery, playerIndex, basex
        if (loopIter + 1) % 5 == 0:
            playerIndex = next(playerIndexGen)
        loopIter = (loopIter + 1) % 30
        basex = -((-basex + 4) % baseShift)
        headx = -((-headx + 4) % headshift)                                                         ##
        playerShm(playerShmVals)

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))                                                    ##
        SCREEN.blit(IMAGES['player'][playerIndex],
                    (playerx, playery + playerShmVals['val']))
        SCREEN.blit(IMAGES['message'], (messagex, messagey))
        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        SCREEN.blit(IMAGES['head'], (headx, HEAD))                                                  ##


        pygame.display.update()
        FPSCLOCK.tick(FPS)


def mainGame(movementInfo):
    score = playerIndex = loopIter = 0
    playerIndexGen = movementInfo['playerIndexGen']
    playerx, playery = int(SCREENWIDTH * 0.2), movementInfo['playery']

    basex = movementInfo['basex']
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()
    headx = movementInfo['headx']                                                                   ##
    headshift = IMAGES['head'].get_width() - IMAGES['background'].get_width()                       ##

    # get 5 new Planets to add to upperPlanets, middlePlanets, lowerPlanets list
    newplanet1 = getRandomplanet()                                                                  ##
    newplanet2 = getRandomplanet()                                                                  ##
    newplanet3 = getRandomplanet()                                                                  ##
    newplanet4 = getRandomplanet()                                                                  ##
    newplanet5 = getRandomplanet()                                                                  ##

    # list of upper Planets
    upperPlanets = [
        {'x': SCREENWIDTH + 200, 'y': newplanet1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newplanet2[0]['y']},
    ]

    # list of lowerplanet
    lowerPlanets = [
        {'x': SCREENWIDTH + 200, 'y': newplanet3[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newplanet4[1]['y']},
    ]

    #list of middle planet
    middlePlanets = [                                                                               ##
            {'x':SCREENWIDTH + 200, 'y': newplanet1[1]['y']},                                       ##
            {'x':SCREENWIDTH + 200 +  (SCREENWIDTH / 2), 'y':newplanet5[1]['y']},                   ##
    ]                                                                                               ##

    planetVelX = -10                                                                                ##

    # player velocity, max velocity, downward accleration, accleration on Boost
    playerVelY    =  -9   # player's velocity along Y, default same as player Boosted
    playerMaxVelY =  10   # max velocity along Y, max descend speed
    playerMinVelY =  -8   # min velocity along Y, max ascend speed
    playerAccY    =   1   # players downward accleration
    playerRot     =  40   # player's rotation
    playerVelRot  =   3   # angular speed
    playerRotThr  =  20   # rotation threshold
    playerBoostAcc =  -9   # players speed on Boosting
    playerBoostped = False # True when player Boosts


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > -2 * IMAGES['player'][0].get_height():
                    playerVelY = playerBoostAcc
                    playerBoostped = True
                    SOUNDS['wing'].play()
                    
        # check for crash here
        crashTest = checkCrash({'x': playerx, 'y': playery, 'index': playerIndex},
                               upperPlanets, middlePlanets, lowerPlanets)                       ##
        if crashTest[0]:
            return {
                'y': playery,
                'groundCrash': crashTest[1],
                'basex': basex,
                'headx': headx,                                                                 ##                
                'upperPlanets': upperPlanets,
                'lowerPlanets': lowerPlanets,
                'middlePlanets': middlePlanets,                                                 ##
                'score': score,
                'playerVelY': playerVelY,
                'playerRot': playerRot
            }

        # check for score
        playerMidPos = playerx + IMAGES['player'][0].get_width() / 2
        for planet in upperPlanets:
            planetMidPos = planet['x'] + IMAGES['planet'][0].get_width() / 2
            if planetMidPos <= playerMidPos < planetMidPos + 4:
                score += 1
                SOUNDS['point'].play()

        # playerIndex basex change
        if (loopIter + 1) % 3 == 0:
            playerIndex = next(playerIndexGen)
        loopIter = (loopIter + 1) % 30
        basex = -((-basex + 100) % baseShift)
        headx = -((-headx + 100) % headshift)                                                   ##

        # rotate the player
        if playerRot > -90:
            playerRot -= playerVelRot

        # player's movement
        if playerVelY < playerMaxVelY and not playerBoostped:
            playerVelY += playerAccY
        if playerBoostped:
            playerBoostped = False

            # more rotation to cover the threshold (calculated in visible rotation)
            playerRot = 45

        playerHeight = IMAGES['player'][playerIndex].get_height()
        playery += min(playerVelY, BASEY - playery - playerHeight)

        # move Planets to left
        for uplanet, lplanet, mplanet in zip(upperPlanets, lowerPlanets, middlePlanets):        ##
            uplanet['x'] += planetVelX
            lplanet['x'] += planetVelX
            mplanet['x'] += planetVelX                                                          ##


        # add new planet when first planet is about to touch left of screen
        if 0 < upperPlanets[0]['x'] < 9:                                                        ##
            newplanet = getRandomplanet()
            upperPlanets.append(newplanet[0])
            lowerPlanets.append(newplanet[1])
            middlePlanets.append(newplanet[2])                                                  ##

        # remove first planet if its out of the screen
        if upperPlanets[0]['x'] < -IMAGES['planet'][0].get_width():
            upperPlanets.pop(0)
            lowerPlanets.pop(0)
            middlePlanets.pop(0)                                                                ##

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))

        for uplanet, lplanet, mplanet in zip(upperPlanets, lowerPlanets, middlePlanets):        ##
            SCREEN.blit(IMAGES['planet'][0], (uplanet['x'], uplanet['y']))
            SCREEN.blit(IMAGES['planet'][1], (lplanet['x'], lplanet['y']))
            SCREEN.blit(IMAGES['planet'][2], (mplanet['x'], mplanet['y']))                      ##

        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        SCREEN.blit(IMAGES['head'], (headx, HEAD))                                              ##
        # print score so player overlaps the score
        showScore(score)

        # Player rotation has a threshold
        visibleRot = playerRotThr
        if playerRot <= playerRotThr:
            visibleRot = playerRot
        
        playerSurface = pygame.transform.rotate(IMAGES['player'][playerIndex], visibleRot)
        SCREEN.blit(playerSurface, (playerx, playery))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def showGameOverScreen(crashInfo):
    """When the player crashes, Game over Sprite is displayed"""
    score = crashInfo['score']
    playerx = SCREENWIDTH * 0.2
    playery = crashInfo['y']
    playerHeight = IMAGES['player'][0].get_height()
    playerVelY = crashInfo['playerVelY']
    playerAccY = 2
    playerRot = crashInfo['playerRot']
    playerVelRot = 7

    basex = crashInfo['basex']
    headx = crashInfo['headx']                                                              ##

    upperPlanets, lowerPlanets, middlePlanets = crashInfo['upperPlanets'], crashInfo['lowerPlanets'], crashInfo['middlePlanets']  ##

    # play hit and die sounds
    SOUNDS['hit'].play()
    if not crashInfo['groundCrash']:
        SOUNDS['die'].play()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery + playerHeight >= BASEY - 1:
                    return

        # player y shift
        if playery + playerHeight < BASEY - 1:
            playery += min(playerVelY, BASEY - playery - playerHeight)

        # player velocity change
        if playerVelY < 15:
            playerVelY += playerAccY

        # rotate only when it's a planet crash
        if not crashInfo['groundCrash']:
            if playerRot > -90:
                playerRot -= playerVelRot

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))

        for uplanet, lplanet, mplanet in zip(upperPlanets, lowerPlanets, middlePlanets):                            ##
            SCREEN.blit(IMAGES['planet'][0], (uplanet['x'], uplanet['y']))
            SCREEN.blit(IMAGES['planet'][1], (lplanet['x'], lplanet['y']))
            SCREEN.blit(IMAGES['planet'][2], (mplanet['x'], mplanet['y']))                                          ##

        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        SCREEN.blit(IMAGES['head'], (headx, HEAD))                                                                  ##
        showScore(score)

        


        playerSurface = pygame.transform.rotate(IMAGES['player'][1], playerRot)
        SCREEN.blit(playerSurface, (playerx,playery))
        SCREEN.blit(IMAGES['gameover'], (50, 180))                                                                   ##

        FPSCLOCK.tick(FPS)
        pygame.display.update()


def playerShm(playerShm):
    """oscillates the value of playerShm['val'] between 8 and -8"""
    if abs(playerShm['val']) == 8:
        playerShm['dir'] *= -1

    if playerShm['dir'] == 1:
         playerShm['val'] += 1
    else:
        playerShm['val'] -= 1


def getRandomplanet():
    """returns a randomly generated planet"""
    # y of gap between upper and lower planet
    gapY = random.randrange(0, int(BASEY * 0.9 - PLANETGAPSIZE))                                        ##
    gapY += int(BASEY * 0.2)                                                                            ##
    planetHeight = IMAGES['planet'][0].get_height()                                                     ##
    planetX = SCREENWIDTH + 10                                                                          ##

    return [
        {'x': planetX, 'y': gapY - planetHeight},  # upper planet
        {'x': planetX, 'y': gapY + PLANETGAPSIZE}, # lower planet
        {'x': planetX , 'y':gapY + PLANETGAPSIZE}, # middle planet              ##
    ]


def showScore(score):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0 # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH - totalWidth) / 2

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.15))                   ##
        Xoffset += IMAGES['numbers'][digit].get_width()


def checkCrash(player, upperPlanets, lowerPlanets, middlePlanets):              ##
    """returns True if player collders with base or Planets."""
    pi = player['index']
    player['w'] = IMAGES['player'][0].get_width()
    player['h'] = IMAGES['player'][0].get_height()

    # if player crashes into ground
    if player['y'] + player['h'] >= BASEY - 1:
        return [True, True]
    if player['y'] + player['h'] <= HEAD + 1:                                    ##
        return [True, True]                                                      ##
    
    else:

        playerRect = pygame.Rect(player['x'], player['y'],
                      player['w'], player['h'])
        planetW = IMAGES['planet'][0].get_width()
        planetH = IMAGES['planet'][0].get_height()

        for uplanet, lplanet, mplanet in zip(upperPlanets, lowerPlanets, middlePlanets):            ##
            # upper and lower planet rects                                                                  
            uplanetRect = pygame.Rect(uplanet['x'], uplanet['y'], planetW, planetH)
            lplanetRect = pygame.Rect(lplanet['x'], lplanet['y'], planetW, planetH)
            mplanetRect = pygame.Rect(mplanet['x'], mplanet['y'], planetW, planetH)                  ##

            # player and upper/lower planet hitmasks
            pHitMask = HITMASKS['player'][pi]
            uHitmask = HITMASKS['planet'][0]
            lHitmask = HITMASKS['planet'][1]
            mHitmask = HITMASKS['planet'][2]                                                        ##

            # if ufo collided with uplanet or lplanet
            uCollide = pixelCollision(playerRect, uplanetRect, pHitMask, uHitmask)
            lCollide = pixelCollision(playerRect, lplanetRect, pHitMask, lHitmask)
            mCollide = pixelCollision(playerRect, mplanetRect, pHitMask, mHitmask)                  ##

            if uCollide or lCollide or mCollide:                                                    ##
                return [True, False]

    return [False, False]

def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    """Checks if two objects collide and not just their rects"""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in range(rect.width):
        for y in range(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False

def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in range(image.get_width()):
        mask.append([])
        for y in range(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask

if __name__ == '__main__':
    main()
