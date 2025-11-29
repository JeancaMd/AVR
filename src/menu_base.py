import pygame
from src import Button

class BaseMenu:
    def __init__(self, window):
        self.window = window
        self.screen = window.screen
        self.font = window.font
        self.menu_image = window.menu_image
        self.BUTTON_X = window.BUTTON_X
        self.RESOLUTION = window.RESOLUTION
        self.buttons = []
        self.selected_index = 0

    def añadir_boton(self, name, x, y, text=None, label=None):
        btn = Button.Button(x, y, self.window.menu_button, self.screen, self.BUTTON_X)

        if label is None:
            label = self.font.render(text, True, (206, 143, 31))

        label_rect = label.get_rect(center=btn.rect.center)

        self.buttons.append({
            "name": name,
            "button": btn,
            "label": label,
            "label_rect": label_rect
        })

    def mover_arriba(self):
        self.selected_index = (self.selected_index - 1) % len(self.buttons)

    def mover_abajo(self):
        self.selected_index = (self.selected_index + 1) % len(self.buttons)

    def confirmar(self, nombre):
        if hasattr(self.window, 'confirmar'):
            self.window.confirmar(nombre)


    ### Controlar acciones del control
    def handle_udp(self, comando):
        if comando == "Y+":
            self.mover_arriba()
        elif comando == "Y-":
            self.mover_abajo()
        elif comando in ("O", "X", "JOYSTICK_PRESIONADO"):
            nombre = self.buttons[self.selected_index]["name"]
            self.confirmar(nombre)

    ### Controlar acciones del teclado
    def handle_keyboard(self, key):
        if key == pygame.K_UP:
            self.mover_arriba()
        elif key == pygame.K_DOWN:
            self.mover_abajo()
        elif key == pygame.K_RETURN:
            nombre = self.buttons[self.selected_index]["name"]
            self.confirmar(nombre)

    ### Controlar acciones del mouse
    def handle_mouse(self, pos):
        for i, item in enumerate(self.buttons):
            if item["button"].rect.collidepoint(pos):
                self.selected_index = i
                self.confirmar(item["name"])

    ### Controlar acciones generales
    def handle_events(self, control_udp):
        import pygame
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.window.running = False

            elif event.type == pygame.KEYDOWN:
                self.handle_keyboard(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse(event.pos)

        comando = control_udp.obtener_evento()
        if comando:
            self.handle_udp(comando)


    def render(self):
        self.screen.blit(self.menu_image, (0, 0))

        for i, item in enumerate(self.buttons):
            btn = item["button"]
            lbl = item["label"]
            lbl_rect = item["label_rect"]

            btn.draw()

            ### Borde dorado en botones
            if i == self.selected_index:
                pygame.draw.rect(self.screen, (255, 215, 0), btn.rect, 4)

            lbl_rect.center = btn.rect.center
            self.screen.blit(lbl, lbl_rect)

        pygame.display.flip()
