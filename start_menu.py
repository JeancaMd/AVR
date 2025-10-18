import pygame
from src import Button
from src.window import Window

pygame.init()


class MainMenu(Window):
    def __init__(self):
        super().__init__()

        ##-- Configuración de posiciones
        center_x = self.RESOLUTION[0] / 2
        
        ##-- Botón Iniciar
        self.start_button = Button.Button(
            center_x, 
            self.RESOLUTION[1] / 1.68, 
            self.menu_button, 
            self.screen, 
            self.BUTTON_X
        )
        self.label_start = self.font.render("Iniciar Juego", True, (206, 143, 31))
        self.start_rect = self.label_start.get_rect(center=self.start_button.rect.center)

        ##-- Botón Opciones
        self.options_button = Button.Button(
            center_x, 
            self.RESOLUTION[1] / 1.36, 
            self.menu_button, 
            self.screen, 
            self.BUTTON_X
        )
        self.label_options = self.font.render("Opciones", True, (206, 143, 31))
        self.options_rect = self.label_options.get_rect(center=self.options_button.rect.center)

        ##-- Botón Salir
        self.exit_button = Button.Button(
            center_x, 
            self.RESOLUTION[1] / 1.14, 
            self.menu_button, 
            self.screen, 
            self.BUTTON_X
        )
        self.label_exit = self.font.render("Salir", True, (206, 143, 31))
        self.exit_rect = self.label_exit.get_rect(center=self.exit_button.rect.center)

    def render(self):
        self.screen.blit(self.menu_image, (0, 0))

        if self.start_button.draw():
            print("INICIAR")
        if self.options_button.draw():
            print("OPCIONES")
        if self.exit_button.draw():
            self.running = False

        self.screen.blit(self.label_start, self.start_rect)
        self.screen.blit(self.label_options, self.options_rect)
        self.screen.blit(self.label_exit, self.exit_rect)

        pygame.display.flip()
