import pygame
from src.window import Window
from src import Button
from database import GrupoCajetaDB

class ThemesMenu(Window):
    def __init__(self):
        super().__init__()
        self.center_x = self.RESOLUTION[0] / 2
        start_y = self.RESOLUTION[1] / 2.5
        spacing = 120

        ##-- Botón Tema Original
        self.theme0_button = Button.Button(
            self.center_x, 
            start_y, 
            self.menu_button, 
            self.screen, 
            self.BUTTON_X
        )
        self.label_theme0 = self.font.render("Tema Original", True, (206, 143, 31))
        self.theme0_rect = self.label_theme0.get_rect(center=self.theme0_button.rect.center)
                                                      
        ##-- Botón Tema Desértico
        self.theme1_button = Button.Button(
            self.center_x, 
            start_y + spacing, 
            self.menu_button, 
            self.screen, 
            self.BUTTON_X
        )
        self.label_theme1 = self.font.render("Tema Desértico", True, (206, 143, 31))
        self.theme1_rect = self.label_theme1.get_rect(center=self.theme1_button.rect.center)

        ##-- Botón Tema Navidad
        self.theme2_button = Button.Button(
            self.center_x, 
            start_y + spacing * 2, 
            self.menu_button, 
            self.screen, 
            self.BUTTON_X
        )
        self.label_theme2 = self.font.render("Tema Navideño", True, (206, 143, 31))
        self.theme2_rect = self.label_theme2.get_rect(center=self.theme2_button.rect.center)

        ##-- Botón de volver
        self.back_buttonx = Button.Button(self.RESOLUTION[0]/12, self.RESOLUTION[1]/1.05, self.back_button, self.screen, 0.07)

        self.title_text = self.font.render("SELECCIONAR TEMA", True, (206, 143, 31))
        self.title_rect = self.title_text.get_rect(midtop=(self.RESOLUTION[0] / 2, 50))

    def render(self):
        self.screen.blit(self.menu_image, (0, 0))

        # Dibujar título
        self.screen.blit(self.title_text, self.title_rect)

        # Botones de temas
        if self.theme0_button.draw():
            self.actualizar_tema(0)
            self.db.actualizar_tema(self.user, self.tema)

        if self.theme1_button.draw():
            self.actualizar_tema(1)
            self.db.actualizar_tema(self.user, self.tema)
        
        if self.theme2_button.draw():
            self.actualizar_tema(2)
            self.db.actualizar_tema(self.user, self.tema)

        # Botón de volver - regresa al menú de opciones
        if self.back_buttonx.draw():
            from options_menu import OptionsMenu  # Import aquí para evitar circular
            self.cambiar_ventana(OptionsMenu)

        # Dibujar labels de los temas
        self.screen.blit(self.label_theme0, self.theme0_rect)
        self.screen.blit(self.label_theme1, self.theme1_rect)
        self.screen.blit(self.label_theme2, self.theme2_rect)

        pygame.display.flip()

    def run(self):
        self.db = GrupoCajetaDB()
        if not self.db.conectar():
            self.mostrar_error("No se pudo conectar a la base de datos")
            return

        while self.running:
            self.handle_events()
            self.render()
        
        self.db.cerrar()
        
        # Esto es importante: ejecutar la siguiente ventana después de cerrar la BD
        if self.next_window:
            nueva_ventana = self.next_window()
            nueva_ventana.run()