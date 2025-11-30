import pygame
from src.window import Window
from src.menu_base import BaseMenu
from src import Button
from instrucciones import Instrucciones 


class RooksInstrucciones(Window):
    def __init__(self):
        super().__init__()
        self.s = pygame.Surface(self.RESOLUTION)
        self.s.set_alpha(180)
        self.titulo = self.font.render("Tipos de Rooks", True, (255, 255, 255))
        self.texto = self.font.render("La frecuencia de ataque para todas las Rooks es de 4 segundos", True, (255,255,255))
        self.menu = BaseMenu(self)

        self.help_btn = Button.Button(
            self.RESOLUTION[0] / 1.1, 
            self.RESOLUTION[1] / 1.05, 
            self.menu_button, 
            self.screen, 
            0.07
        )
        self.label_help = self.font.render("Volver", 1, (206, 143, 31))
        self.help_rect = self.label_help.get_rect(center=(self.help_btn.rect.centerx, self.help_btn.rect.centery))

        self.menu.buttons.append({
            "name": "volver",
            "button": self.help_btn,
            "label": self.label_help,
            "label_rect": self.help_rect
        })

        ### Control UDP
        try:
            self.control = self.control
        except:
            from src.cliente import ControladorUDP
            self.control = ControladorUDP()

        ### Rutas imagenes
        self.images_paths = [
            "assets/images/ui/sand_rook.png",
            "assets/images/ui/rock_rook.png",
            "assets/images/ui/fire_rook.png",
            "assets/images/ui/water_rook.png",
        ]

        ### Texto por avatar
        self.textos = [
            ["SandRook", "Ataque: 2", "Vida: 3", "Costo: 50"],
            ["RockRook", "Ataque: 4", "Vida: 14", "Costo: 100"],
            ["FireRook", "Ataque: 8", "Vida: 16", "Costo: 150"],
            ["WaterRook", "Ataque: 8", "Vida: 16", "Costo: 150"],
        ]

        ### Cargar imágenes
        self.rooks = []
        for path in self.images_paths:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (140, 130))
            self.rooks.append(img)


    def confirmar(self, nombre):
        if nombre == "volver":
            from instrucciones import Instrucciones
            self.cambiar_ventana(Instrucciones)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                   self.cambiar_ventana(Instrucciones)
                else:
                    self.menu.handle_keyboard(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.menu.handle_mouse(event.pos)

        comando = self.control.obtener_evento()
        if comando:
            self.menu.handle_udp(comando)


    def render(self):
        self.screen.blit(self.menu_image, (0, 0))
        self.screen.blit(self.s, (0, 0))
        self.screen.blit(self.titulo, (self.RESOLUTION[0]//2.4, 100))
        self.screen.blit(self.texto, (self.RESOLUTION[0]//10, 530))


        ### Tamaño de cada celda
        cell_width = self.RESOLUTION[0] // 2.2
        cell_height = self.RESOLUTION[1] // 2

        ### Tamaños dentro de la celda
        x_img_offset = 60
        y_img_offset = 180
        x_text_offset = 215
        line_spacing = 28

        for i, img in enumerate(self.rooks):
            row = i // 2      # 0 o 1
            col = i % 2      # 0 o 1

            ### Coordenadas base de la celda
            cell_x = col * cell_width
            cell_y = (self.RESOLUTION[1] / 2) + (row * cell_height * 0.5)

            ### Posición dentro de la celda
            x_img = cell_x + x_img_offset
            y_img = cell_y - y_img_offset 

            ### Dibujar rook
            rect = img.get_rect(topleft=(x_img, y_img))
            self.screen.blit(img, rect)

            ### Texto a la derecha
            x_text = cell_x + x_text_offset
            y_text = y_img

            for j, linea in enumerate(self.textos[i]):
                label = self.font.render(linea, True, (255, 255, 255))
                label_rect = label.get_rect(topleft=(x_text, y_text + j * line_spacing))
                self.screen.blit(label, label_rect)

            for i, item in enumerate(self.menu.buttons):
                button = item["button"]
                label = item["label"]
                label_rect = item["label_rect"]

                button.draw()

            ### Borde dorado
            if i == self.menu.selected_index:
                pygame.draw.rect(self.screen, (255, 215, 0), button.rect, 5)

            label_rect.center = button.rect.center
            self.screen.blit(label, label_rect)

        pygame.display.flip()


if __name__ == "__main__":
    RooksInstrucciones().run()
