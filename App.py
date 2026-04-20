# Example file showing a basic pygame "game loop"
import pygame
from pygame import Color
import pygame.gfxdraw
from Player import *
from Ball import *
from Game import *
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
pause = False
MouseWheel = 0
fps = 60

#Game setup
game = Game(screen)
game.setup()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEWHEEL:
            MouseWheel = event.precise_y
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                game.debug_mode = not game.debug_mode
                print(f"Debug mode is now {game.debug_mode}")
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                game.setup()
                fps = 60
                pause = False
                print("Game reset")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause = not pause
                print(f"Game paused: {pause}")
                
    # RENDER YOUR GAME HERE
        
    if pause:
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            print("skip frame")
        else:
            continue
    
    if MouseWheel != 0:
        fps -= MouseWheel*3
        fps = int(max(1, fps))
        MouseWheel = 0
        print(f"FPS is now {fps}")
    
    game.update()
    # ball.move()

    #collision detection
    
    # if ball.reach_goal() !=0:
    #     if ball.reach_goal() == -1:
    #         print("Player 2 scores!")
    #     else:
    #         print("Player 1 scores!")

    # for player in players:
    #     if player.rect.colliderect(ball.rect):
    #         ball.bounce()
    


    #drawing objects
    game.draw()
    # for player in players:
    #     screen.blit(player.image, player.rect)
    # screen.blit(ball.image, ball.rect)    

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(fps)  # limits FPS to specified value

pygame.quit()