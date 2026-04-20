import pygame
import pygame.gfxdraw
from Player import *
from Ball import *
from Stage import *
from debug_objects import *
import math

class Game():
    def __init__(self, screen:pygame.Surface):
        self.screen = screen
        print(self.screen.get_rect())
        self.screenRect = self.screen.get_rect()
        self.players: list[Player] = []
        self.balls: list[Ball] = []
        self.score = [0, 0]
        self.stage = BasicStage(screen)

        self.debug_vecs = []
        self.debug_points = []
        self.debug_texts = []

        self.debug_mode = False

    def setup(self):
        self.players = []
        self.balls = []
        self.debug_vecs = []
        self.debug_points = []
        self.debug_texts = []

        self.stage.setup()

        self.players.append(Player(self.screenRect.w//20, self.screenRect.h//2, 
                      25,100, 
                      pygame.Color("white"), 0, dir=RIGHT, img_path = 'Sprites/Players/Link.png'))
        self.players.append(Player(self.screenRect.w - self.screenRect.w//20 - 20, self.screenRect.h//2, 
                      25,100, 
                      pygame.Color("white"), 1, dir=LEFT, img_path = 'Sprites/Players/Zelda.png'))

        self.balls.append(Ball(self.screenRect.w//2, self.screenRect.h//2, 10, pygame.Color("white"), pygame.Vector2(5, -5)))
    
        self.score = [0, 0]
        self.score_text1 = TextDebug(f"{self.score[0]}", (self.players[0].rect.left, 10),font_size=40,font_name="consolas")

        self.score_text2 = TextDebug(f"{self.score[1]}", (self.players[1].rect.left, 10),font_size=40,font_name="consolas")



    def update(self):

        keys = pygame.key.get_pressed()
        #player movement
        if keys[pygame.K_UP]:
            self.players[1].move(UP)
            self.players[1].was_moving = True
        elif keys[pygame.K_DOWN]:
            self.players[1].move(DOWN)
            self.players[1].was_moving = True
        else:
            self.players[1].was_moving = False
        
        if keys[pygame.K_w]:
            self.players[0].move(UP)
            self.players[0].was_moving = True
        elif keys[pygame.K_s]:
            self.players[0].move(DOWN)
            self.players[0].was_moving = True
        else:
            self.players[0].was_moving = False

        #ball control
        if keys[pygame.K_m]:
            self.balls.append(Ball(self.screenRect.w//2, self.screenRect.h//2, 10, pygame.Color("white"), pygame.Vector2(random.randint(-8,8), random.randint(-8,8))))
        for ball in self.balls:
            if keys[pygame.K_l]:
                ball.vel.rotate_ip(5)
            if keys[pygame.K_k]:
                ball.vel.rotate_ip(-5)

        #Move Balls
        for ball in self.balls:
            ball.move()


        #collision detection
        for ball in self.balls:
            if ball.reach_goal() !=0:
                if ball.reach_goal() == -1: #Right side goal
                    self.score[1] += 1
                else:                       #Left side goal
                    self.score[0] += 1
                print(f"Score: {self.score}")
                self.score_text1.text = f"{self.score[0]}"
                self.score_text2.text = f"{self.score[1]}"
                
                self.balls.remove(ball)
                self.balls.append(Ball(self.screenRect.w//2, self.screenRect.h//2, 10, pygame.Color("white"), pygame.Vector2(random.randint(-8,8), random.randint(-8,8))))
        for ball in self.balls:
            playerCollided = ball.rect.collideobjects(self.players, key = lambda o: o.rect)
            if playerCollided is not None:        #Any collisions found
                ball.bounce(playerCollided)

    def draw(self):
        self.stage.draw(self.screen)
        

        #draw score
        self.score_text1.draw(self.screen)
        self.score_text2.draw(self.screen)

        for player in self.players:
            player.draw(self.screen, debug=self.debug_mode)
        for ball in self.balls:
            ball.draw(self.screen, debug=self.debug_mode)
        

        #drawing debugging objects
        if self.debug_mode:
            # for vec in self.debug_vecs:
            #     vec.draw(self.screen)
            # for point in self.debug_points:
            #     point.draw(self.screen)

            #debug texts
            if len(self.debug_vecs) >= 4:
                TextDebug(f"impact 1: {self.debug_vecs[0].vec/self.debug_vecs[0].scale}  toPlayer 1: {self.debug_vecs[1].vec/self.debug_vecs[1].scale}, Angle: {self.debug_vecs[0].vec.angle_to(self.debug_vecs[1].vec)}", (self.players[0].rect.left, 30)).draw(self.screen)
                TextDebug(f"impact 2: {self.debug_vecs[2].vec/self.debug_vecs[2].scale}  toPlayer 2: {self.debug_vecs[3].vec/self.debug_vecs[3].scale}, Angle: {self.debug_vecs[2].vec.angle_to(self.debug_vecs[3].vec)}", (self.players[0].rect.left, 50)).draw(self.screen)
            for text in self.debug_texts:
                text.draw(self.screen)
            if self.balls is not []:
                TextDebug(str(self.balls[0]), (self.players[0].rect.left, self.screenRect.h - 60)).draw(self.screen)