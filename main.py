from settings import *
from game import Board
import pygame

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

def main():
    run = True
    board = Board(20,  0)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        board.update()
        display(screen,board)


def display(screen,board):
    screen.fill(BROWN)
    board.display(screen)
    pygame.display.update()
    clock.tick(FPS)


main()
