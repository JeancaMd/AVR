import pygame

class Rook:
    def __init__(self, x, y, size, nombre, ataque, vida, costo, image_path):
        self.x = x
        self.y = y
        self.size = size
        self.nombre = nombre
        self.ataque = ataque
        self.vida = vida
        self.vida_max = vida
        self.costo = costo
        self.velocidad_ataque = 4.0 
        self.tiempo_ultimo_ataque = pygame.time.get_ticks()
        self.avatar_objetivo = None

        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        if self.avatar_objetivo:
            tiempo_actual = pygame.time.get_ticks()
            delta_t_ataque = (tiempo_actual - self.tiempo_ultimo_ataque) / 1000.0
            
            if delta_t_ataque >= self.velocidad_ataque:
                self.avatar_objetivo.vida -= self.ataque
                self.tiempo_ultimo_ataque = tiempo_actual
                
                if self.avatar_objetivo.vida <= 0:
                    self.avatar_objetivo = None

    def avatar_update(self, tamaño_celda):
        tiempo_actual = pygame.time.get_ticks()

        if self.rook_objetivo:
            delta_t_ataque = (tiempo_actual - self.tiempo_ultimo_ataque) / 1000.0
            if delta_t_ataque >= self.velocidad_ataque:
                self.rook_objetivo.vida -= self.ataque
                self.tiempo_ultimo_ataque = tiempo_actual
                
                if self.rook_objetivo.vida <= 0:
                    self.rook_objetivo.avatar_objetivo = None 
                    self.rook_objetivo = None
                    self.detener = False
            
            if self.vida <= 0:
                if self.rook_objetivo:
                    self.rook_objetivo.avatar_objetivo = None
                return True 
        
        if not self.detener:
            delta_t = (tiempo_actual - self.tiempo_ultimo_movimiento) / 1000.0
            if delta_t >= self.velocidad_casilla:
                self.rect.y -= tamaño_celda
                self.tiempo_ultimo_movimiento = tiempo_actual
        
        return False 

    def draw(self, surface):
        surface.blit(self.image, self.rect)

        bar_width = self.rect.width
        bar_height = 6
        vida_ratio = max(self.vida / self.vida_max, 0)
        vida_actual = int(bar_width * vida_ratio)
        bar_x = self.rect.left
        bar_y = self.rect.top - 10

        pygame.draw.rect(surface, (150, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, vida_actual, bar_height))
        pygame.draw.rect(surface, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 1)


class SandRook(Rook):
    nombre = "Sand Rook"
    ataque = 2
    vida = 3
    costo = 50
    image_path = "assets/images/ui/sand_rook.png"

    def __init__(self, x, y, size):
        super().__init__(x, y, size, self.nombre, self.ataque, self.vida, self.costo, self.image_path)


class RockRook(Rook):
    nombre = "Rock Rook"
    ataque = 4
    vida = 14
    costo = 100
    image_path = "assets/images/ui/rock_rook.png"

    def __init__(self, x, y, size):
        super().__init__(x, y, size, self.nombre, self.ataque, self.vida, self.costo, self.image_path)


class FireRook(Rook):
    nombre = "Fire Rook"
    ataque = 8
    vida = 16
    costo = 150
    image_path = "assets/images/ui/fire_rook.png"

    def __init__(self, x, y, size):
        super().__init__(x, y, size, self.nombre, self.ataque, self.vida, self.costo, self.image_path)


class WaterRook(Rook):
    nombre = "Water Rook"
    ataque = 8
    vida = 10
    costo = 150
    image_path = "assets/images/ui/water_rook.png"

    def __init__(self, x, y, size):
        super().__init__(x, y, size, self.nombre, self.ataque, self.vida, self.costo, self.image_path)
