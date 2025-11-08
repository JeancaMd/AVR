import pygame 
import random

class Moneda:
    def __init__(self, x, y, size, valor=50):
        self.x = x
        self.y = y
        self.size = size
        self.valor = valor
        self.rect = pygame.Rect(x - size//2, y - size//2, size, size)
        
        self.color = (255, 215, 0)
        self.border_color = (218, 165, 32)
        
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.size // 2)
        pygame.draw.circle(surface, self.border_color, (self.x, self.y), self.size // 2, 2)
        

class MonedasManager:
    def __init__(self, tablero, spawn_interval=5):
        self.tablero = tablero
        self.monedas = []
        self.spawn_interval = spawn_interval * 1000 
        self.last_spawn_time = pygame.time.get_ticks()
        self.moneda_size = 30
        
    def update(self):
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_spawn_time >= self.spawn_interval:
            self.spawn_moneda()
            self.last_spawn_time = current_time
    
    def spawn_moneda(self):
        celdas_vacias = []
        for fila in self.tablero.celdas:
            for celda in fila:
                if not celda.rook:
                    celdas_vacias.append(celda)
        
        if celdas_vacias:
            celda = random.choice(celdas_vacias)
            x = celda.rect.centerx
            y = celda.rect.centery
            nueva_moneda = Moneda(x, y, self.moneda_size, valor=50)
            self.monedas.append(nueva_moneda)
    
    def handle_click(self, pos):
        for moneda in self.monedas:
            if moneda.rect.collidepoint(pos):
                valor = moneda.valor
                self.monedas.remove(moneda)
                return valor
        return 0
    
    def draw(self, surface):
        for moneda in self.monedas:
            moneda.draw(surface)