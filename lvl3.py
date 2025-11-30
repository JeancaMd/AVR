import pygame
import time
from database import GrupoCajetaDB
from src.window import Window
from src.tablero import Tablero
from src.rooks import *
from src.avatars import AvatarsManager
from src.monedas import MonedasManager
from src.cliente import ControladorUDP


class Level3(Window):
    def __init__(self):
        super().__init__()
        self.tablero = Tablero(self.RESOLUTION)
        self.clock = pygame.time.Clock()
        self.monedas = 0
        self.avatars = AvatarsManager(self.tablero, spawn_interval=4, max_avatars=16, level=self)
        self.monedas_coleccionables = MonedasManager(self.tablero, spawn_interval=5)
        self.db = GrupoCajetaDB()
        self.db.conectar()
        self.inicio_tiempo = None
        self.titulo = self.font.render("Nivel 3", True, (206, 143, 31))

        ### Control para recibir datos desde cliente.py
        self.control = ControladorUDP()

        ### Rooks disponibles
        self.rooks_tipos = [
            ("Sand Rook", SandRook),
            ("Rock Rook", RockRook),
            ("Fire Rook", FireRook),
            ("Water Rook", WaterRook)
        ]

        self.botones = []
        self.rook_seleccionada = None
        self.crear_botones()

        ### Sistema de navegación
        self.modo_seleccion = "rooks"
        self.indice_rook = 0
        self.celda_seleccionada = [0, 0]

        ### Cooldown para evitar spam
        self.ultimo_udp_ts = 0
        self.udp_cooldown_ms = 120



# -------------------------------
# Controlr eventos control
# -------------------------------
    def handle_udp(self, comando):
        ahora = int(time.time() * 1000)
        if ahora - self.ultimo_udp_ts < self.udp_cooldown_ms:
            pass
        self.ultimo_udp_ts = ahora

        if comando == "CUADRADO":
            self.modo_seleccion = "rooks"
            print("Modo: Seleccionar Rooks")

        if comando == "TRIANGULO":
            self.modo_seleccion = "tablero"
            print("Modo: Seleccionar Tablero")

        if comando == "O":
            self.recoger_moneda_en_celda()

        if comando == "JOYSTICK_PRESIONADO":
            if self.modo_seleccion == "tablero":
                self.colocar_rook_en_celda()

        ### Movimientos verticales del joystick
        if comando == "Y+":
            if self.modo_seleccion == "rooks":
                self.indice_rook = (self.indice_rook - 1) % len(self.rooks_tipos)
                self.rook_seleccionada = self.rooks_tipos[self.indice_rook]
                print(f"Rook: {self.rook_seleccionada[0]}")
            else:
                self.celda_seleccionada[0] = max(0, self.celda_seleccionada[0] - 1)
            return

        if comando == "Y-":
            if self.modo_seleccion == "rooks":
                self.indice_rook = (self.indice_rook + 1) % len(self.rooks_tipos)
                self.rook_seleccionada = self.rooks_tipos[self.indice_rook]
                print(f"Rook: {self.rook_seleccionada[0]}")
            else:
                self.celda_seleccionada[0] = min(self.tablero.FILAS - 1, self.celda_seleccionada[0] + 1)
            return

        ### Movimientos horizontales joystick
        if comando == "X+":
            if self.modo_seleccion == "tablero":
                self.celda_seleccionada[1] = min(self.tablero.COLUMNAS - 1, self.celda_seleccionada[1] + 1)
            return

        if comando == "X-":
            if self.modo_seleccion == "tablero":
                self.celda_seleccionada[1] = max(0, self.celda_seleccionada[1] - 1)
            return

        ### botón X del control
        if comando == "X":
            if self.modo_seleccion == "tablero":
                self.colocar_rook_en_celda()
            else:
                print("Botón X presionado en modo rooks")
            return



# -------------------------------
# Controlar eventos del teclado y mouse
# -------------------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self.handle_keyboard(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                monedas_ganadas = self.monedas_coleccionables.handle_click(pos)
                if monedas_ganadas > 0:
                    self.monedas += monedas_ganadas
                    return

                for i, (rect, nombre, _) in enumerate(self.botones):
                    if rect.collidepoint(pos):
                        self.rook_seleccionada = self.rooks_tipos[i]
                        self.indice_rook = i
                        print(f"Seleccionada: {nombre}")
                        return

                if self.rook_seleccionada:
                    _, rook_class = self.rook_seleccionada
                    costo = rook_class.costo
                    if self.monedas >= costo:
                        colocado = self.tablero.handle_click(pos, rook_class)
                        if colocado:
                            self.monedas -= costo
                            print(f"Rook colocado. Monedas restantes: {self.monedas}")
                    else:
                        print("No hay suficientes monedas para colocar el rook")

    def handle_keyboard(self, key):
        if key == pygame.K_a:
            self.modo_seleccion = "rooks"
            print("Modo: Seleccionar Rooks")
            return

        if key == pygame.K_s:
            self.modo_seleccion = "tablero"
            print("Modo: Seleccionar Tablero")
            return

        if key == pygame.K_d:
            self.recoger_moneda_en_celda()
            return

        if self.modo_seleccion == "rooks":
            if key == pygame.K_UP:
                self.indice_rook = (self.indice_rook - 1) % len(self.rooks_tipos)
                self.rook_seleccionada = self.rooks_tipos[self.indice_rook]
                print(f"Rook: {self.rook_seleccionada[0]}")
            elif key == pygame.K_DOWN:
                self.indice_rook = (self.indice_rook + 1) % len(self.rooks_tipos)
                self.rook_seleccionada = self.rooks_tipos[self.indice_rook]
                print(f"Rook: {self.rook_seleccionada[0]}")
        else:
            fila, col = self.celda_seleccionada
            if key == pygame.K_UP:
                self.celda_seleccionada[0] = max(0, fila - 1)
            elif key == pygame.K_DOWN:
                self.celda_seleccionada[0] = min(self.tablero.FILAS - 1, fila + 1)
            elif key == pygame.K_LEFT:
                self.celda_seleccionada[1] = max(0, col - 1)
            elif key == pygame.K_RIGHT:
                self.celda_seleccionada[1] = min(self.tablero.COLUMNAS - 1, col + 1)
            elif key == pygame.K_RETURN:
                self.colocar_rook_en_celda()


# -------------------------------
# Crear botones para los rooks
# -------------------------------
    def crear_botones(self):
        button_size = 120
        spacing = 15
        x = 40
        start_y = self.RESOLUTION[1] - ((button_size + spacing) * len(self.rooks_tipos)) - 80
        self.botones.clear()
        for i, (nombre, rook_class) in enumerate(self.rooks_tipos):
            y = start_y + i * (button_size + spacing)
            rect = pygame.Rect(x, y, button_size, button_size)
            temp_rook = rook_class(0, 0, button_size)
            image = temp_rook.image
            self.botones.append((rect, nombre, image))

# -------------------------------
# Acciones del tablero
 # -------------------------------
    def colocar_rook_en_celda(self):
        if not self.rook_seleccionada:
            print("No hay rook seleccionado.")
            return
        fila, col = self.celda_seleccionada
        celda = self.tablero.celdas[fila][col]
        if celda.rook is not None:
            print("La celda ya tiene un rook")
            return
        _, rook_class = self.rook_seleccionada
        costo = rook_class.costo
        if self.monedas >= costo:
            size = celda.rect.width
            celda.rook = rook_class(celda.rect.x, celda.rect.y, size)
            self.monedas -= costo
            print(f"Rook colocado en [{fila}, {col}]. Monedas restantes: {self.monedas}")
        else:
            print("No hay suficientes monedas para colocar el rook")

    def recoger_moneda_en_celda(self):
        fila, col = self.celda_seleccionada
        celda = self.tablero.celdas[fila][col]
        for moneda in self.monedas_coleccionables.monedas[:]:
            if celda.rect.colliderect(moneda.rect):
                self.monedas += moneda.valor
                self.monedas_coleccionables.monedas.remove(moneda)
                print(f"Moneda recogida. Total: {self.monedas}")
                return
        print("No hay moneda en la celda seleccionada")


# -------------------------------
# Render
# -------------------------------
    def render(self):
        self.screen.blit(self.game_image, (0, 0))
        self.tablero.draw(self.screen)
        self.avatars.draw(self.screen)
        self.tablero.draw_attacks(self.screen)
        self.monedas_coleccionables.draw(self.screen)
        self.cant_monedas = self.font.render(f"Monedas: {self.monedas}", True, (255, 255, 0))
        self.screen.blit(self.cant_monedas, (40, 20))
        self.screen.blit(self.titulo, (self.RESOLUTION[0]//2.25, 30))

        tiempo_actual = time.time() - Window.tiempo_inicio_global
        timer_text = self.font.render(f"{tiempo_actual:0.1f}s", True, (255, 255, 255))
        timer_rect = timer_text.get_rect(topright=(self.RESOLUTION[0] - 30, 30))
        self.screen.blit(timer_text, timer_rect)

        modo_render = self.font.render(
            f"Modo: {self.modo_seleccion.upper()}",
            True, (255, 255, 255)
        )
        self.screen.blit(modo_render, (40, 50))
        for i, (rect, nombre, image) in enumerate(self.botones):
            pygame.draw.rect(self.screen, (230, 230, 230), rect)
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
            img_rect = image.get_rect(center=rect.center)
            self.screen.blit(image, img_rect)
            rook_class = next(r for n, r in self.rooks_tipos if n == nombre)
            costo = rook_class.costo
            costo_text = self.font.render(f"{costo}", True, (255, 255, 255))
            self.screen.blit(costo_text, (rect.right + 15, rect.centery - costo_text.get_height() // 2))
            if i == self.indice_rook:
                pygame.draw.rect(self.screen, (255, 215, 0), rect, 4)
        if self.modo_seleccion == "tablero":
            fila, col = self.celda_seleccionada
            celda = self.tablero.celdas[fila][col]
            pygame.draw.rect(self.screen, (255, 215, 0), celda.rect, 5)

        pygame.display.flip()

# -------------------------------
# Loop principal
# -------------------------------
    def move(self):
        self.avatars.move()

    def update(self):
        if Window.tiempo_inicio_global is None:
            Window.tiempo_inicio_global = time.time()

        self.tablero.update()
        monedas_ganadas = self.avatars.update()
        self.monedas += monedas_ganadas
        self.monedas_coleccionables.update()
        self.tablero.limpiar_rooks_muertos()
        
        # Verificar fin de nivel
        if (
            getattr(self.avatars, "avatars_spawneados", 0) >= getattr(self.avatars, "max_avatars", 10)
            and len(getattr(self.avatars, "avatars", [])) == 0
        ):
            print("Nivel completado.")
            self.finalizar_partida_win()

    def run(self):
        self.inicio_tiempo = time.time()
        
        while self.running:
            comando = self.control.obtener_evento()
            if comando:
                self.handle_udp(comando)
            
            self.handle_events()
            self.update()  # Tu lógica específica
            self.render()
            self.clock.tick(60)
        
        pygame.event.clear()
        if self.next_window:
            nueva_ventana = self.next_window()
            nueva_ventana.run()

# -------------------------------
# Finalizar
# -------------------------------
    def finalizar_partida_win(self):
        ### Tiempo total global desde que inició el juego
        duracion = time.time() - Window.tiempo_inicio_global

        minutos_extra = max(0, duracion - 55) / 5
        penalizacion = int(minutos_extra) * 100
        puntaje = max(0, 5000 - penalizacion)

        print(f"Duración: {duracion:.2f}s")
        print(f"Puntaje final: {puntaje}")

        ### Guardar puntaje
        try:
            self.db.guardar_puntaje(self.user, puntaje, duracion)
        except Exception as e:
            print("Error al guardar puntaje:", e)
        finally:
            self.db.cerrar()

        ### Cambiar ventana
        from fama import SalonFama
        self.cambiar_ventana(SalonFama)

    def finalizar_partida_derrota(self):
        from menu_derrota import DefeatWindow
        self.cambiar_ventana(DefeatWindow)


