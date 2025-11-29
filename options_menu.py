import pygame
from src.window import Window
from src.menu_base import BaseMenu
from src.cliente import ControladorUDP


class OptionsMenu(Window):
    def __init__(self, pico_ip="192.168.0.107"):
        super().__init__()
        self.menu = BaseMenu(self)

        ### Configurar posiciones
        center_x = self.RESOLUTION[0] / 2
        start_y = self.RESOLUTION[1] / 1.5
        spacing = 120

        left_x = center_x - 150
        right_x = center_x + 150

        ### Agregar botones con BaseMenu
        self.menu.añadir_boton("temas", left_x, start_y, "Temas")
        self.menu.añadir_boton("spotify", right_x, start_y, "Spotify")
        self.menu.añadir_boton("config2", left_x, start_y + spacing, "Configuración")
        self.menu.añadir_boton("volver", right_x, start_y + spacing, "Volver")

        self.title_text = self.font.render("OPCIONES", True, (206, 143, 31))
        self.title_rect = self.title_text.get_rect(midtop=(self.RESOLUTION[0] / 2, 50))

        ### Control UDP
        try:
            self.control = self.control
        except:
            self.control = ControladorUDP(pico_ip)

# -----------------------------------------------------------------------------------
#  Click confirmar en botones
# -----------------------------------------------------------------------------------
    def confirmar(self, nombre):
        if nombre == "temas":
            from themes_menu import ThemesMenu
            self.cambiar_ventana(ThemesMenu)

        elif nombre == "spotify":
            from spotify_window import SpotifyWindow
            self.cambiar_ventana(SpotifyWindow)

        elif nombre == "config2":
            print("Configuración 2 presionada - Sin función aún")

        elif nombre == "volver":
            from start_menu import MainMenu
            self.cambiar_ventana(MainMenu)

# -----------------------------------------------------------------------------------
#   Handle events desde MenuBase
# -----------------------------------------------------------------------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from start_menu import MainMenu
                    self.cambiar_ventana(MainMenu)
                else:
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
        self.screen.blit(self.title_text, self.title_rect)

        for i, item in enumerate(self.menu.buttons):
            btn = item["button"]
            lbl = item["label"]
            lbl_rect = item["label_rect"]

            btn.draw()

            if i == self.menu.selected_index:
                pygame.draw.rect(self.screen, (255, 215, 0), btn.rect, 4)

            lbl_rect.center = btn.rect.center
            self.screen.blit(lbl, lbl_rect)

        pygame.display.flip()