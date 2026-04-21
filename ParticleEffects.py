import pygame
import random

class Particle:

    def __init__(self, pos,decay = 5,color:pygame.Color = pygame.Color("orange")):
        self.pos = list(pos)
        # Random velocity to make them spread out like a trail
        self.vel = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.radius = 5
        self.lifetime = 255  # Used for transparency or color fade
        self.decay = decay
        self.color = color

    def update(self):
        # Move the particle
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        # Shrink and fade
        self.radius -= 0.1
        self.lifetime -= self.decay
    
    def is_dead(self):
        return self.lifetime<=0

    def draw(self, surface):
        # Only draw if still visible
        if self.radius > 0:
            pygame.draw.circle(surface, self.color, 
                               (int(self.pos[0]), int(self.pos[1])), 
                               int(self.radius))
            
class ParticleTrail:
    def __init__(self,decay=5,colors:list[pygame.Color] = [pygame.Color("white")],max=20) -> None:
        self.decay = decay
        self.colors = colors
        self.max = max
        self.particleArray: list[Particle] = []
    
    def add_particle(self,pos:tuple[int,int],colors:list[pygame.Color] = [],chance = 0.3,num = 1,):
        particleColors = colors if colors else self.colors
        for i in range(num):
            if random.random()<chance:
                if len(self.particleArray) >= self.max:
                    self.particleArray.pop(0)
                
                self.particleArray.append(Particle(pos,self.decay,color = random.choice(particleColors)))
    
    def update(self):
        for p in self.particleArray:
            p.update()
            if p.is_dead():
                self.particleArray.remove(p)

    def clear(self):
        self.particleArray.clear()

    def draw(self,surface):
        for p in  self.particleArray:
            p.draw(surface)
        