import pygame
import random, time

class Avatar:
    def __init__(self, x, y, size, nombre, ataque, vida, velocidad_casilla, velocidad_ataque, 
                 image_paths_walk, image_paths_attack, image_paths_death,
                 escala=1.0, level=None):

        self.x = x
        self.y = y
        self.size = size
        self.nombre = nombre
        self.level = level
        self.ataque = ataque
        self.vida_max = vida
        self.vida = vida
        self.velocidad_casilla = velocidad_casilla
        self.velocidad_ataque = velocidad_ataque
        self.detener = False
        self.escala = escala
        self.oponente = None
        self.total_casillas = 1

        # Estados: walking, attacking, dying
        self.state = "walking"
        self.death_start_time = None
        self.death_duration = 1500 

        # Tiempo de control
        self.tiempo_ultimo_movimiento = pygame.time.get_ticks()
        self.tiempo_ultimo_ataque = pygame.time.get_ticks()

        # Cargar sprites caminando
        self.sprites_walk = []
        for path in image_paths_walk:
            img = pygame.image.load(path).convert_alpha()
            w, h = img.get_size()
            img = pygame.transform.scale(img, (int(w * escala), int(h * escala)))
            self.sprites_walk.append(img)

        # Cargar sprites ataque
        self.sprites_attack = []
        for path in image_paths_attack:
            img = pygame.image.load(path).convert_alpha()
            w, h = img.get_size()
            img = pygame.transform.scale(img, (int(w * escala), int(h * escala)))
            self.sprites_attack.append(img)

        # Cargar sprites muerte (3 imágenes)
        self.sprites_death = []
        for path in image_paths_death:
            img = pygame.image.load(path).convert_alpha()
            w, h = img.get_size()
            img = pygame.transform.scale(img, (int(w * escala), int(h * escala)))
            self.sprites_death.append(img)

        # Control de animación
        self.sprite_actual = 0
        self.tiempo_ultimo_cambio_sprite = pygame.time.get_ticks()
        self.velocidad_animacion = 200

        # Imagen inicial
        self.image = self.sprites_walk[0]
        self.rect = self.image.get_rect(center=(x, y))

    def iniciar_muerte(self):
        self.state = "dying"
        self.detener = True
        self.sprite_actual = 0
        self.death_start_time = pygame.time.get_ticks()

    def animacion_muerte_completa(self):
        """Indica si ya pasaron los 2 segundos de animación."""
        if self.death_start_time is None:
            return False
        return pygame.time.get_ticks() - self.death_start_time >= self.death_duration

    def actualizar_animacion(self):
        tiempo = pygame.time.get_ticks()

        if tiempo - self.tiempo_ultimo_cambio_sprite < self.velocidad_animacion:
            return

        self.tiempo_ultimo_cambio_sprite = tiempo

        if self.state == "dying":
            elapsed = tiempo - self.death_start_time
            total_frames = len(self.sprites_death)

            frame = int((elapsed / self.death_duration) * total_frames)
            frame = min(frame, total_frames - 1)

            self.sprite_actual = frame
            self.image = self.sprites_death[self.sprite_actual]

            return


        # Animación de combate
        if self.state == "attacking":
            self.sprite_actual = (self.sprite_actual + 1) % len(self.sprites_attack)
            self.image = self.sprites_attack[self.sprite_actual]
            return

        # Animación caminando
        if self.state == "walking":
            self.sprite_actual = (self.sprite_actual + 1) % len(self.sprites_walk)
            self.image = self.sprites_walk[self.sprite_actual]

    def atacar(self, objetivo):
        tiempo = pygame.time.get_ticks()
        delta = (tiempo - self.tiempo_ultimo_ataque) / 1000.0

        if delta >= self.velocidad_ataque:
            objetivo.vida -= self.ataque
            self.tiempo_ultimo_ataque = tiempo
            return True
        return False

    def update(self, tamaño_celda):

        # Estado muerte
        if self.state == "dying":
            self.actualizar_animacion()
            return self.animacion_muerte_completa()  # True = eliminar

        # Si vida llegó a 0, iniciar animación de muerte
        if self.vida <= 0:
            self.iniciar_muerte()
            return False

        tiempo = pygame.time.get_ticks()

        # Combate
        if self.oponente and self.oponente.vida > 0:
            self.state = "attacking"
            self.atacar(self.oponente)
            self.actualizar_animacion()
            return False

        # Terminar combate
        if self.oponente and self.oponente.vida <= 0:
            self.oponente = None
            self.state = "walking"

        # Movimiento
        if self.state == "walking":
            self.actualizar_animacion()
            delta_t = (tiempo - self.tiempo_ultimo_movimiento) / 1000.0

            if delta_t >= self.velocidad_casilla:
                self.rect.y -= tamaño_celda
                self.tiempo_ultimo_movimiento = tiempo
                self.total_casillas += 1
                print(self.total_casillas)

                if self.total_casillas >= 10:
                    time.sleep(1)
                    self.level.finalizar_partida()
                    return False

        return False

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.barra_vida(surface)

    def barra_vida(self, surface):
        if self.state == "dying":
            return  # sin barra mientras muere

        bar_width = self.rect.width
        bar_height = 6
        bar_x = self.rect.x
        bar_y = self.rect.y - 10
        vida_ratio = max(0, min(self.vida / self.vida_max, 1))
        pygame.draw.rect(surface, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(surface, (0, 200, 0), (bar_x, bar_y, int(bar_width * vida_ratio), bar_height))
        pygame.draw.rect(surface, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 1)


class AvatarsManager:
    def __init__(self, tablero, spawn_interval=10, max_avatars=10, on_avatar_killed=None, level=None):
        self.tablero = tablero
        self.level = level
        self.avatars = []
        self.spawn_interval = spawn_interval * 1000
        self.last_spawn_time = pygame.time.get_ticks()
        self.max_avatars = max_avatars
        self.avatars_spawneados = 0
        self.on_avatar_killed = on_avatar_killed

        self.avatar_tipos = [Flechador, Escudero, Leñador, Canibal]

    def update(self):
        current_time = pygame.time.get_ticks()

        # Spawning
        if current_time - self.last_spawn_time >= self.spawn_interval and self.avatars_spawneados < self.max_avatars:
            self.spawn_avatar()
            self.last_spawn_time = current_time
            self.avatars_spawneados += 1

        avatares_muertos = 0
        nuevos = []

        for avatar in self.avatars:

            # Si el avatar NO tiene oponente activo, buscar rook
            if avatar.state != "dying":
                if not avatar.oponente or avatar.oponente.vida <= 0:
                    avatar.oponente = None
                    avatar.detener = False
                    avatar.state = "walking"

                    # Buscar rook en la misma columna
                    col = self.obtener_columna_por_x(avatar.rect.centerx)
                    if col is not None:
                        rook = self.buscar_rook_adyacente(col, avatar.rect.centery)
                        if rook:
                            self.iniciar_combate(avatar, rook)

            # Actualización del avatar
            eliminar = avatar.update(self.tablero.TAMAÑO_CELDA)

            # Si terminó la animación de muerte → eliminar
            if eliminar:
                avatares_muertos += 1
                continue

            nuevos.append(avatar)

        self.avatars = nuevos
        return avatares_muertos * 75


    def spawn_avatar(self):
        columna = random.randint(0, self.tablero.COLUMNAS - 1)
        celda = self.tablero.celdas[-1][columna]

        x = celda.rect.centerx
        y = celda.rect.bottom - 30

        avatar_class = self.seleccionar_avatar_ponderado()
        nuevo = avatar_class(x, y, self.tablero.TAMAÑO_CELDA, level=self.level)
        self.avatars.append(nuevo)

    def seleccionar_avatar_ponderado(self):
        avatars = []
        pesos = []

        for avatar_class in self.avatar_tipos:
            temp = avatar_class(0, 0, 0)
            avatars.append(avatar_class)
            pesos.append(temp.peso_aparicion)

        return random.choices(avatars, weights=pesos, k=1)[0]

    def draw(self, surface):
        for avatar in self.avatars:
            avatar.draw(surface)

    def iniciar_combate(self, avatar, rook):
        avatar.detener = True
        avatar.oponente = rook
        avatar.state = "attacking"
        rook.oponente = avatar

    def obtener_columna_por_x(self, x_position):
        for col_idx in range(self.tablero.COLUMNAS):
            celda = self.tablero.celdas[0][col_idx]
            if celda.rect.left <= x_position <= celda.rect.right:
                return col_idx
        return None

    def buscar_rook_adyacente(self, columna, avatar_y):
        distancia_celda = self.tablero.TAMAÑO_CELDA
        margen = distancia_celda * 1.5
        
        rook_mas_cercano = None
        distancia_minima = float('inf')
        
        for fila in self.tablero.celdas:
            celda = fila[columna]
            if celda.rook and not celda.rook.oponente:
                distancia = avatar_y - celda.rook.rect.centery
                if 0 < distancia <= margen and distancia < distancia_minima:
                    distancia_minima = distancia
                    rook_mas_cercano = celda.rook
        
        return rook_mas_cercano


# ==== CLASES ESPECÍFICAS DE AVATARES ====

class Flechador(Avatar):
    def __init__(self, x, y, size, level=None):
        walk = [
            "assets/images/ui/avatar_flechador_move_1.png",
            "assets/images/ui/avatar_flechador_move_2.png",
            "assets/images/ui/avatar_flechador_move_3.png"
        ]
        attack = [
            "assets/images/ui/avatar_flechador_attack_1.png",
            "assets/images/ui/avatar_flechador_attack_2.png",
            "assets/images/ui/avatar_flechador_attack_3.png"
        ]
        death = [
            "assets/images/ui/avatar_flechador_death_1.png",
            "assets/images/ui/avatar_flechador_death_2.png",
            "assets/images/ui/avatar_flechador_death_3.png"
        ]
        super().__init__(x, y, size, "Flechador", 2, 5, 12, 10, walk, attack, death, 0.1, level)
        self.peso_aparicion = 40


class Escudero(Avatar):
    def __init__(self, x, y, size, level=None):
        walk = [
            "assets/images/ui/avatar_escudero_move_1.png",
            "assets/images/ui/avatar_escudero_move_2.png",
            "assets/images/ui/avatar_escudero_move_3.png"
        ]
        attack = [
            "assets/images/ui/avatar_escudero_attack_1.png",
            "assets/images/ui/avatar_escudero_attack_2.png",
            "assets/images/ui/avatar_escudero_attack_3.png"
        ]
        death = [
            "assets/images/ui/avatar_escudero_death_1.png",
            "assets/images/ui/avatar_escudero_death_2.png",
            "assets/images/ui/avatar_escudero_death_3.png"
        ]
        super().__init__(x, y, size, "Escudero", 3, 10, 10, 15, walk, attack, death, 0.09, level)
        self.peso_aparicion = 30


class Leñador(Avatar):
    def __init__(self, x, y, size, level=None):
        walk = [
            "assets/images/ui/avatar_leñador_move_1.png",
            "assets/images/ui/avatar_leñador_move_2.png",
            "assets/images/ui/avatar_leñador_move_3.png"
        ]
        attack = [
            "assets/images/ui/avatar_leñador_attack_1.png",
            "assets/images/ui/avatar_leñador_attack_2.png",
            "assets/images/ui/avatar_leñador_attack_3.png"
        ]
        death = [
            "assets/images/ui/avatar_leñador_death_1.png",
            "assets/images/ui/avatar_leñador_death_2.png",
            "assets/images/ui/avatar_leñador_death_3.png"
        ]
        super().__init__(x, y, size, "Leñador", 9, 20, 13, 5, walk, attack, death, 0.08, level)
        self.peso_aparicion = 20


class Canibal(Avatar):
    def __init__(self, x, y, size, level=None):
        walk = [
            "assets/images/ui/avatar_canibal_move_1.png",
            "assets/images/ui/avatar_canibal_move_2.png",
            "assets/images/ui/avatar_canibal_move_3.png"
        ]
        attack = [
            "assets/images/ui/avatar_canibal_attack_1.png",
            "assets/images/ui/avatar_canibal_attack_2.png",
            "assets/images/ui/avatar_canibal_attack_3.png"
        ]
        death = [
            "assets/images/ui/avatar_canibal_death_1.png",
            "assets/images/ui/avatar_canibal_death_2.png",
            "assets/images/ui/avatar_canibal_death_3.png"
        ]
        super().__init__(x, y, size, "Canibal", 12, 25, 14, 3, walk, attack, death, 0.08, level)
        self.peso_aparicion = 10
