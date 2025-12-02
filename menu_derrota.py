import pygame
from src.window import Window
from src.menu_base import BaseMenu
from src.cliente import ControladorUDP

class DefeatWindow(Window):
    def __init__(self):
        super().__init__()
        self.menu = BaseMenu(self)
        self.s = pygame.Surface(self.RESOLUTION)
        self.s.set_alpha(180)

        self.alt_font = pygame.font.SysFont("High tower text", 40)
        self.titulo = self.alt_font.render("DERROTA", True, (206, 143, 31))
        self.texto = self.alt_font.render("Los Avatars entraron a tu base", True, (206, 143, 31))

        ### Configurar posiciones
        center_x = self.RESOLUTION[0] / 2
        start_y = self.RESOLUTION[1] / 1.5

        left_x = center_x - 150
        right_x = center_x + 150
                
        self.menu.añadir_boton("jugar", left_x, start_y, "Volver a jugar")
        self.menu.añadir_boton("menu", right_x, start_y, "Menu principal")

        ### Control UDP
        try:
            # Intentar reutilizar el control existente de Window
            if hasattr(Window, 'control') and Window.control:
                self.control = Window.control
            else:
                self.control = ControladorUDP()
        except:
            self.control = ControladorUDP()

# -----------------------------------------------------------------------------------
#  Click confirmar en botones
# -----------------------------------------------------------------------------------
    def confirmar(self, nombre):
        if nombre == "jugar":
            from lvl1 import Level1
            self.cambiar_ventana(Level1)

        elif nombre == "menu":
            from start_menu import MainMenu 
            self.cambiar_ventana(MainMenu)

# -----------------------------------------------------------------------------------
#   Handle events desde MenuBase
# -----------------------------------------------------------------------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.next_window = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from start_menu import MainMenu
                    self.cambiar_ventana(MainMenu)
                else:
                    self.menu.handle_keyboard(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.menu.handle_mouse(event.pos)

        comando = self.control.obtener_evento()
        if comando:
            self.menu.handle_udp(comando)
            
# -----------------------------------------------------------------------------------
# Render
# -----------------------------------------------------------------------------------
    def render(self):
        self.screen.blit(self.game_image, (0, 0))
        self.screen.blit(self.s, (0,0))

        rect_texto = self.texto.get_rect(center=(self.RESOLUTION[0]//2, self.RESOLUTION[1]//2.2))
        self.screen.blit(self.texto, rect_texto)
        rect_titulo = self.titulo.get_rect(center=(self.RESOLUTION[0]//2, self.RESOLUTION[1]//3))
        self.screen.blit(self.titulo, rect_titulo)
        
        for i, item in enumerate(self.menu.buttons):
            btn = item["button"]
            lbl = item["label"]
            lbl_rect = item["label_rect"]

            btn.draw()

            if i == self.menu.selected_index:
                pygame.draw.rect(self.screen, (255, 215, 0), btn.rect, 4)

            lbl_rect.center = btn.rect.center
            self.screen.blit(lbl, lbl_rect)

        pygame.display.flip()


