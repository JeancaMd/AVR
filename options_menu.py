import pygame
from src.window import Window
from src import Button

class Options(Window):
    def __init__(self):
        super().__init__()
        self.center_x = self.RESOLUTION[0] / 2

    ##-- Botón Tema Oscuro
        self.theme0_button = Button.Button(
            self.center_x, 
            self.RESOLUTION[1] / 1.6, 
            self.menu_button, 
            self.screen, 
            self.BUTTON_X
        )
        self.label_theme0 = self.font.render("Tema 0", True, (206, 143, 31))
        self.theme0_rect = self.label_theme0.get_rect(center=self.theme0_button.rect.center)
                                                      
    ##-- Botón Tema Claro
        self.theme1_button = Button.Button(
            self.center_x, 
            self.RESOLUTION[1] / 1.30, 
            self.menu_button, 
            self.screen, 
            self.BUTTON_X
        )
        self.label_theme1 = self.font.render("Tema 1", True, (206, 143, 31))
        self.theme1_rect = self.label_theme1.get_rect(center=self.theme1_button.rect.center)

    ##-- Botón Tema Navidad
        self.theme2_button = Button.Button(
            self.center_x, 
            self.RESOLUTION[1] / 1.1, 
            self.menu_button, 
            self.screen, 
            self.BUTTON_X
        )
        self.label_theme2 = self.font.render("Tema 2", True, (206, 143, 31))
        self.theme2_rect = self.label_theme2.get_rect(center=self.theme2_button.rect.center)



    def render(self):
        self.screen.blit(self.menu_image, (0, 0))

        if self.theme0_button.draw():
            self.actualizar_tema(0)
            self.db.actualizar_tema(self.user, self.tema)

        if self.theme1_button.draw():
            self.actualizar_tema(1)
            self.db.actualizar_tema(self.user, self.tema)
        
        if self.theme2_button.draw():
            self.actualizar_tema(2)
            self.db.actualizar_tema(self.user, self.tema)

        self.screen.blit(self.label_theme1, self.theme1_rect)
        self.screen.blit(self.label_theme0, self.theme0_rect)
        self.screen.blit(self.label_theme2, self.theme2_rect)

        pygame.display.flip()

    def run(self):
        from database import GrupoCajetaDB
        self.db = GrupoCajetaDB()
        if not self.db.conectar():
            self.mostrar_error("No se pudo conectar a la base de datos")
            return

        while self.running:
            self.handle_events()
            self.render()
        
        self.db.cerrar()
