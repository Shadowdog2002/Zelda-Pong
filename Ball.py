import pygame
from Player import *
from debug_objects import *
from ParticleEffects import *
import random
RIGHT = 1
LEFT = -1

class Ball(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int, radius:int, color:pygame.Color, vel:pygame.Vector2 = pygame.Vector2(5, 5)):
        super().__init__()
        self.image = pygame.Surface((radius, radius))
        self.image.fill(color)
        self.particles = []
        self.particleTrail = ParticleTrail(colors=["orange","red","yellow"])


        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.vel = vel
        self.last_hit_player_id = -1
        self.last_hit_player: Player|None = None 

        #tuning parameters
        self.min_vel = 7
        self.max_vel = 19
        self.xlim = 4

        #debug objects
        self.debug_vecs = []
        self.debug_points = []
    
    def draw(self, screen:pygame.Surface, debug:bool = False):
        #give a particle trail when at high magnitude
        if self.vel.magnitude()>10:
            self.image.fill("red")
            # pygame.draw.rect(self.image,random.choice(["orange","red","yellow"]),self.image.get_bounding_rect(),width=2)
            self.particleTrail.add_particle(self.rect.center,num = self.rect.bottom)
            self.particleTrail.update()
            self.particleTrail.draw(screen)
            # print(len(self.particleTrail.particleArray))
        #clear particle trail when slow
        else:
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

    def move(self):
        #limit velocity
        if abs(self.vel.x)<self.xlim:
            self.vel.x = self.xlim if self.vel.x>0 else -self.xlim
        self.vel.clamp_magnitude_ip(self.min_vel, self.max_vel)

        self.rect.centerx += int(self.vel.x)
        self.rect.centery += int(self.vel.y)

        if self.rect.top < 0 or self.rect.bottom > pygame.display.get_surface().get_height():
            self.vel.y *= -1
        
        self.debug_points.append(PointDebug(self.rect.center))

    def bounce(self, player:Player):
        # prevent ball from bouncing multiple times on the same player
        if player is self.last_hit_player and player is not None:
            print(f"same player object hit {player.id}")
            return
        self.last_hit_player = player

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
        self.debug_vecs.extend([VectorDebug(self.rect.center, self.vel,scale=5), VectorDebug(self.rect.center, vec_to_player, pygame.Color("yellow"))])


    
    def reach_goal(self):
        if self.rect.left < 0:
            return -1
        elif self.rect.right > pygame.display.get_surface().get_width():
            return 1
        else:
            return 0

    def __str__(self) -> str:
        return f"Ball Velocity: {self.vel}\n Magnitude:{self.vel.magnitude()} Position {self.rect.center}"