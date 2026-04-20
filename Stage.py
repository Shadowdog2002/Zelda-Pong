import pygame
from  Items import *

class Stage():
    def __init__(self, screen:pygame.Surface):
        self.screen = screen.copy()
        self.screen.fill("black")
        for i in range(10, self.screen.get_height(), 20):
            pygame.draw.line(self.screen, pygame.Color("white"), (self.screen.get_width()//2, i), (self.screen.get_width()//2, i+10), width=3)

    def draw(self, screen:pygame.Surface):
        screen.blit(self.screen, (0, 0))

class BasicStage(Stage):
    def __init__(self, screen:pygame.Surface):
        super().__init__(screen)
        self.items: list[Item] = []
        self.circle_image = pygame.image.load("Sprites/Items/Items_Circle.png.png")

        itemRect = pygame.Rect(0,0,100,100)
        itemRect.center = (350,200)
        self.items.append(HylianShield(itemRect))

        itemRect = pygame.Rect(0,0,100,100)
        itemRect.center = (self.screen.get_width()-350, self.screen.get_height()-300)
        self.items.append(MasterSword(itemRect))
        
        

    def setup(self):
        self.items = []
        #create item rect, center it, and append to item list
        itemRect = pygame.Rect(0,0,100,100)
        itemRect.center = (350,200)
        self.items.append(HylianShield(itemRect))

        itemRect = pygame.Rect(0,0,100,100)
        itemRect.center = (self.screen.get_width()-350, self.screen.get_height()-300)
        self.items.append(MasterSword(itemRect))

        
    def draw(self, screen: pygame.Surface):
        for item in self.items:
            self.screen.blit(self.circle_image, self.circle_image.get_rect(center = item.rect.center))
            item.draw(self.screen)

        super().draw(screen)