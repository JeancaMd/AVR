import pygame
from database import GrupoCajetaDB
from src.window import Window
from src import Button

pygame.init()

class SalonFama(Window):
    def __init__(self):
        super().__init__()
        self.db = GrupoCajetaDB()
        self.db.conectar()

        # Cargar puntajes desde la base de datos
        self.puntajes = self.db.obtener_mejores_puntajes(limite=5)
        self.db.cerrar()

        # Centro horizontal
        self.center_x = self.RESOLUTION[0] // 2

        # Fuente para los textos
        self.title_font = pygame.font.SysFont("High Tower Text", 60, bold=True)
        self.score_font = pygame.font.SysFont("High Tower Text", 40)
        self.info_font = pygame.font.SysFont("High Tower Text", 28)

        # Botón Volver
        self.back_button = Button.Button(
            self.center_x,
            self.RESOLUTION[1] * 0.88,
            self.menu_button,
            self.screen,
            self.BUTTON_X
        )
        self.back_label = self.font.render("Volver al menú principal", True, (206, 143, 31))
        self.back_rect = self.back_label.get_rect(center=self.back_button.rect.center)

        # Texto estático
        self.title = self.title_font.render("🏆 SALÓN DE LA FAMA 🏆", True, (255, 215, 0))
        self.title_rect = self.title.get_rect(center=(self.center_x, self.RESOLUTION[1] * 0.15))

    def render(self):
        """Dibuja la pantalla del salón de la fama."""
        self.screen.blit(self.menu_image, (0, 0))

        # Título
        self.screen.blit(self.title, self.title_rect)

        # Mostrar puntajes
        start_y = self.RESOLUTION[1] * 0.30
        line_height = 60

        if self.puntajes:
            for i, (nombre, puntos) in enumerate(self.puntajes, start=1):
                texto = f"{i}. {nombre} — {int(puntos):,} pts"
                render = self.score_font.render(texto, True, (255, 255, 255))
                rect = render.get_rect(center=(self.center_x, start_y + (i - 1) * line_height))
                self.screen.blit(render, rect)
        else:
            mensaje = self.info_font.render("Aún no hay puntajes registrados.", True, (200, 200, 200))
            rect = mensaje.get_rect(center=(self.center_x, self.RESOLUTION[1] * 0.5))
            self.screen.blit(mensaje, rect)

        # Botón Volver
        if self.back_button.draw():
            from start_menu import MainMenu
            self.cambiar_ventana(MainMenu)

        self.screen.blit(self.back_label, self.back_rect)
        pygame.display.flip()

    def run(self):
        """Bucle principal de la pantalla."""
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    return
            self.render()
