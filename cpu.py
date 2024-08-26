import random

class CPU:
    def __init__(self, memory, display):
        self.memory = memory
        self.display = display
        self.v = [0] * 16   
        self.i = 0         
        self.pc = 0x200     
        self.stack = []
        self.delay_timer = 0
        self.sound_timer = 0
        self.key = [0] * 16  

    def load_program(self, path):
        with open(path, 'rb') as f:
            rom = f.read()
        for i, byte in enumerate(rom):
            self.memory.memory[0x200 + i] = byte

    def fetch_opcode(self):
        return self.memory.memory[self.pc] << 8 | self.memory.memory[self.pc + 1]

    def decode_execute(self, opcode):
        self.pc += 2 
        nnn = opcode & 0x0FFF
        n = opcode & 0x000F
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        kk = opcode & 0x00FF

        if opcode == 0x00E0:  # CLS
            self.display.clear()
        elif opcode == 0x00EE:  # RET ***
            self.pc = self.stack.pop()
        elif opcode & 0xF000 == 0x1000:  # JP addr
            self.pc = nnn
        elif opcode & 0xF000 == 0x2000:  # CALL addr
            self.stack.append(self.pc)
            self.pc = nnn
        elif opcode & 0xF000 == 0x3000:  # SE Vx, byte
            if self.v[x] == kk:
                self.pc += 2
        elif opcode & 0xF000 == 0x4000:  # SNE Vx, byte
            if self.v[x] != kk:
                self.pc += 2
        elif opcode & 0xF000 == 0x5000:  # SE Vx, Vy
            if self.v[x] == self.v[y]:
                self.pc += 2
        elif opcode & 0xF000 == 0x6000:  # LD Vx, byte
            self.v[x] = kk
        elif opcode & 0xF000 == 0x7000:  # ADD Vx, byte
            self.v[x] = (self.v[x] + kk) & 0xFF
        elif opcode & 0xF00F == 0x8000:  # LD Vx, Vy
            self.v[x] = self.v[y]
        elif opcode & 0xF00F == 0x8001:  # OR Vx, Vy
            self.v[x] |= self.v[y]
        elif opcode & 0xF00F == 0x8002:  # AND Vx, Vy
            self.v[x] &= self.v[y]
        elif opcode & 0xF00F == 0x8003:  # XOR Vx, Vy
            self.v[x] ^= self.v[y]
        elif opcode & 0xF00F == 0x8004:  # ADD Vx, Vy
            self.v[x] += self.v[y] 
            if self.v[x] > 0xFF:
                self.v[0xF] = 1
            else:
                self.v[0xF] = 0
            self.v[x] &= 0xFF
        elif opcode & 0xF00F == 0x8005:  # SUB Vx, Vy
            if self.v[x] > self.v[y]:
                self.v[0xF] = 1
            else:
                self.v[0xF] = 0
            self.v[x] = (self.v[x] - self.v[y]) & 0xFF
        elif opcode & 0xF00F == 0x8006:  # SHR Vx {, Vy}
            self.v[0xF] = self.v[x] & 0x1
            self.v[x] >>= 1
        elif opcode & 0xF00F == 0x8007:  # SUBN Vx, Vy
            if self.v[y] > self.v[x]:
                self.v[0xF] = 1 
            else:
                self.v[0xF] = 0
            self.v[x] = (self.v[y] - self.v[x]) & 0xFF
        elif opcode & 0xF00F == 0x800E:  # SHL Vx {, Vy}
            self.v[0xF] = (self.v[x] & 0x80) >> 7
            self.v[x] = (self.v[x] << 1) & 0xFF
        elif opcode & 0xF00F == 0x9000:  # SNE Vx, Vy
            if self.v[x] != self.v[y]:
                self.pc += 2
        elif opcode & 0xF000 == 0xA000:  # LD I, addr
            self.i = nnn
        elif opcode & 0xF000 == 0xB000:  # JP V0, addr
            self.pc = nnn + self.v[0]
        elif opcode & 0xF000 == 0xC000:  # RND Vx, byte
            self.v[x] = random.randint(0, 255) & kk
        elif opcode & 0xF000 == 0xD000:  # DRW Vx, Vy, nibble
            self.draw_sprite(x, y, n)
        elif opcode & 0xF0FF == 0xE09E:  # SKP Vx
            if self.key[self.v[x]] == 1:
                self.pc += 2
        elif opcode & 0xF0FF == 0xE0A1:  # SKNP Vx
            if self.key[self.v[x]] == 0:
                self.pc += 2
        elif opcode & 0xF0FF == 0xF007:  # LD Vx, DT
            self.v[x] = self.delay_timer
        elif opcode & 0xF0FF == 0xF00A:  # LD Vx, K
            key_press = False
            for i in range(len(self.key)):
                if self.key[i] != 0:
                    self.v[x] = i
                    key_press = True
                    break
            if not key_press:
                self.pc -= 2
        elif opcode & 0xF0FF == 0xF015:  # LD DT, Vx
            self.delay_timer = self.v[x]
        elif opcode & 0xF0FF == 0xF018:  # LD ST, Vx
            self.sound_timer = self.v[x]
        elif opcode & 0xF0FF == 0xF01E:  # ADD I, Vx
            self.i = (self.i + self.v[x]) & 0xFFF
        elif opcode & 0xF0FF == 0xF029:  # LD F, Vx
            self.i = self.v[x] * 5
        elif opcode & 0xF0FF == 0xF033:  # LD B, Vx
            self.memory.memory[self.i] = self.v[x] // 100
            self.memory.memory[self.i + 1] = (self.v[x] // 10) % 10
            self.memory.memory[self.i + 2] = self.v[x] % 10
        elif opcode & 0xF0FF == 0xF055:  # LD [I], Vx
            for i in range(x + 1):
                self.memory.memory[self.i + i] = self.v[i]
        elif opcode & 0xF0FF == 0xF065:  # LD Vx, [I]
            for i in range(x + 1):
                self.v[i] = self.memory.memory[self.i + i]

    def draw_sprite(self, vx, vy, height):
        x = self.v[vx] % self.display.width
        y = self.v[vy] % self.display.height
        self.v[0xF] = 0  # Collision flag

        for row in range(height):
            sprite = self.memory.memory[self.i + row]
            for col in range(8):
                if (sprite & (0x80 >> col)) != 0:
                    pixel_x = (x + col) % self.display.width
                    pixel_y = (y + row) % self.display.height
                    if self.display.pixels[pixel_y][pixel_x] == 1:
                        self.v[0xF] = 1
                    self.display.pixels[pixel_y][pixel_x] ^= 1
                    self.display.draw(pixel_x, pixel_y, self.display.pixels[pixel_y][pixel_x])
    
    def cycle(self):
        opcode = self.fetch_opcode()
        self.decode_execute(opcode)

    def update_timers(self):
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1
