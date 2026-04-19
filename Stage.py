import pygame


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
        
    def draw(self, screen: pygame.Surface):
        def draw_dotted_circle(screen, color, center, radius, width=2, dots=10):
            for i in range(0, 314*2, (314*2)//dots):
                pygame.draw.arc(screen, "white",(center[0],center[1],radius,radius),0.01*i,0.01*(i+20), width=width)
        
        draw_dotted_circle(self.screen, "white", (250, 200), 100, width=2, dots=10)
        draw_dotted_circle(self.screen, "white", (screen.get_width()-350, screen.get_height()-300), 100, width=2, dots=10)

        super().draw(screen)    