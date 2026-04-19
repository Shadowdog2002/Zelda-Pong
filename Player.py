import pygame
UP = -1
DOWN = 1
RIGHT = 1
LEFT = -1

class Player(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int, width:int, height:int, color:pygame.Color, id:int, img_path:str = r'Sprites\Players\Link.png', dir = RIGHT):
        super().__init__()
        self.image = pygame.image.load(img_path).convert_alpha()

        self.dir =  dir
        if dir == LEFT:
            self.image = pygame.transform.flip(self.image, True, False)
        

        self.rect = pygame.Rect(x, y, width, height)
        # self.rect.topright = self.image.get_rect().topright
        self.speed = 5
        self.vel = self.speed

        self.id = id
        self.was_moving = False
    
    def draw(self, screen:pygame.Surface, debug:bool = False):
        if self.dir == RIGHT:
            screen.blit(self.image, (self.rect.x-25, self.rect.y))
        else:
            screen.blit(self.image, self.rect)
        if debug:
            color = "red" if self.was_moving else "green"
            pygame.draw.rect(screen, color, self.rect, width=2)
        
    def move(self, dir:int):
        self.vel = self.speed*dir
        self.rect.y += self.vel
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > pygame.display.get_surface().get_height():
            self.rect.bottom = pygame.display.get_surface().get_height()

    def set_speed(self, new_speed:int):
        self.vel = max(1, new_speed)

    

    def __str__(self) -> str:
        return f"Player at {self.rect}"