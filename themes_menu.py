import pygame
from src.window import Window
from database import GrupoCajetaDB
from src.menu_base import BaseMenu

class ThemesMenu(Window):
    def __init__(self):
        super().__init__()
        self.menu = BaseMenu(self)

        ### Configurar posiciones
        center_x = self.RESOLUTION[0] / 2
        start_y = self.RESOLUTION[1] / 1.5
        spacing = 120
        
        left_x  = center_x - 150
        right_x = center_x + 150

        self.db = GrupoCajetaDB()
        self.db.conectar()

        ### Agregar botones con BaseMenu
        self.menu.añadir_boton("tema0", left_x, start_y, "Tema Default")
        self.menu.añadir_boton("tema1", right_x, start_y, "Tema Desértico")
        self.menu.añadir_boton("tema2", left_x, start_y + spacing, "Tema Navideño")
        self.menu.añadir_boton("volver", right_x, start_y + spacing, "Volver")

        self.title_text = self.font.render("Seleccionar Tema", True, (206, 143, 31))
        self.title_rect = self.title_text.get_rect(midtop=(self.RESOLUTION[0] / 2, 50))

        # Control UDP
        try:
            self.control = self.control
        except:
            from src.cliente import ControladorUDP
            self.control = ControladorUDP()
            

# -----------------------------------------------------------------------------------
#  Confirmar click en botones
# -----------------------------------------------------------------------------------
    def confirmar(self, nombre):
        if nombre == "tema0":
            self.actualizar_tema(0)
            self.db.actualizar_tema(self.user, self.tema)

        elif nombre == "tema1":
            self.actualizar_tema(1)
            self.db.actualizar_tema(self.user, self.tema)

        elif nombre == "tema2":
            self.actualizar_tema(2)
            self.db.actualizar_tema(self.user, self.tema)

        elif nombre == "volver":
            self.db.cerrar()
            from options_menu import OptionsMenu
            self.cambiar_ventana(OptionsMenu)


# -----------------------------------------------------------------------------------
# Handle events desde MenuBase
# -----------------------------------------------------------------------------------
    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
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
        self.screen.blit(self.menu_image, (0, 0))

        # Dibujar botones
        for i, item in enumerate(self.menu.buttons):
            button = item["button"]
            label = item["label"]
            label_rect = item["label_rect"]

            button.draw()

            # Highlight del seleccionado actualmente
            if i == self.menu.selected_index:
                pygame.draw.rect(self.screen, (255, 215, 0), button.rect, 4)
            
            # Dibujar texto centrado
            label_rect.center = button.rect.center
            self.screen.blit(label, label_rect)

        self.screen.blit(self.title_text, self.title_rect)

        pygame.display.flip()


