import pygame
import numpy as np

class Food:

    def __init__(self, size = 5, color = (0, 255, 0),location = (0, 0)):
        self.size = size
        self.color = color
        self.location = location

    def showFood(self, game =  None):
        if game == None:
            raise 'No Game to display.!'
            quit()
        pygame.draw.circle(game, self.color, self.location, self.size)
        

class snake:
    
    def __init__(self, length = 1, size = 8, color = (0, 255, 255), x = 0, y = 0):
        self.length = length
        self.size = size
        self.color = color
        self.headX = x
        self.headY = y
        self.snakeCords = []
        for i in range(self.length): self.snakeCords.insert(0, (self.headX, self.headY - 2*i*self.size))
        self.headY -= 2*(self.length-1)*self.size
        self.speed = self.size
        self.dead = False

    def updatePosition(self):
        if len(self.snakeCords) > 1: 
            if self.snakeCords[1] == (self.headX,self.headY): 
                self.dead = True 
                self.color = (255, 0, 0)
        self.snakeCords.insert(0, (self.headX,self.headY))
        if len(self.snakeCords) > self.length: del self.snakeCords[-1]

    def eatenItSelf(self):
        for pos in self.snakeCords[1:]:
            if pos == self.snakeCords[0]:
                self.dead = True
                self.color = (255, 0, 0)
        return False

    def moveLeft(self): self.headX -= self.speed
    def moveRight(self): self.headX += self.speed
    def moveDown(self): self.headY += self.speed
    def moveUp(self): self.headY -= self.speed

    def showSnake(self, game = None, color = (255, 255, 255)):
        if game == None:
            raise 'No Game to display.!'
            quit()
        for pos in self.snakeCords: pygame.draw.circle(game, self.color, pos, self.size)

        

class game:

    def __init__(self, gameWidth = 400, gameHeight = 400):
        pygame.init()
        self.gameWidth = gameWidth
        self.gameHeight = gameHeight
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BACKGROUND = (51, 51, 51)
        self.player = snake(x = np.random.randint(low = 50, high = self.gameWidth-50), y = np.random.randint(low = 50, high = self.gameHeight - 50))
        self.display = pygame.display.set_mode((self.gameWidth, self.gameHeight))
        pygame.display.set_caption('Snake')
        self.fps = pygame.time.Clock()
        self.score = 0
        self.frameRate = 30
        self.reward = Food(location = (np.random.randint(50, self.gameWidth- 50), np.random.randint(50, self.gameHeight - 50)))

    def makeobjMsg(self, msg, fontD,color = (0, 0, 0)):
        return fontD.render(msg, True, color), fontD.render(msg, True, color).get_rect()
        
    def message(self, msg, color = (0, 0, 0), fontType = 'freesansbold.ttf', fontSize = 15, xpos = 10, ypos = 10):
        fontDefination = pygame.font.Font(fontType, fontSize)
        msgSurface, msgRectangle = self.makeobjMsg(msg, fontDefination, color)
        msgRectangle = (xpos, ypos)
        self.display.blit(msgSurface, msgRectangle)

    def pauseGame(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_r:
                        return
            self.message(msg = 'PAUSED.!',color = self.WHITE, fontSize = 30, xpos = self.gameWidth // 2 - 50, ypos = self.gameHeight // 2)
            pygame.display.update()


    def playGame(self):
        left = right = up = down = False
        while not self.player.dead:
            
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pauseGame()
                    if event.key == pygame.K_DOWN: 
                        down = True
                        up = left = right = False
                    elif event.key == pygame.K_UP: 
                        up = True
                        down = left = right = False
                    elif event.key == pygame.K_LEFT: 
                        left = True
                        up = down = right = False
                    elif event.key == pygame.K_RIGHT:
                        right = True
                        up = down = left = False

                '''if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN: down = False
                    elif event.key == pygame.K_UP: up = False
                    elif event.key == pygame.K_LEFT: left = False
                    elif event.key == pygame.K_RIGHT: right = False'''

            if left: self.moveLeft()
            elif right: self.moveRight()
            elif up: self.moveUp()
            elif down: self.moveDown()
            self.display.fill(self.BACKGROUND)
            self.showGame()
            if self.foodEaten():
                self.player.length += 1
                self.moveFood()
                self.score += 1
            self.message('Score = '+str(self.score), color = self.WHITE)
            pygame.display.update()
            self.fps.tick(self.frameRate)
        

    def moveFood(self): self.reward.location = (np.random.randint(low = 50, high = self.gameWidth-50), np.random.randint(low = 50, high = self.gameHeight-50))
    
    def foodEaten(self):
        fx, fy = self.reward.location
        sx, sy = self.player.headX, self.player.headY
        if (sx - self.player.size < fx - self.reward.size < sx + self.player.size or sx - self.player.size < fx + self.reward.size < sx + self.player.size)\
           and (sy - self.player.size < fy-self.reward.size < sy + self.player.size or sy - self.player.size < fy+self.reward.size < sy + self.player.size): return True
        return False
    
    def showGame(self):
        self.player.showSnake(self.display,self.BLACK)
        self.reward.showFood(self.display)
        
    def moveLeft(self):
        self.player.moveLeft()
        if self.player.headX - self.player.size < 0: 
            self.player.headX = self.player.size 
            self.player.dead = True #self.player.headX = self.gameWidth - self.player.size
            self.player.color = (255, 0, 0)
        self.player.updatePosition()
        self.player.eatenItSelf()

    def moveRight(self):
        self.player.moveRight()
        if self.player.headX + self.player.size > self.gameWidth:
            self.player.headX = self.gameWidth - self.player.size 
            self.player.dead = True #self.player.headX = self.player.size
            self.player.color = (255, 0, 0)
        self.player.updatePosition()
        self.player.eatenItSelf()

    def moveDown(self):
        self.player.moveDown()
        if self.player.headY + self.player.size > self.gameHeight: 
            self.player.headY = self.gameHeight - self.player.size 
            self.player.dead = True #self.player.headY = self.player.size
            self.player.color = (255, 0, 0)
        self.player.updatePosition()
        self.player.eatenItSelf()

    def moveUp(self):
        self.player.moveUp()
        if self.player.headY - self.player.size < 0:
            self.player.headY = self.player.size 
            self.player.dead = True #self.gameHeight - self.player.size
            self.player.color = (255, 0, 0)
        self.player.updatePosition()
        self.player.eatenItSelf()

if __name__ == '__main__':
    g = game()
    g.playGame()
    pygame.quit()      