import pygame
from src import Button
from src.window import Window
from database import GrupoCajetaDB

pygame.init()


class MainMenu(Window):
    def __init__(self):
        super().__init__()
        print(self.user)

        pygame.display.set_caption("MENÚ PRINCIPAL")

        self.center_x = self.RESOLUTION[0] / 2
        self.alt_font = pygame.font.SysFont("High tower text", 40)
        
        start_y = self.RESOLUTION[1] / 2.35  # Primer botón (como tenías)
        spacing = 120                        # Espaciado entre botones (ajústalo a gusto)

        self.start_button = Button.Button(self.center_x, start_y, self.menu_button, self.screen, self.BUTTON_X)
        self.label_start = self.font.render("Iniciar Juego", True, (206, 143, 31))
        self.start_rect = self.label_start.get_rect(center=self.start_button.rect.center)

        self.options_button = Button.Button(self.center_x, start_y + spacing, self.menu_button, self.screen, self.BUTTON_X)
        self.label_options = self.font.render("Opciones", True, (206, 143, 31))
        self.options_rect = self.label_options.get_rect(center=self.options_button.rect.center)

        self.fame_button = Button.Button(self.center_x, start_y + spacing * 2, self.menu_button, self.screen, self.BUTTON_X)
        self.label_fame = self.font.render("Salón de la Fama", True, (206, 143, 31))
        self.fame_rect = self.label_fame.get_rect(center=self.fame_button.rect.center)

        self.exit_button = Button.Button(self.center_x, start_y + spacing * 3, self.menu_button, self.screen, self.BUTTON_X)
        self.label_exit = self.font.render("Salir", True, (206, 143, 31))
        self.exit_rect = self.label_exit.get_rect(center=self.exit_button.rect.center)


        self.welcome_text = self.alt_font.render(f"Bienvenido: {self.user}", 1, (206,143,31))
        self.rect_welcome = self.welcome_text.get_rect(midtop=(self.RESOLUTION[0] / 2, 35))                                 
                                             
    def render(self):
        from options_menu import OptionsMenu
        from fama import SalonFama
        from lvl1 import Level1
        self.screen.blit(self.menu_image, (0, 0))

        if self.start_button.draw():
            self.cambiar_ventana(Level1)
        if self.fame_button.draw():
            self.cambiar_ventana(SalonFama)
        if self.options_button.draw():
            self.cambiar_ventana(OptionsMenu)
        if self.exit_button.draw():
            self.running = False

        self.screen.blit(self.label_start, self.start_rect)
        self.screen.blit(self.label_options, self.options_rect)
        self.screen.blit(self.label_exit, self.exit_rect)
        self.screen.blit(self.label_fame, self.fame_rect)
        self.screen.blit(self.welcome_text, self.rect_welcome)



        pygame.display.flip()
