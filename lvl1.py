import pygame
from src.window import Window
from src.tablero import Tablero
from src.rooks import *
from src.avatars import AvatarsManager
from src.monedas import MonedasManager


class Level1(Window):
    def __init__(self):
        super().__init__()
        self.tablero = Tablero(self.RESOLUTION)
        self.clock = pygame.time.Clock()
        self.monedas = 0
        self.avatars = AvatarsManager(self.tablero, spawn_interval=10, max_avatars=10) 
        self.monedas_coleccionables = MonedasManager(self.tablero, spawn_interval=5)

        self.rooks_tipos = [
            ("Sand Rook", SandRook),
            ("Rock Rook", RockRook),
            ("Fire Rook", FireRook),
            ("Water Rook", WaterRook)
        ]

        self.botones = []
        self.rook_seleccionada = None
        self.crear_botones()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                monedas_ganadas = self.monedas_coleccionables.handle_click(pos)
                if monedas_ganadas > 0:
                    self.monedas += monedas_ganadas
                    return
                
                for rect, nombre, _ in self.botones:
                    if rect.collidepoint(pos):
                        self.rook_seleccionada = next(r for r in self.rooks_tipos if r[0] == nombre)
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

    def render(self):
        self.screen.blit(self.game_image, (0, 0))
        self.tablero.draw(self.screen)
        self.avatars.draw(self.screen)
        self.monedas_coleccionables.draw(self.screen)
        self.cant_monedas = self.font.render(f"Monedas: {self.monedas}", True, (255, 255, 0))
        self.screen.blit(self.cant_monedas, (40, 30))

        for rect, nombre, image in self.botones:
            pygame.draw.rect(self.screen, (230, 230, 230), rect)
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)

            img_rect = image.get_rect(center=rect.center)
            self.screen.blit(image, img_rect)

            rook_class = next(r for n, r in self.rooks_tipos if n == nombre)
            costo = rook_class.costo
            costo_text = self.font.render(f"{costo}", True, (255, 255, 255))
            costo_pos = (rect.right + 15, rect.centery - costo_text.get_height() // 2)
            self.screen.blit(costo_text, costo_pos)

            if self.rook_seleccionada and self.rook_seleccionada[0] == nombre:
                pygame.draw.rect(self.screen, (255, 215, 0), rect, 4)

        pygame.display.flip()

    def move(self):
        self.avatars.move()

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.tablero.update()
            monedas_ganadas = self.avatars.update()
            self.monedas += monedas_ganadas
            self.monedas_coleccionables.update()
            self.tablero.limpiar_rooks_muertos()
            self.render()
            self.clock.tick(60)
            
if __name__ == "__main__":
    Level1().run()
