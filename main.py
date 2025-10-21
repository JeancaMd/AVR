import pygame
from src import Button
from register_menu import MenuRegistro
from src.window import Window
from login_menu import LoginMenu

pygame.init()

class Main(Window):
    def __init__(self):
        super().__init__()

        ##-- Botones y textos
        self.login_btn = Button.Button(self.RESOLUTION[0] / 2, self.RESOLUTION[1] / 1.6, self.menu_button, self.screen, self.BUTTON_X)
        self.label_login = self.font.render("Iniciar Sesion", 1, (206,143,31))

        self.register_btn = Button.Button(self.RESOLUTION[0] / 2, self.RESOLUTION[1] / 1.23, self.menu_button, self.screen, self.BUTTON_X)
        self.label_register = self.font.render("Registrarse", 1, (206,143,31))

        ##Obtener el centro del boton para mantener el texto dentro de este margen
        self.login_rect = self.label_login.get_rect(center=(self.login_btn.rect.centerx, self.login_btn.rect.centery))
        self.register_rect = self.label_register.get_rect(center=(self.register_btn.rect.centerx, self.register_btn.rect.centery))

        
    def render(self):
            self.screen.blit(self.menu_image, (0, 0))

            if self.login_btn.draw():
                print("Iniciar Sesión")
                self.running = False
                self.cambiar_ventana(LoginMenu)
            if self.register_btn.draw():
                print("Registrar")
                self.running = False
                self.cambiar_ventana(MenuRegistro)

            self.screen.blit(self.label_login, self.login_rect)
            self.screen.blit(self.label_register, self.register_rect)

            pygame.display.flip()


if __name__ == "__main__":
    menu = Main()
    menu.run()

