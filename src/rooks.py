import pygame

class Rook:
    def __init__(self, x, y, size, nombre, ataque, vida, costo, image_path, attack_sprite_paths=None):
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
        self.oponente = None 

        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

        # Sprites de ataque (rayos)
        self.attack_sprites = []
        self.mostrar_ataque = False
        self.tiempo_mostrar_ataque = 0
        self.duracion_sprite_ataque = 500  # Duración total de la animación
        self.sprite_ataque_actual = 0
        self.tiempo_ultimo_cambio_sprite = 0
        self.velocidad_animacion_ataque = 200  # Milisegundos entre cada sprite
        
        if attack_sprite_paths:
            for path in attack_sprite_paths:
                sprite = pygame.image.load(path).convert_alpha()
                sprite = pygame.transform.scale(sprite, (size // 2, size))
                self.attack_sprites.append(sprite)

    def atacar(self, objetivo):
        """Realiza un ataque al objetivo"""
        tiempo_actual = pygame.time.get_ticks()
        delta_t = (tiempo_actual - self.tiempo_ultimo_ataque) / 1000.0
        
        if delta_t >= self.velocidad_ataque:
            objetivo.vida -= self.ataque
            self.tiempo_ultimo_ataque = tiempo_actual
            
            # Activar animación de ataque
            self.mostrar_ataque = True
            self.tiempo_mostrar_ataque = tiempo_actual
            self.sprite_ataque_actual = 0
            self.tiempo_ultimo_cambio_sprite = tiempo_actual
            return True
        return False

    def actualizar_animacion_ataque(self):
        """Alterna entre los sprites de ataque"""
        tiempo_actual = pygame.time.get_ticks()
        
        # Cambiar al siguiente sprite
        if tiempo_actual - self.tiempo_ultimo_cambio_sprite >= self.velocidad_animacion_ataque:
            self.sprite_ataque_actual = (self.sprite_ataque_actual + 1) % len(self.attack_sprites)
            self.tiempo_ultimo_cambio_sprite = tiempo_actual
        
        # Desactivar después de la duración total
        if tiempo_actual - self.tiempo_mostrar_ataque >= self.duracion_sprite_ataque:
            self.mostrar_ataque = False

    def update(self):
        # Actualizar animación de ataque
        if self.mostrar_ataque and self.attack_sprites:
            self.actualizar_animacion_ataque()
        
        if self.oponente and self.oponente.vida > 0:
            self.atacar(self.oponente)
        elif self.oponente and self.oponente.vida <= 0:
            # El oponente murió, liberar
            self.oponente = None
            self.mostrar_ataque = False

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
    
    def draw_attack(self, surface):
        """Dibuja el sprite de ataque (llamar después de dibujar todo lo demás)"""
        if self.mostrar_ataque and self.attack_sprites:
            sprite_actual = self.attack_sprites[self.sprite_ataque_actual]
            attack_x = self.rect.centerx - sprite_actual.get_width() // 2
            attack_y = self.rect.bottom - 10
            surface.blit(sprite_actual, (attack_x, attack_y))


class SandRook(Rook):
    nombre = "Sand Rook"
    ataque = 2
    vida = 3
    costo = 50
    image_path = "assets/images/ui/sand_rook.png"
    attack_sprite_paths = [
        "assets/images/ui/sandrook_attack_1.png",
        "assets/images/ui/sandrook_attack_2.png",
        "assets/images/ui/sandrook_attack_3.png"
    ]

    def __init__(self, x, y, size):
        super().__init__(x, y, size, self.nombre, self.ataque, self.vida, self.costo, self.image_path, self.attack_sprite_paths)


class RockRook(Rook):
    nombre = "Rock Rook"
    ataque = 4
    vida = 14
    costo = 100
    image_path = "assets/images/ui/rock_rook.png"
    attack_sprite_paths = [
        "assets/images/ui/rockrook_attack_1.png",
        "assets/images/ui/rockrook_attack_2.png",
        "assets/images/ui/rockrook_attack_3.png"
    ]

    def __init__(self, x, y, size):
        super().__init__(x, y, size, self.nombre, self.ataque, self.vida, self.costo, self.image_path, self.attack_sprite_paths)


class FireRook(Rook):
    nombre = "Fire Rook"
    ataque = 8
    vida = 16
    costo = 150
    image_path = "assets/images/ui/fire_rook.png"
    attack_sprite_paths = [
        "assets/images/ui/firerook_attack_1.png",
        "assets/images/ui/firerook_attack_2.png",
        "assets/images/ui/firerook_attack_3.png"
    ]

    def __init__(self, x, y, size):
        super().__init__(x, y, size, self.nombre, self.ataque, self.vida, self.costo, self.image_path, self.attack_sprite_paths)


class WaterRook(Rook):
    nombre = "Water Rook"
    ataque = 8
    vida = 10
    costo = 150
    image_path = "assets/images/ui/water_rook.png"
    attack_sprite_paths = [
        "assets/images/ui/waterrook_attack_1.png",
        "assets/images/ui/waterrook_attack_2.png",
        "assets/images/ui/waterrook_attack_3.png"
    ]

    def __init__(self, x, y, size):
        super().__init__(x, y, size, self.nombre, self.ataque, self.vida, self.costo, self.image_path, self.attack_sprite_paths)