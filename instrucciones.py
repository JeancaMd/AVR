import pygame
from src import Button
from src.window import Window

class Instrucciones(Window):
    def __init__(self):
        super().__init__()

        # Oscurecer pantalla
        self.s = pygame.Surface(self.RESOLUTION)
        self.s.set_alpha(110)

        # Texto de las instrucciones
        self.instructions = [
            "Cada 5 segundos aparecen monedas.",
            "Cada 10 segundos aparecen los avatars.",
            "Para construir una torre primero debes",
            "seleccionarla y darle click al lugar",
            "donde desees construirla."
        ]
        
        ##-- Boton de volver
        self.back_buttonx = Button.Button(self.RESOLUTION[0]/12, self.RESOLUTION[1]/1.05, self.back_button, self.screen, 0.07)
        
        # Preparar las superficies de texto para las instrucciones
        self.instruction_font = pygame.font.SysFont('Arial', 32)
        self.instruction_surfaces = []
        self.instruction_rects = []
        
        for i, instruction in enumerate(self.instructions):
            surface = self.instruction_font.render(instruction, 1, (255, 255, 255))
            rect = surface.get_rect(center=(self.RESOLUTION[0] / 2, 200 + i * 60))
            self.instruction_surfaces.append(surface)
            self.instruction_rects.append(rect)

    def render(self):
        # Fondo
        self.screen.blit(self.menu_image, (0, 0))
        self.screen.blit(self.s, (0,0))
        
        
        # Dibujar instrucciones
        for surface, rect in zip(self.instruction_surfaces, self.instruction_rects):
            self.screen.blit(surface, rect)
        
        # Dibujar botón de volver
        if self.back_buttonx.draw():
                from main import Main
                self.cambiar_ventana(Main)
        
        
        pygame.display.flip()