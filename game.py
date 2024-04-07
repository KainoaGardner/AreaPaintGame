import pygame
import numpy as np
from settings import *

pygame.font.init()

class Board:
    def __init__(self,size,turn):
        self.board = np.zeros((size,size),dtype=np.int32)
        self.tileSize = (WIDTH - MARGINSIZE * 2) // len(self.board)
        self.turn = turn
        self.p1Pos = (0,len(self.board)//2)
        self.p2Pos = (len(self.board[0]) - 1,len(self.board)//2)
        self.board[self.p1Pos[1],self.p1Pos[0]] = 1
        self.board[self.p2Pos[1],self.p2Pos[0]] = 2
        self.p1Direction = (0,0)
        self.p2Direction = (0,0)
        self.p1Score = 0
        self.p2Score = 0
        self.gameCount = 0
        self.gameSpeed = 10

        self.validFlood1 = []
        self.validFlood2 = []
        self.visitedTiles = []
        self.stopFlood = False

        self.scoreFont = pygame.font.Font("font/LEMONMILK-Regular.otf",MARGINSIZE)

    def move(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_t]:
            self.turn = 0
        if keys[pygame.K_y]:
            self.turn = 1
        
        if self.turn == 0:
            if keys[pygame.K_UP]:
                self.p1Direction = (0,-1)
            if keys[pygame.K_DOWN]:
                self.p1Direction = (0,1)
            if keys[pygame.K_LEFT]:
                self.p1Direction = (-1,0)
            if keys[pygame.K_RIGHT]:
                self.p1Direction = (1,0)

        elif self.turn == 1:
            if keys[pygame.K_UP]:
                self.p2Direction = (0,-1)
            if keys[pygame.K_DOWN]:
                self.p2Direction = (0,1)
            if keys[pygame.K_LEFT]:
                self.p2Direction = (-1,0)
            if keys[pygame.K_RIGHT]:
                self.p2Direction = (1,0)
    
    def fillValidTile(self,x,y,player,newColor):
        if x < 0 or x >= len(self.board[0]) or y < 0 or y >= len(self.board) : 
            self.stopFlood = True
            return False
        elif self.board[y][x] == newColor or self.board[y][x] == player or (x,y) in self.visitedTiles:
            return False
        return True
    
    def floodFill(self,x,y,player,newColor):
        queue = []
        possibleTiles = []
        if (x,y) not in self.visitedTiles:
            queue.append((x,y))
            possibleTiles.append((x,y))
            self.visitedTiles.append((x,y))
        while queue:
            if self.stopFlood == True:
               return None
            currrentTile = queue.pop()
            posx = currrentTile[0]
            posy = currrentTile[1]
            
            if self.fillValidTile(posx - 1,posy,player,newColor):
                possibleTiles.append((posx - 1,posy))
                queue.append((posx - 1,posy))
                self.visitedTiles.append((posx - 1,posy))
            if self.fillValidTile(posx,posy - 1,player,newColor):
                possibleTiles.append((posx,posy - 1))
                queue.append((posx,posy - 1))
                self.visitedTiles.append((posx,posy - 1))
            if self.fillValidTile(posx + 1,posy,player,newColor):
                possibleTiles.append((posx + 1,posy))
                queue.append((posx + 1,posy))
                self.visitedTiles.append((posx + 1,posy))
            if self.fillValidTile(posx,posy + 1,player,newColor):
                possibleTiles.append((posx,posy + 1))
                queue.append((posx,posy + 1))
                self.visitedTiles.append((posx,posy + 1))

        if self.stopFlood == True:
            return None
        else:
            return possibleTiles

    def checkForFlood(self):
        if self.gameCount % self.gameSpeed == 0:
            p1Directions = [(self.p1Pos[0] - 1,self.p1Pos[1] - 1),(self.p1Pos[0] - 1,self.p1Pos[1] + 1),(self.p1Pos[0] + 1,self.p1Pos[1] - 1),(self.p1Pos[0] + 1,self.p1Pos[1] + 1)]
            p2Directions = [(self.p2Pos[0] - 1,self.p2Pos[1] - 1),(self.p2Pos[0] - 1,self.p2Pos[1] + 1),(self.p2Pos[0] + 1,self.p2Pos[1] - 1),(self.p2Pos[0] + 1,self.p2Pos[1] + 1)]

            for direction in p1Directions:               
                self.stopFlood = False
                self.visitedTiles.clear()
                outPut = self.floodFill(direction[0],direction[1],1,3)
                if outPut:
                    for tile in outPut:
                        if tile not in self.validFlood1:
                            self.validFlood1.append(tile)

            for direction in p2Directions: 
                self.stopFlood = False
                self.visitedTiles.clear()
                outPut2 = self.floodFill(direction[0],direction[1],2,4)
                if outPut2:
                    for tile in outPut2:
                        if tile not in self.validFlood2:
                            self.validFlood2.append(tile)

            if self.validFlood1 != []:
                for tile in self.validFlood1:
                    self.board[tile[1],tile[0]] = 3
            self.validFlood1 = []

            if self.validFlood2 != []:
                for tile in self.validFlood2:
                    self.board[tile[1],tile[0]] = 4
            self.validFlood2 = []



    def getScore(self):
        if self.gameCount % self.gameSpeed == 0:
            p1Score = 0
            p2Score = 0
            for r in range(len(self.board)):
                for c in range(len(self.board[r])):
                    if self.board[r][c] == 1 or self.board[r][c] == 3:
                        p1Score += 1
                    elif self.board[r][c] == 2 or self.board[r][c] == 4:
                        p2Score += 1
            self.p1Score = p1Score
            self.p2Score = p2Score


    def update(self):
        self.getScore()
        self.checkForFlood()
        self.move()
        if self.gameCount % self.gameSpeed == 0:
            if self.p1Direction != (0,0):
                if 0 <= self.p1Pos[0] + self.p1Direction[0] < len(self.board[0]) and 0 <= self.p1Pos[1] + self.p1Direction[1] < len(self.board):
                    if self.board[self.p1Pos[1] + self.p1Direction[1]][self.p1Pos[0] + self.p1Direction[0]] != 2:
                        self.board[self.p1Pos[1] + self.p1Direction[1]][self.p1Pos[0] + self.p1Direction[0]] = 1
                        self.board[self.p1Pos[1]][self.p1Pos[0]] = 3
                        self.p1Pos = (self.p1Pos[0] + self.p1Direction[0],self.p1Pos[1] + self.p1Direction[1])
            if self.p2Direction != (0,0):
                if 0 <= self.p2Pos[0] + self.p2Direction[0] < len(self.board[0]) and 0 <= self.p2Pos[1] + self.p2Direction[1] < len(self.board):
                    if self.board[self.p2Pos[1] + self.p2Direction[1]][self.p2Pos[0] + self.p2Direction[0]] != 1:
                        self.board[self.p2Pos[1] + self.p2Direction[1]][self.p2Pos[0] + self.p2Direction[0]] = 2
                        self.board[self.p2Pos[1]][self.p2Pos[0]] = 4
                        self.p2Pos = (self.p2Pos[0] + self.p2Direction[0],self.p2Pos[1] + self.p2Direction[1])
        self.gameCount += 1
    

    def displayScore(self,screen):
        p1ScoreText = self.scoreFont.render(str(self.p1Score),True,DARKRED)
        p2ScoreText = self.scoreFont.render(str(self.p2Score),True,DARKBLUE)
        screen.blit(p1ScoreText,(WIDTH // 2 - p1ScoreText.get_width() // 2,MARGINSIZE // 2 - p1ScoreText.get_height() //2))
        screen.blit(p2ScoreText,(WIDTH // 2 - p2ScoreText.get_width() // 2,HEIGHT - MARGINSIZE // 2 - p2ScoreText.get_height() //2))

    def display(self,screen):
        self.displayScore(screen)
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r,c] == 0:
                    pygame.draw.rect(screen,LIGHTBROWN,(MARGINSIZE + c * self.tileSize,MARGINSIZE + r * self.tileSize,self.tileSize,self.tileSize))
                elif self.board[r,c] == 1:
                    pygame.draw.rect(screen,RED,(MARGINSIZE + c * self.tileSize,MARGINSIZE + r * self.tileSize,self.tileSize,self.tileSize))
                    pygame.draw.rect(screen,DARKRED,(MARGINSIZE + c * self.tileSize,MARGINSIZE + r * self.tileSize,self.tileSize,self.tileSize),5)
                elif self.board[r,c] == 2:
                    pygame.draw.rect(screen,BLUE,(MARGINSIZE + c * self.tileSize,MARGINSIZE + r * self.tileSize,self.tileSize,self.tileSize))
                    pygame.draw.rect(screen,DARKBLUE,(MARGINSIZE + c * self.tileSize,MARGINSIZE + r * self.tileSize,self.tileSize,self.tileSize),5)

                elif self.board[r,c] == 3:
                    pygame.draw.rect(screen,LIGHTRED,(MARGINSIZE + c * self.tileSize,MARGINSIZE + r * self.tileSize,self.tileSize,self.tileSize))
                elif self.board[r,c] == 4:
                    pygame.draw.rect(screen,LIGHTBLUE,(MARGINSIZE + c * self.tileSize,MARGINSIZE + r * self.tileSize,self.tileSize,self.tileSize))



