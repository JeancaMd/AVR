import pygame
import time
from src.window import Window

class TransitionWindow(Window):
    def __init__(self, texto="Preparando siguiente nivel", duracion=3, siguiente_clase=None):
        super().__init__()
        self.texto = texto
        self.duracion = duracion
        self.siguiente_clase = siguiente_clase
        self.clock = pygame.time.Clock()

        self.render_texto = self.font.render(texto, True, (255, 255, 255))
        self.start_time = time.time()

    def run(self):
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.blit(self.game_image, (0, 0))

            rect = self.render_texto.get_rect(center=(self.RESOLUTION[0]//2,
                                                      self.RESOLUTION[1]//2))
            self.screen.blit(self.render_texto, rect)
            pygame.display.flip()
            self.clock.tick(60)

            if time.time() - self.start_time >= self.duracion:
                self.running = False

        if self.siguiente_clase is not None:
            ventana = self.siguiente_clase()
            ventana.run()
