import pygame
from src.window import Window
from src.menu_base import BaseMenu
from src import Button
from instrucciones import Instrucciones 


class JuegoInstrucciones(Window):
    def __init__(self):
        super().__init__()
        self.s = pygame.Surface(self.RESOLUTION)
        self.s.set_alpha(200)

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

        # Control UDP
        try:
            self.control = self.control
        except:
            from src.cliente import ControladorUDP
            self.control = ControladorUDP()


        ### --- Textos 
        self.titulo = self.font.render("Mecánica de juego", True, (255, 255, 255))

        self.texto = self.font.render("El objetivo colocar Rooks estrategicamente para evitar\n     " \
        "que los Avatars lleguen hasta el final del tablero", True, (255,255,255))

        self.texto2 = self.font.render("Cada 5 segundos apareceran monedas de diferentes valores \n                         " \
        "Verde: 25, Amarillo: 50, Rojo: 100", True, (255,255,255))

        self.texto3 = self.font.render("Cada vez que elimines un Avatar, se te sumarán 75 monedas", True, (255,255,255))

        self.titulo2 = self.font.render("Controles", True, (255, 255, 255))

        self.titulo3 = self.font.render("Control", True, (255, 255, 255))

        self.texto4 = self.font.render("[Joystick]: Mover     [O]: Recoger moneda     [X]: Colocar Rook\n                      "
        "[Δ]: Modo Tablero     [□]: Modo Rook", True, (255,255,255))

        self.titulo4 = self.font.render("Teclado", True, (255, 255, 255))

        self.texto5 = self.font.render("[Flechas]: Mover     [D]: Recoger moneda     [Enter]: Colocar Rook\n                      "
        "[S]: Modo Tablero     [A]: Modo Rook", True, (255,255,255))


        ### Lista de elementos para evitar sobrecargar en render()
        self.elementos = [
            (self.menu_image, (0, 0)),
            (self.s, (0, 0)),
            (self.titulo, (self.RESOLUTION[0]//2.4, 50)),
            (self.texto, (self.RESOLUTION[0]//6, 100)),
            (self.texto2, (self.RESOLUTION[0]//8, 190)),
            (self.texto3, (self.RESOLUTION[0]//8, 280)),
            (self.titulo2, (self.RESOLUTION[0]//2.2, 340)),
            (self.titulo3, (self.RESOLUTION[0]//2.15, 400)),
            (self.titulo4, (self.RESOLUTION[0]//2.15, 530)),
            (self.texto4, (self.RESOLUTION[0]//11, 440)),
            (self.texto5, (self.RESOLUTION[0]//11, 560))
        ]


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
        ### Dibujar elementos de la lista
        for elemento, pos in self.elementos:
            self.screen.blit(elemento, pos)

        for i, item in enumerate(self.menu.buttons):
            button = item["button"]
            label = item["label"]
            label_rect = item["label_rect"]

            button.draw()

        if i == self.menu.selected_index:
            pygame.draw.rect(self.screen, (255, 215, 0), button.rect, 5)

        label_rect.center = button.rect.center
        self.screen.blit(label, label_rect)

        pygame.display.flip()

