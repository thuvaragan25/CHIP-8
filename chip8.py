import pygame
from cpu import CPU
from display import Display
from memory import Memory
from input import Input

class Chip8:
    def __init__(self):
        self.memory = Memory()
        self.display = Display()
        self.cpu = CPU(self.memory, self.display)
        self.input_handler = Input()

    def load_rom(self, path):
        self.cpu.load_program(path)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                key = self.input_handler.get_key(event)
                if key is not None:
                    if event.type == pygame.KEYDOWN:
                        self.cpu.key[key] = 1 
                    else:
                        self.cpu.key[key] = 0

            self.cpu.cycle()
            self.cpu.update_timers()
            clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python chip8.py [ROM file]")
    else:
        rom_path = sys.argv[1]
        chip8 = Chip8()
        chip8.load_rom(rom_path)
        chip8.run()