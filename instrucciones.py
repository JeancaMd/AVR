import pygame
from src.window import Window
from src.menu_base import BaseMenu


class Instrucciones(Window):
    def __init__(self):
        super().__init__()
        self.menu = BaseMenu(self)

        ### Configurar posiciones
        center_x = self.RESOLUTION[0] / 2
        start_y = self.RESOLUTION[1] / 1.5
        spacing = 120

        left_x = center_x - 150
        right_x = center_x + 150

        ### Agregar botones con BaseMenu
        self.menu.añadir_boton("avatars", left_x, start_y, "Avatars")
        self.menu.añadir_boton("rooks", right_x, start_y, "Rooks")
        self.menu.añadir_boton("juego", left_x, start_y + spacing, "Juego")
        self.menu.añadir_boton("volver", right_x, start_y + spacing, "Volver")

        ### Título
        self.title_text = self.font.render("INSTRUCCIONES", True, (206, 143, 31))
        self.title_rect = self.title_text.get_rect(midtop=(self.RESOLUTION[0] / 2, 50))

        ### Control UDP
        try:
            self.control = self.control
        except:
            from src.cliente import ControladorUDP
            self.control = ControladorUDP("192.168.0.107")


    def confirmar(self, nombre):
        if nombre == "avatars":
            from instrucciones_avatars import AvatarsInstrucciones
            self.cambiar_ventana(AvatarsInstrucciones)    

        elif nombre == "rooks":
            from instrucciones_rooks import RooksInstrucciones
            self.cambiar_ventana(RooksInstrucciones)    
            
        elif nombre == "juego":
            from instrucciones_juego import JuegoInstrucciones
            self.cambiar_ventana(JuegoInstrucciones)    

        elif nombre == "volver":
            from start_menu import MainMenu
            self.cambiar_ventana(MainMenu)


    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from start_menu import MainMenu
                    self.cambiar_ventana(MainMenu)
                else:
                    self.menu.handle_keyboard(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.menu.handle_mouse(event.pos)

        # Leer del pico (UDP)
        comando = self.control.obtener_evento()
        if comando:
            self.menu.handle_udp(comando)


    def render(self):
        self.screen.blit(self.menu_image, (0, 0))
        self.screen.blit(self.title_text, self.title_rect)
                
        ### Botones usando BaseMenu
        for i, item in enumerate(self.menu.buttons):
            button = item["button"]
            label = item["label"]
            label_rect = item["label_rect"]

            button.draw()

            ### Borde dorado
            if i == self.menu.selected_index:
                pygame.draw.rect(self.screen, (255, 215, 0), button.rect, 4)

            label_rect.center = button.rect.center
            self.screen.blit(label, label_rect)
        
        pygame.display.flip()


