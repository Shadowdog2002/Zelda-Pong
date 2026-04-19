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
        self.players = []
        self.ball:  Ball|None = None
        self.score = [0, 0]
        self.stage = BasicStage(screen)

        self.debug_vecs = []
        self.debug_points = []
        self.debug_texts = []

        self.debug_mode = False

    def setup(self):
        self.players = []
        self.debug_vecs = []
        self.debug_points = []
        self.debug_texts = []

        self.players.append(Player(self.screen.get_width()//20, self.screen.get_height()//2, 
                      25,100, 
                      pygame.Color("white"), 0, dir=RIGHT))
        self.players.append(Player(self.screen.get_width() - self.screen.get_width()//20 - 20, self.screen.get_height()//2, 
                      25,100, 
                      pygame.Color("white"), 1, dir=LEFT))

        self.ball = Ball(self.screen.get_width()//2, self.screen.get_height()//2, 10, pygame.Color("white"), pygame.Vector2(5, 5))
    
        self.score = [0, 0]
        self.score_text1 = TextDebug(f"{self.score[0]}", (self.players[0].rect.left, 10),font_size=40,font_name="consolas")

        self.score_text2 = TextDebug(f"{self.score[1]}", (self.players[1].rect.left, 10),font_size=40,font_name="consolas")



    def update(self):
        if self.ball is None:
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.players[0].move(UP)
            self.players[0].was_moving = True
        elif keys[pygame.K_DOWN]:
            self.players[0].move(DOWN)
            self.players[0].was_moving = True
        else:
            self.players[0].was_moving = False
        
        if keys[pygame.K_w]:
            self.players[1].move(UP)
            self.players[1].was_moving = True
        elif keys[pygame.K_s]:
            self.players[1].move(DOWN)
            self.players[1].was_moving = True
        else:
            self.players[1].was_moving = False

        if keys[pygame.K_l]:
            self.ball.vel.rotate_ip(5)
        if keys[pygame.K_k]:
            self.ball.vel.rotate_ip(-5)

        #debugging vector
        self.ball.move()
        self.debug_points.append(PointDebug(self.ball.rect.center))

        #collision detection
        if self.ball.reach_goal() !=0:
            if self.ball.reach_goal() == -1:
                self.score[1] += 1
            else:
                self.score[0] += 1
            print(f"Score: {self.score}")
            self.score_text1.text = f"{self.score[0]}"
            self.score_text2.text = f"{self.score[1]}"

            self.ball.rect.center = (self.screen.get_width()//2, self.screen.get_height()//2)
            self.ball.vel = pygame.Vector2(5 * (-1 if self.ball.vel.x < 0 else 1), 5)

        playerCollided = self.ball.rect.collidelist(self.players)
        if playerCollided != -1:
            player = self.players[playerCollided]
            
            #debugging vector
            self.ball.bounce(player)


    def draw(self):
        self.stage.draw(self.screen)
        

        #draw score
        self.score_text1.draw(self.screen)
        self.score_text2.draw(self.screen)

        for player in self.players:
            player.draw(self.screen, debug=self.debug_mode)
        if self.ball is not None:
            self.ball.draw(self.screen, debug=self.debug_mode)
        

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
            if self.ball is not None:
                TextDebug(f"Ball velocity: {self.ball.vel.magnitude()}", (self.players[0].rect.left, self.screen.get_height() - 30)).draw(self.screen)
