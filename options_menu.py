import pygame
from src.window import Window
from src import Button

class OptionsMenu(Window):
    def __init__(self):
        super().__init__()
        self.center_x = self.RESOLUTION[0] / 2
        start_y = self.RESOLUTION[1] / 2.5
        spacing = 120

        # Botón 3: Temas - abre el menú de temas
        self.themes_button = Button.Button(self.center_x, start_y, self.menu_button, self.screen, self.BUTTON_X)
        self.label_themes = self.font.render("Temas", True, (206, 143, 31))
        self.themes_rect = self.label_themes.get_rect(center=self.themes_button.rect.center)

        # Botón 1: Spotify - abre el reproductor de música
        self.spotify_button = Button.Button(self.center_x, start_y + spacing, self.menu_button, self.screen, self.BUTTON_X)
        self.label_spotify = self.font.render("Reproductor Spotify", True, (206, 143, 31))
        self.spotify_rect = self.label_spotify.get_rect(center=self.spotify_button.rect.center)

        # Botón 2: Sin función (por ahora) 
        self.button2 = Button.Button(self.center_x, start_y + spacing * 2, self.menu_button, self.screen, self.BUTTON_X)
        self.label_button2 = self.font.render("Configuración 2", True, (206, 143, 31))
        self.button2_rect = self.label_button2.get_rect(center=self.button2.rect.center)

        # Botón de volver
        self.back_buttonx = Button.Button(self.RESOLUTION[0]/12, self.RESOLUTION[1]/1.05, self.back_button, self.screen, 0.07)

        self.title_text = self.font.render("OPCIONES", True, (206, 143, 31))
        self.title_rect = self.title_text.get_rect(midtop=(self.RESOLUTION[0] / 2, 50))

    def render(self):
        self.screen.blit(self.menu_image, (0, 0))

        # Dibujar título
        self.screen.blit(self.title_text, self.title_rect)

        # Botón de Spotify - abre el reproductor de música
        spotify_clicked = self.spotify_button.draw()
        if spotify_clicked and self.verificar_click_valido():
            from spotify_window import SpotifyWindow
            self.cambiar_ventana(SpotifyWindow)

        # Botón sin función (por ahora)
        if self.button2.draw() and self.verificar_click_valido():
            print("Configuración 2 presionada - Sin función aún")

        # Botón de Temas - abre el menú de temas
        if self.themes_button.draw() and self.verificar_click_valido():
            from themes_menu import ThemesMenu
            self.cambiar_ventana(ThemesMenu)

        # Botón de volver - regresa al menú principal
        if self.back_buttonx.draw() and self.verificar_click_valido():
            from start_menu import MainMenu
            self.cambiar_ventana(MainMenu)

        # Dibujar labels de los botones
        self.screen.blit(self.label_spotify, self.spotify_rect)
        self.screen.blit(self.label_button2, self.button2_rect)
        self.screen.blit(self.label_themes, self.themes_rect)

        pygame.display.flip()

    def verificar_click_valido(self):
        """Verifica que el clic sea válido (no un clic fantasma)"""
        # Pequeño delay para evitar clics inmediatos al abrir el menú
        tiempo_actual = pygame.time.get_ticks()
        if not hasattr(self, 'tiempo_apertura'):
            self.tiempo_apertura = tiempo_actual
        
        # Esperar al menos 300ms después de abrir el menú antes de aceptar clics
        return tiempo_actual - self.tiempo_apertura > 300