import pygame
from abc import ABC, abstractmethod

class Item(ABC):
    def __init__(self,rect:pygame.Rect) -> None:
        super().__init__()
        self.rect = rect
        self.image: pygame.Surface
    @abstractmethod
    def ability(self):
        pass
    def draw(self,screen:pygame.Surface):
        screen.blit(self.image,self.image.get_rect(center = self.rect.center))

    


class HylianShield(Item):
    def __init__(self, rect: pygame.Rect, img_path = "Sprites/Items/Hylian Shield.png") -> None:
        super().__init__(rect)
        self.image = pygame.image.load(img_path)

    def ability(self):
        return super().ability()

class MasterSword(Item):
    def __init__(self, rect: pygame.Rect, img_path = "Sprites/Items/Master sword.png") -> None:
        super().__init__(rect)
        self.image = pygame.image.load(img_path)

    def ability(self):
        return super().ability()