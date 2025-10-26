import pygame
from src import Button
from src.window import Window
from database import GrupoCajetaDB

pygame.init()


class MainMenu(Window):
    def __init__(self):
        super().__init__()
        print(self.user)

        self.center_x = self.RESOLUTION[0] / 2
        self.alt_font = pygame.font.SysFont("High tower text", 40)
        
        ##-- Botón Iniciar
        self.start_button = Button.Button(
            self.center_x, 
            self.RESOLUTION[1] / 1.68, 
            self.menu_button, 
            self.screen, 
            self.BUTTON_X
        )
        self.label_start = self.font.render("Iniciar Juego", True, (206, 143, 31))
        self.start_rect = self.label_start.get_rect(center=self.start_button.rect.center)


        ##-- Botón Opciones
        self.options_button = Button.Button(
            self.center_x, 
            self.RESOLUTION[1] / 1.36, 
            self.menu_button, 
            self.screen, 
            self.BUTTON_X
        )
        self.label_options = self.font.render("Opciones", True, (206, 143, 31))
        self.options_rect = self.label_options.get_rect(center=self.options_button.rect.center)

        ##-- Botón Salir
        self.exit_button = Button.Button(
            self.center_x, 
            self.RESOLUTION[1] / 1.14, 
            self.menu_button, 
            self.screen, 
            self.BUTTON_X
        )
        self.label_exit = self.font.render("Salir", True, (206, 143, 31))
        self.exit_rect = self.label_exit.get_rect(center=self.exit_button.rect.center)

        self.welcome_text = self.alt_font.render(f"Bienvenido: {self.user}", 1, (206,143,31))
        self.rect_welcome = self.welcome_text.get_rect(midtop=(self.RESOLUTION[0] / 2, 35))                                 
                                             
    def render(self):
        from options_menu import Options
        self.screen.blit(self.menu_image, (0, 0))

        if self.start_button.draw():
            print("INICIAR")
        if self.options_button.draw():
            self.cambiar_ventana(Options)
        if self.exit_button.draw():
            self.running = False

        self.screen.blit(self.label_start, self.start_rect)
        self.screen.blit(self.label_options, self.options_rect)
        self.screen.blit(self.label_exit, self.exit_rect)
        self.screen.blit(self.welcome_text, self.rect_welcome)



        pygame.display.flip()
