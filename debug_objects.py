import pygame

class VectorDebug():
    def __init__(self, pos:tuple, vec:pygame.Vector2, 
                 color:pygame.Color = pygame.Color("red"), width:int = 2, scale:float = 1):
        self.pos = pos
        self.vec = vec * scale
        self.color = color
        self.width = width
        self.scale = scale

    def draw(self, screen:pygame.Surface):
        pygame.draw.line(screen, self.color, self.pos, (self.pos[0] + self.vec.x, self.pos[1] + self.vec.y), self.width)

class PointDebug():
    def __init__(self, pos:tuple, color:pygame.Color = pygame.Color("orange"), radius:int = 1):
        self.pos = pos
        self.color = color
        self.radius = radius

    def draw(self, screen:pygame.Surface):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)

class TextDebug():
    def __init__(self, text:str, pos:tuple, color:pygame.Color = pygame.Color("white"), font_size:int = 20, font_name:str|None = None):
        self.text = text
        self.pos = pos
        self.color = color
        self.font_size = font_size
        self.font = pygame.font.SysFont(font_name, self.font_size)

    def draw(self, screen:pygame.Surface):
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, self.pos)