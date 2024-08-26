import pygame

class Input:
    KEY_MAP = {
        pygame.K_x: 0x0,
        pygame.K_1: 0x1,
        pygame.K_2: 0x2,
        pygame.K_3: 0x3,
        pygame.K_q: 0x4,
        pygame.K_w: 0x5,
        pygame.K_e: 0x6,
        pygame.K_a: 0x7,
        pygame.K_s: 0x8,
        pygame.K_d: 0x9,
        pygame.K_z: 0xA,
        pygame.K_c: 0xB,
        pygame.K_4: 0xC,
        pygame.K_r: 0xD,
        pygame.K_f: 0xE,
        pygame.K_v: 0xF
    }
    
    def get_key(self, event):
        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            return self.KEY_MAP.get(event.key)
        return None
