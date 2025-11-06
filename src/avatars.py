import pygame
import random

import pygame
import random

class Avatar:
    def __init__(self, x, y, size, nombre, ataque, vida, velocidad_casilla, velocidad_ataque, image_path, escala=1.0):
        self.x = x
        self.y = y
        self.size = size
        self.nombre = nombre
        self.ataque = ataque
        self.vida_max = vida
        self.vida = vida
        self.velocidad_casilla = velocidad_casilla
        self.velocidad_ataque = velocidad_ataque
        self.detener = False
        self.escala = escala
        self.tiempo_ultimo_movimiento = pygame.time.get_ticks()
        self.tiempo_ultimo_ataque = pygame.time.get_ticks()
        self.rook_objetivo = None

        self.image = pygame.image.load(image_path).convert_alpha()
        w, h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w * self.escala), int(h * self.escala)))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, tamaño_celda):
        tiempo_actual = pygame.time.get_ticks()

        if self.rook_objetivo:
            delta_t_ataque = (tiempo_actual - self.tiempo_ultimo_ataque) / 1000.0
            if delta_t_ataque >= self.velocidad_ataque:
                self.rook_objetivo.vida -= self.ataque
                
                self.vida -= self.rook_objetivo.ataque
                
                self.tiempo_ultimo_ataque = tiempo_actual
                
                if self.rook_objetivo.vida <= 0:
                    self.rook_objetivo = None
                    self.detener = False
                
                if self.vida <= 0:
                    return True 
        
        if not self.detener:
            delta_t = (tiempo_actual - self.tiempo_ultimo_movimiento) / 1000.0
            if delta_t >= self.velocidad_casilla:
                self.rect.y -= tamaño_celda
                self.tiempo_ultimo_movimiento = tiempo_actual
        
        return False 

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.barra_vida(surface)

    def barra_vida(self, surface):
        bar_width = self.rect.width
        bar_height = 6
        bar_x = self.rect.x
        bar_y = self.rect.y - 10
        vida_ratio = max(0, min(self.vida / self.vida_max, 1))
        pygame.draw.rect(surface, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(surface, (0, 200, 0), (bar_x, bar_y, int(bar_width * vida_ratio), bar_height))
        pygame.draw.rect(surface, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 1)


class AvatarsManager:
    def __init__(self, tablero, spawn_interval=10, max_avatars=10, on_avatar_killed=None):
        self.tablero = tablero
        self.avatars = []
        self.spawn_interval = spawn_interval * 1000 
        self.last_spawn_time = pygame.time.get_ticks()
        self.max_avatars = max_avatars
        self.avatars_spawneados = 0 
        self.on_avatar_killed = on_avatar_killed 

        self.avatar_tipos =  [Flechador, Escudero, Leñador, Canibal]

    def update(self):
        current_time = pygame.time.get_ticks()

        if (current_time - self.last_spawn_time >= self.spawn_interval and 
            self.avatars_spawneados < self.max_avatars):
            self.spawn_avatar()
            self.last_spawn_time = current_time
            self.avatars_spawneados += 1

        for avatar in self.avatars:
            if not avatar.rook_objetivo:
                for fila_idx, fila in enumerate(self.tablero.celdas):
                    for col_idx, celda in enumerate(fila):
                        if avatar.rect.colliderect(celda.rect):
                            if fila_idx > 0:
                                celda_arriba = self.tablero.celdas[fila_idx - 1][col_idx]
                                if celda_arriba.rook:
                                    avatar.detener = True
                                    avatar.rook_objetivo = celda_arriba.rook
                                    celda_arriba.rook.avatar_objetivo = avatar
                                    avatar.rect.centery = celda.rect.centery
                                    break

            avatar.update(self.tablero.TAMAÑO_CELDA)

        avatares_muertos = 0
        avatares_vivos = []
        for avatar in self.avatars:
            if avatar.vida > 0:
                avatares_vivos.append(avatar)
            else:
                avatares_muertos += 1
        
        self.avatars = avatares_vivos
        return avatares_muertos * 75 


    def draw(self, surface):
        for avatar in self.avatars:
            avatar.draw(surface)

    def spawn_avatar(self):
        columna = random.randint(0, self.tablero.COLUMNAS - 1)
        celda = self.tablero.celdas[-1][columna]

        x = celda.rect.centerx
        y = celda.rect.bottom - 30

        avatar_class = self.seleccionar_avatar_ponderado()
        nuevo_avatar = avatar_class(x, y, self.tablero.TAMAÑO_CELDA)
        self.avatars.append(nuevo_avatar)

    def seleccionar_avatar_ponderado(self):
        avatars_con_pesos = []
        pesos = []
        
        for avatar_class in self.avatar_tipos:
            temp_avatar = avatar_class(0, 0, 0)
            avatars_con_pesos.append(avatar_class)
            pesos.append(temp_avatar.peso_aparicion)
        
        return random.choices(avatars_con_pesos, weights=pesos, k=1)[0]


class Flechador(Avatar):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, "Flechador", 2, 5, 12, 10, "assets/images/ui/avatar_flechador.png", 0.1)
        self.peso_aparicion = 40

class Escudero(Avatar):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, "Escudero", 3, 10, 10, 15, "assets/images/ui/avatar_escudero.png", 0.09)
        self.peso_aparicion = 30 

class Leñador(Avatar):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, "Leñador", 9, 20, 13, 5, "assets/images/ui/avatar_leñador.png", 0.08)
        self.peso_aparicion = 20

class Canibal(Avatar):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, "Canibal", 12, 25, 14, 3, "assets/images/ui/avatar_canibal.png", 0.08)
        self.peso_aparicion = 10
