import pygame
from pygame import Color
from Player import *
from debug_objects import *
from ParticleEffects import *
from StageObjects import *
import random
RIGHT = 1
LEFT = -1

class Ball(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int, radius:int, color:pygame.Color, vel:pygame.Vector2 = pygame.Vector2(5, 5)):
        super().__init__()
        #visual
        self.image = pygame.Surface((radius, radius))
        self.image.fill(color)
        self.particleTrail = ParticleTrail(colors=[Color("orange"),Color("red"),Color("yellow")],max=20)

        #collision
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        #tracking vars
        self.vel = vel
        self.last_hit_player_id = -1
        self.last_hit_player: Player|None = None 
        self.last_hit_stage_object: StageObject|None = None
        self.is_flaming: bool = False
        self.under_water: bool = False

        #tuning parameters
        self.min_vel = 7
        self.max_vel = 19
        self.xlim = 4

        #debug objects
        self.debug_vecs = []
        self.debug_points = []
        self.max_debug_points = 1000
    
    def draw(self, screen:pygame.Surface, debug:bool = False):
        #give a particle trail when at high magnitude
        if self.vel.magnitude()>10:
            self.is_flaming = True
        if self.is_flaming:
            ball_color = Color("red")
            #default particle colors
            particle_colors = []
            #turn white if underwater
            if self.under_water:
                print("ball underwater")
                particle_colors = [Color("white")]
                ball_color = Color("white")
            self.image.fill(ball_color)
            self.particleTrail.add_particle(self.rect.center, chance=.7,colors=particle_colors)
            self.particleTrail.update()
            self.particleTrail.draw(screen)
        #clear particle trail when slow
        else:
            self.is_flaming = False
            self.particleTrail.clear()
            self.image.fill("white")
        screen.blit(self.image, self.rect)

        #debug vectors
        if debug:
            VectorDebug(pos=self.rect.center, vec=self.vel, scale=5,color=pygame.Color("blue")).draw(screen)
            for vec in self.debug_vecs:
                vec.draw(screen)
            for point in self.debug_points:
                point.draw(screen)

    def stageHazardCollisions(self,stageHazards:list[StageHazard]):
        #get hazards colliding with the ball
        under_water = False
        collidingHazards = self.rect.collideobjectsall(stageHazards,key=lambda o:o.rect)
        for hazard in collidingHazards:
            if isinstance(hazard,WaterHazard):
                under_water = True
        self.under_water = under_water




    def move(self):
        #limit velocity
        if abs(self.vel.x)<self.xlim:
            self.vel.x = self.xlim if self.vel.x>0 else -self.xlim
        self.vel.clamp_magnitude_ip(self.min_vel, self.max_vel)

        #apply effects
        final_vel = pygame.Vector2(0,0)
        #slow under water
        if self.under_water:
            # print("ball under water")
            final_vel = self.vel.copy()
            final_vel.scale_to_length(self.vel.length()*.7)
        #no effect
        else:
            # print("ball in air")
            final_vel = self.vel

        #move ball
        self.rect.centerx += int(final_vel.x)
        self.rect.centery += int(final_vel.y)

        if self.rect.top < 0 or self.rect.bottom > pygame.display.get_surface().get_height():
            self.vel.y *= -1
        

        #debug
        if len(self.debug_points)>self.max_debug_points:
            self.debug_points.pop()
        # self.debug_points.append(PointDebug(self.rect.center))

    def bounce(self, player:Player):
        # prevent ball from bouncing multiple times on the same player
        if player is self.last_hit_player and player is not None:
            print(f"same player object hit {player.id}")
            return
        self.last_hit_player = player

        # reset last hit object
        self.last_hit_stage_object = None

        
        vec_to_player = pygame.Vector2(player.rect.center) - pygame.Vector2(self.rect.center)

        #change velocity based on where it hit the player (tips=higher, middle=lower)
        self.vel.y -= (vec_to_player.y/100)*self.vel.length()
        self.vel.x *= -1.05
        self.vel.scale_to_length(self.vel.length()*1.03)

        #increase magnitude and change angle based on player vertical movement
        if player.was_moving:
            lenght_before = self.vel.length()
            self.vel.y += (player.vel)/2
            self.vel.scale_to_length(lenght_before*1.1)
            print(f"Player was moving, adding extra {player.vel} to ball velocity")

        #debug vectors
        # self.debug_vecs.extend([VectorDebug(self.rect.center, self.vel,scale=5), VectorDebug(self.rect.center, vec_to_player, pygame.Color("yellow"))])


    
    def reach_goal(self):
        if self.rect.left < 0:
            return -1
        elif self.rect.right > pygame.display.get_surface().get_width():
            return 1
        else:
            return 0

    def __str__(self) -> str:
        return f"Ball Velocity: {self.vel}\n Magnitude:{self.vel.magnitude()} Position {self.rect.center}"