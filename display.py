import pygame

class Display:
    def __init__(self, scale=10):
        self.width = 64
        self.height = 32
        self.scale = scale
        self.screen = pygame.display.set_mode((self.width * self.scale, self.height * self.scale))
        pygame.display.set_caption('CHIP-8 Emulator')
        self.pixels = [[0] * self.width for _ in range(self.height)]
        self.clear()

    def clear(self):
        self.pixels = [[0] * self.width for _ in range(self.height)]
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

    def draw(self, x, y, pixel):   
        if pixel: 
            color = (255, 255, 255) 
        else:
            color = (0, 0, 0)
        pygame.draw.rect(self.screen, color, (x * self.scale, y * self.scale, self.scale, self.scale))
        pygame.display.flip()
