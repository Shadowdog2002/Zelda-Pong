from __future__ import annotations
import pygame
from abc import ABC, abstractmethod
from typing import cast, TYPE_CHECKING
import random

if TYPE_CHECKING:
    from Ball import Ball
    from Player import Player



class StageObject(ABC):
    """
    A Stage Object that is able to be hit by ball
    Only updates when hit by ball
    """
    def __init__(self,rect:pygame.Rect) -> None:
        super().__init__()
        self.rect = rect
        self.image: pygame.Surface
        self.balls_last_collided: list[Ball] = []

    def draw(self,screen:pygame.Surface):
        screen.blit(self.image,self.image.get_rect(center = self.rect.center))
    
    def update(self):
        pass
    @abstractmethod
    def hit_by_ball(self,ball:Ball):
        if ball in self.balls_last_collided:
            return -1

class StageHazard(ABC):
    """
    A Stage Hazard that can affect players and balls
    It gets updated every frame
    """
    def __init__(self, rect: pygame.Rect,img_path:str) -> None:
        self.rect = rect
        #if path given
        if img_path:
            self.image = pygame.image.load(img_path).convert_alpha()
        
        self.image:pygame.Surface
    
    def apply_ball_effect(self, ball: Ball):
        pass

    def ball_collisions(self,balls:list[Ball]):
        pass    

    def draw(self,screen:pygame.Surface):
        screen.blit(self.image,self.image.get_rect(center = self.rect.center))
    @abstractmethod
    def update(self):
        pass    

class HylianShield(StageObject):
    def __init__(self, rect: pygame.Rect, img_path = "Sprites/Items/Hylian Shield.png") -> None:
        super().__init__(rect)
        self.image = pygame.image.load(img_path).convert_alpha()
    def hit_by_ball(self, ball: Ball):
        print("Shield hit by ball")
        return super().hit_by_ball(ball)



class MasterSword(StageObject):
    def __init__(self, rect: pygame.Rect, img_path = "Sprites/Items/Master sword.png") -> None:
        super().__init__(rect)
        self.image = pygame.image.load(img_path).convert_alpha()
    def hit_by_ball(self, ball: Ball):
        print("Sword hit by ball")
        return super().hit_by_ball(ball)


class WaterHazard(StageHazard):
    def __init__(self, rect: pygame.Rect,img_path:str = "") -> None:
        super().__init__(rect,img_path)
        self.vel = pygame.Vector2(0,0)
        self.y = self.rect.y

        #make blue water
        self.image = pygame.Surface((self.rect.size), pygame.SRCALPHA).convert_alpha()
        self.image.fill((0, 100, 255, 150))
        
        dark_blue = (0, 50, 150, 200) 
        for _ in range(200):
            x = random.randint(0, self.rect.w)
            y = random.randint(0, self.rect.h)
            radius = random.randint(2, 5)
            pygame.draw.circle(self.image, dark_blue, (x, y), radius)

    def apply_ball_effect(self, ball: Ball):
        ball.under_water = True
    def unapply_ball_effect(self,ball:Ball):
        ball.under_water = False
    def ball_collisions(self,balls:list[Ball]):
        # print("checking ball collisions")
        for ball in balls:
            if self.rect.collidepoint(ball.rect.center):
                self.apply_ball_effect(ball)
                # print("ball colliding with water")
            else:
                self.unapply_ball_effect(ball)


    def rise_by(self,y):
        if self.rect.y<=0:
            self.vel.y = 0
            return
        print("rising water")
        self.y -=y
        self.vel.y = -2
    
    def update(self):
        self.rect.move_ip(self.vel.xy)
        #if water rises higher than y stop rising.
        if self.rect.y<self.y:
            self.rect.y = max(self.y,0)
            self.vel.update(0,0)
            print("stoping the rising waters")
        if self.rect.y<0:
            self.rect.y = 0
            
        # self.image.scroll(-1,0)


        
        
class WaterCrystal(StageObject):
    """
    each player activates a WaterHazard with respect to their position in the list (Make sure to swap them)
    \nAccepts WaterHazards only
    """
    def __init__(self, rect: pygame.Rect,players:list[Player], waterHazerds:list[StageHazard],tint = (0,120,0),img_path = "Sprites/Items/Hylian Shield.png") -> None:
        super().__init__(rect)
        self.image = pygame.image.load(img_path)
        self.image.fill(tint, special_flags=pygame.BLEND_RGB_ADD)

        #store players
        self.players = players

        for h in waterHazerds:
            if not isinstance(h, WaterHazard):
                raise TypeError(f"Expected WaterHazard, got {type(h).__name__}")
        
        self.risingWaters:list[WaterHazard] = cast(list[WaterHazard], waterHazerds)
        

    def hit_by_ball(self,ball:Ball):
        #ignore balls not hit by a player
        if ball.last_hit_player is None:
            return
        #ignore if ball already hit
        if ball.last_hit_stage_object is self:
            return
        
        #update ball's last hit object
        # print("updating balls last hit")
        ball.last_hit_stage_object = self
        # print(f"WaterCrystal hit by ball by player {str(ball.last_hit_player)}")
        # print(f"players in WaterCrystal object: ",[str(p) for p in self.players])

        #find player index that hit the ball (0 or 1)
        playerIndex = self.players.index(ball.last_hit_player)
        # print(f"player {playerIndex} activated the Water Crystal")
        #rise the associated player's water
        self.risingWaters[playerIndex].rise_by(100)

    def update(self):
        pass
    
