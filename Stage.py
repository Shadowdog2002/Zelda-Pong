import pygame
from  StageObjects import *
from Ball import *

class Stage():
    def __init__(self, screen:pygame.Surface,players:list[Player]):
        #blank screen
        self.screen = screen.copy()
        self.stageObjetcs: list[StageObject] = []
        self.stageHazards: list[StageHazard] = []
        self.screen.fill("black")
        self.players = players

    def setup(self,players:list[Player]):
        self.screen.fill("black")

        self.stageObjetcs: list[StageObject] = []
        self.stageHazards: list[StageHazard] = []
        self.players = players
        
    def draw(self, screen:pygame.Surface):
        screen.blit(self.screen, (0, 0))
    
    def update(self):
        pass

    def stageObjectCollisions(self,balls:list[Ball]):
        #loop through all stage objects
        for stageObject in self.stageObjetcs:
            #get balls that hit the current StageObject
            balls_collided_with_stageObject = stageObject.rect.collideobjectsall(balls,key = lambda o:o.rect)
            #only save balls that havent hit this object last
            valid_balls_collided_with_stageObject = []
            for ball in balls_collided_with_stageObject:
                    if ball.last_hit_stage_object is not stageObject and ball.last_hit_player is not None:
                        valid_balls_collided_with_stageObject.append(ball)
                    #update every ball's last hit stage object to this one
                    # ball.last_hit_stage_object = stageObject
            stageObject.balls_last_collided.extend(balls_collided_with_stageObject)#maybe delete
            
            #for each valid ball trigger the StageObject
            for ball in valid_balls_collided_with_stageObject:
                stageObject.hit_by_ball(ball)
    def stageHazardCollisions(self,balls:list[Ball]):
        # for hazard in self.stageHazards:
        #     hazard.ball_collisions(balls=balls)
        for ball in balls:
            ball.stageHazardCollisions(self.stageHazards)

class BasicStage(Stage):
    def __init__(self, screen:pygame.Surface,players:list[Player]):
        super().__init__(screen,players=players)
        #draw dotted line down the middle
        for i in range(10, self.screen.get_height(), 20):
            pygame.draw.line(self.screen, pygame.Color("white"), (self.screen.get_width()//2, i), (self.screen.get_width()//2, i+10), width=3)
        #Item spaces
        self.circle_image = pygame.image.load("Sprites/Items/Items_Circle.png.png")

        self.setup(players=self.players)
        
        

    def setup(self,players:list[Player]):
        super().setup(players=players)

        #create item rect, center it, and append to item list
        itemRect = pygame.Rect(0,0,100,100)
        itemRect.center = (350,200)
        self.stageObjetcs.append(HylianShield(itemRect))

        itemRect = pygame.Rect(0,0,100,100)
        itemRect.center = (self.screen.get_width()-350, self.screen.get_height()-300)
        self.stageObjetcs.append(MasterSword(itemRect))

        
    def draw(self, screen: pygame.Surface):
        for stageObject in self.stageObjetcs:
            self.screen.blit(self.circle_image, self.circle_image.get_rect(center = stageObject.rect.center))
            stageObject.draw(self.screen)

        for stageHazard in self.stageHazards:
            stageHazard.draw(self.screen)        

        super().draw(screen)

class WaterStage(Stage):
    def __init__(self, screen: pygame.Surface,players:list[Player]):
        super().__init__(screen,players=players)
        #Top half of the line down the middle
        for i in range(10, self.screen.get_height()//2 - 50, 20):
            pygame.draw.line(self.screen, pygame.Color("white"), (self.screen.get_width()//2, i), (self.screen.get_width()//2, i+10), width=3)
        for i in range(self.screen.get_height()//2+60, self.screen.get_height(), 20):
            pygame.draw.line(self.screen, pygame.Color("white"), (self.screen.get_width()//2, i), (self.screen.get_width()//2, i+10), width=3)
        #Item spaces
        self.circle_image = pygame.image.load("Sprites/Items/Items_Circle.png.png")

        self.setup(players=self.players)

    def setup(self,players:list[Player]):
        super().setup(players=self.players)
        self.players = players

        #create StageHazard rect and append to StageHazard list
        hazardRect = pygame.Rect(0,self.screen.get_height(),self.screen.get_width()//2,self.screen.get_height())
        self.stageHazards.append(WaterHazard(hazardRect)) #left player water

        hazardRect = pygame.Rect(self.screen.get_width()//2,self.screen.get_height(),self.screen.get_width()//2,self.screen.get_height())
        self.stageHazards.append(WaterHazard(hazardRect)) #right player water
        
        #create StageObject rect, center it, and append to StageObject list
        itemRect = pygame.Rect(0,0,100,100)
        itemRect.center = (self.screen.get_width()//2,self.screen.get_height()//2)
        self.stageObjetcs.append(WaterCrystal(itemRect,
                                              waterHazerds = [self.stageHazards[1],self.stageHazards[0]],#made sure to swap them so each player controls the other player's water
                                              players=self.players))

    def draw(self, screen: pygame.Surface):
        for item in self.stageObjetcs:
            self.screen.blit(self.circle_image, self.circle_image.get_rect(center = item.rect.center))
            item.draw(self.screen)
        for hazard in self.stageHazards:
            hazard.draw(self.screen)

        super().draw(screen)

    def update(self):
        for stageHazard in self.stageHazards:
            stageHazard.update()

        # print("water hazard left",self.stageHazards[0].rect.top,"/",self.stageHazards[0].y, self.stageHazards[0].vel)