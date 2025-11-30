import pygame
from src.window import Window
from src.menu_base import BaseMenu


pygame.init()

class MainMenu(Window):
    def __init__(self):
        super().__init__()
        pygame.display.set_caption("MENÚ PRINCIPAL")
        self.menu = BaseMenu(self)
        self.alt_font = pygame.font.SysFont("High tower text", 40)

        ### Configurar posiciones
        center_x = self.RESOLUTION[0] / 2
        start_y = self.RESOLUTION[1] / 1.5
        spacing = 120

        left_x = center_x - 150
        right_x = center_x + 150

        ### Agregar botones con BaseMenu
        self.menu.añadir_boton("start", left_x, start_y, "Iniciar Juego")
        self.menu.añadir_boton("options", right_x, start_y, "Opciones")
        self.menu.añadir_boton("fame", left_x, start_y + spacing, "Salón de la Fama")
        self.menu.añadir_boton("exit", right_x, start_y + spacing, "Salir")

        ### Texto de bienvenida
        self.welcome_text = self.alt_font.render(f"Bienvenido: {self.user}", True, (206, 143, 31))
        self.rect_welcome = self.welcome_text.get_rect(midtop=(self.RESOLUTION[0] / 2, 35))

        ### Botón de ayuda
        from src import Button
        self.help_btn = Button.Button(
            self.RESOLUTION[0] / 1.1, 
            self.RESOLUTION[1] / 1.05, 
            self.menu_button, 
            self.screen, 
            0.07
        )
        self.label_help = self.font.render("?", 1, (206, 143, 31))
        self.help_rect = self.label_help.get_rect(center=(self.help_btn.rect.centerx, self.help_btn.rect.centery))
        
        self.menu.buttons.append({
            "name": "help",
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

# -----------------------------------------------------------------------------------
#  Confirmar click en botones
# -----------------------------------------------------------------------------------
    def confirmar(self, nombre):
        from options_menu import OptionsMenu
        from fama import SalonFama
        from lvl1 import Level1
        from instrucciones import Instrucciones

        if nombre == "start":
            self.cambiar_ventana(Level1)
        elif nombre == "options":
            self.cambiar_ventana(OptionsMenu)
        elif nombre == "fame":
            self.cambiar_ventana(SalonFama)
        elif nombre == "exit":
            self.running = False
        elif nombre == "help":
            self.cambiar_ventana(Instrucciones)

# -----------------------------------------------------------------------------------
# Handle events desde MenuBase
# -----------------------------------------------------------------------------------
    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self.menu.handle_keyboard(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.menu.handle_mouse(event.pos)

        comando = self.control.obtener_evento()
        if comando:
            self.menu.handle_udp(comando)

# -----------------------------------------------------------------------------------
# Render
# -----------------------------------------------------------------------------------
    def render(self):
        self.screen.blit(self.menu_image, (0, 0))

        ### Renderizar botones usando BaseMenu
        for i, item in enumerate(self.menu.buttons):
            button = item["button"]
            label = item["label"]
            label_rect = item["label_rect"]

            button.draw()

            ### Borde en boton seleccionado
            if i == self.menu.selected_index:
                pygame.draw.rect(self.screen, (255, 215, 0), button.rect, 5)

            label_rect.center = button.rect.center
            self.screen.blit(label, label_rect)

        self.screen.blit(self.welcome_text, self.rect_welcome)

        pygame.display.flip()

