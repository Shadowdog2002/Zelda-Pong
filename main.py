import pygame
from Game import *
import asyncio

pygame.init()
pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

async def main():
    running = True
    pause = False
    MouseWheel = 0
    fps = 60

    game = Game(pygame.display.get_surface())
    game.setup()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEWHEEL:
                MouseWheel = event.precise_y
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    game.debug_mode = not game.debug_mode
                    print(f"Debug mode is now {game.debug_mode}")
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    game.setup()
                    fps = 60
                    pause = False
                    print("Game reset")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = not pause
                    print(f"Game paused: {pause}")

        if pause:
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                print("skip frame")
            else:
                await asyncio.sleep(0)
                continue

        if MouseWheel != 0:
            fps -= MouseWheel*3
            fps = int(max(1, fps))
            MouseWheel = 0
            print(f"FPS is now {fps}")

        game.update()

        game.draw()

        pygame.display.flip()

        clock.tick(fps)
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())
