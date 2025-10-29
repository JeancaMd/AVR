import pygame

pygame.init()



class Window:
    ##-- Constantes
    RESOLUTION = (800,700)
    FONT_SIZE_X = int(RESOLUTION[0]/32) ##Factor para mantener la fuente dentro del área del botón
    BUTTON_X = RESOLUTION[0]/5333 ##Factor para mantener las proporciones del botón sin importar la resolución

    ##-- Config
    tema = None
    user = None

    THEMES = {
        0: "assets/images/backgrounds/theme_0.png",
        1: "assets/images/backgrounds/theme_1.png",
        2: "assets/images/backgrounds/theme_2.png",
    }

    ##-- Recursos
    icon = pygame.image.load("assets/images/ui/logo.png")
    menu_background = pygame.image.load(THEMES[0])
    menu_image = pygame.transform.scale(menu_background, RESOLUTION)
    menu_button = pygame.image.load("assets/images/ui/menu_button.png")
    font = pygame.font.SysFont("High tower text", FONT_SIZE_X)
    
    def __init__(self):
        self.screen = pygame.display.set_mode((self.__class__.RESOLUTION))
        pygame.display.set_caption("Avatars VS Rooks")  
        pygame.display.set_icon(self.__class__.icon)
        self.running = True
        self.next_window = None 

    def cambiar_ventana(self, ventana_clase):
        self.next_window = ventana_clase
        self.running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
    def actualizar_tema(self, nuevo_tema=None):
        if nuevo_tema is not None:
            Window.tema = nuevo_tema

        ruta_tema = Window.THEMES.get(Window.tema, Window.THEMES[0])
        Window.menu_background = pygame.image.load(ruta_tema)
        Window.menu_image = pygame.transform.scale(Window.menu_background, Window.RESOLUTION)

    def render(self):
        self.screen.blit(self.menu_image, (0, 0))
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.render()
        
        if self.next_window:
            nueva_ventana = self.next_window()
            nueva_ventana.run()


