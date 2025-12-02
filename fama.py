import pygame
from database import GrupoCajetaDB
from src.window import Window
from src import Button
from src.menu_base import BaseMenu
from start_menu import MainMenu

pygame.init()

class SalonFama(Window):
    def __init__(self):
        super().__init__()
        self.db = GrupoCajetaDB()
        self.db.conectar()
        ### Cargar puntajes desde la base de datos
        self.tiempos = self.db.obtener_mejores_tiempos(limite=5)
        self.db.cerrar()
        self.menu = BaseMenu(self)
        self.center_x = self.RESOLUTION[0] // 2


        ### Fuente para los textos
        self.title_font = pygame.font.SysFont("High Tower Text", 60, bold=True)
        self.score_font = pygame.font.SysFont("High Tower Text", 40)
        self.info_font = pygame.font.SysFont("High Tower Text", 28)
        
        self.back_btn = Button.Button(
            self.RESOLUTION[0] / 1.1, 
            self.RESOLUTION[1] / 1.05, 
            self.menu_button, 
            self.screen, 
            0.07
        )
        self.label_back = self.font.render("Volver", 1, (206, 143, 31))
        self.back_rect = self.label_back.get_rect(center=(self.back_btn.rect.centerx, self.back_btn.rect.centery))

        self.menu.buttons.append({
            "name": "volver",
            "button": self.back_btn,
            "label": self.label_back,
            "label_rect": self.back_rect
        })

        ### Control UDP
        try:
            self.control = self.control
        except:
            from src.cliente import ControladorUDP
            self.control = ControladorUDP()   

        self.title = self.title_font.render("SALÓN DE LA FAMA", True, (255, 215, 0))
        self.title_rect = self.title.get_rect(center=(self.center_x, self.RESOLUTION[1] * 0.15))
    
    def confirmar(self, nombre):
        if nombre == "volver":
            self.cambiar_ventana(MainMenu)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                   self.cambiar_ventana(MainMenu)
                else:
                    self.menu.handle_keyboard(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.menu.handle_mouse(event.pos)

        comando = self.control.obtener_evento()
        if comando:
            self.menu.handle_udp(comando)


    def formatear_tiempo(self, segundos):
        ### Convierte segundos a formato MM:SS
        if not isinstance(segundos, (int, float)) or segundos < 0:
            raise ValueError("Los segundos deben ser un número positivo")
        
        minutos, segundos = divmod(int(segundos), 60)
        return f"{minutos:02d}:{segundos:02d}"
    
    def obtener_tiempos_formateados(self):
        ### Retorna la lista de tiempos formateados para mostrar
        tiempos_formateados = []
        if self.tiempos:
            for i, (nombre, tiempo) in enumerate(self.tiempos, start=1):
                tiempo_formateado = self.formatear_tiempo(tiempo)
                tiempos_formateados.append({
                    'posicion': i,
                    'nombre': nombre,
                    'tiempo': tiempo_formateado,
                    'tiempo_segundos': tiempo
                })
        return tiempos_formateados
    
    def hay_tiempos_registrados(self):
        ### Verifica si hay tiempos registrados en la base de datos
        return self.tiempos is not None and len(self.tiempos) > 0
    
    def cargar_datos_fama(self):
        ### Carga los datos del salón de la fama desde la base de datos
        ### Retorna: lista de tiempos o lista vacía si hay error
        try:
            self.db.conectar()
            tiempos = self.db.obtener_mejores_tiempos(limite=5)
            self.db.cerrar()
            return tiempos
        except Exception as e:
            print(f"Error cargando datos del salón de la fama: {e}")
            return []


    def render(self):
        ### Dibuja la pantalla del salón de la fama
        self.screen.blit(self.game_image, (0, 0))
        
        ### Título
        self.screen.blit(self.title, self.title_rect)
        
        ### Mostrar puntajes
        start_y = self.RESOLUTION[1] * 0.30
        line_height = 60
        
        if self.hay_tiempos_registrados():
            tiempos_formateados = self.obtener_tiempos_formateados()
            for item in tiempos_formateados:
                texto = f"{item['posicion']}. {item['nombre']} — {item['tiempo']}"
                render = self.score_font.render(texto, True, (255, 255, 255))
                rect = render.get_rect(center=(self.center_x, start_y + (item['posicion'] - 1) * line_height))
                self.screen.blit(render, rect)
        else:
            mensaje = self.info_font.render("Aún no hay tiempos registrados.", True, (200, 200, 200))
            rect = mensaje.get_rect(center=(self.center_x, self.RESOLUTION[1] * 0.5))
            self.screen.blit(mensaje, rect)

        for i, item in enumerate(self.menu.buttons):
            button = item["button"]
            label = item["label"]
            label_rect = item["label_rect"]

            button.draw()

        ### Borde dorado del boton
        if i == self.menu.selected_index:
            pygame.draw.rect(self.screen, (255, 215, 0), button.rect, 5)

        ### Dibujar texto
        label_rect.center = button.rect.center
        self.screen.blit(label, label_rect)
        
        
        pygame.display.flip()