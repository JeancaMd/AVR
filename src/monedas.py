import pygame
import random

class Moneda:
    def __init__(self, x, y, size, valor, color, border_color):
        self.x = x
        self.y = y
        self.size = size
        self.valor = valor
        self.rect = pygame.Rect(x - size//2, y - size//2, size, size)
        self.color = color
        self.border_color = border_color
        
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
        
        self.tipos = {
            25: ((0, 200, 0), (0, 120, 0)),        # Verde
            50: ((255, 215, 0), (218, 165, 32)),  # Dorado
            100: ((200, 0, 0), (120, 0, 0))        # Rojo
        }
        
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
        
        if not celdas_vacias:
            return
        
        ### Elegir una celda aleatoria
        celda = random.choice(celdas_vacias)

        ### Elegir un tipo de moneda aleatorio 
        valor = random.choice(list(self.tipos.keys()))
        color, borde = self.tipos[valor]

        x = celda.rect.centerx
        y = celda.rect.centery

        moneda_nueva = Moneda(x, y, self.moneda_size, valor, color, borde)
        self.monedas.append(moneda_nueva)

    def handle_click(self, pos):
        for moneda in list(self.monedas):
            if moneda.rect.collidepoint(pos):
                valor = moneda.valor
                self.monedas.remove(moneda)
                return valor
        return 0
    
    def draw(self, surface):
        for moneda in self.monedas:
            moneda.draw(surface)
