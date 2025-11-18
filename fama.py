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
        self.tiempos = self.db.obtener_mejores_tiempos(limite=5)
        self.db.cerrar()
        
        # Centro horizontal
        self.center_x = self.RESOLUTION[0] // 2
        
        # Fuente para los textos
        self.title_font = pygame.font.SysFont("High Tower Text", 60, bold=True)
        self.score_font = pygame.font.SysFont("High Tower Text", 40)
        self.info_font = pygame.font.SysFont("High Tower Text", 28)
        
        # SOLUCIÓN: Botón más ancho para "Volver al menú principal"
        # Crear una versión más ancha del botón
        boton_ancho = pygame.transform.scale(
            self.menu_button, 
            (int(self.menu_button.get_width() * 1.5), self.menu_button.get_height())  # 40% más ancho
        )
        
        self.back_button = Button.Button(
            self.center_x,
            self.RESOLUTION[1] * 0.88,
            boton_ancho,  # Usar el botón más ancho
            self.screen,
            self.BUTTON_X
        )
        
        # SOLUCIÓN: Fuente más pequeña para el texto largo
        self.back_font = pygame.font.SysFont("High Tower Text", 28)  # Fuente más pequeña
        self.back_label = self.back_font.render("Volver al menú principal", True, (206, 143, 31))
        self.back_rect = self.back_label.get_rect(center=self.back_button.rect.center)
        
        self.title = self.title_font.render("SALÓN DE LA FAMA", True, (255, 215, 0))
        self.title_rect = self.title.get_rect(center=(self.center_x, self.RESOLUTION[1] * 0.15))
    
    def formatear_tiempo(self, segundos):
        """
        Convierte segundos a formato MM:SS
        """
        if not isinstance(segundos, (int, float)) or segundos < 0:
            raise ValueError("Los segundos deben ser un número positivo")
        
        minutos, segundos = divmod(int(segundos), 60)
        return f"{minutos:02d}:{segundos:02d}"
    
    def obtener_tiempos_formateados(self):
        """
        Retorna la lista de tiempos formateados para mostrar
        """
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
        """
        Verifica si hay tiempos registrados en la base de datos
        """
        return self.tiempos is not None and len(self.tiempos) > 0
    
    def cargar_datos_fama(self):
        """
        Carga los datos del salón de la fama desde la base de datos
        Retorna: lista de tiempos o lista vacía si hay error
        """
        try:
            self.db.conectar()
            tiempos = self.db.obtener_mejores_tiempos(limite=5)
            self.db.cerrar()
            return tiempos
        except Exception as e:
            print(f"Error cargando datos del salón de la fama: {e}")
            return []
    
    def handle_events(self):
        """Maneja los eventos de la pantalla."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.next_window = None
            
            # SOLUCIÓN: Detectar clic de manera consistente
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.back_button.rect.collidepoint(event.pos):
                    from start_menu import MainMenu
                    self.running = False
                    MainMenu().run()
    
    def render(self):
        """Dibuja la pantalla del salón de la fama."""
        self.screen.blit(self.menu_image, (0, 0))
        
        # Título
        self.screen.blit(self.title, self.title_rect)
        
        # Mostrar puntajes
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

        # SOLUCIÓN: Dibujar botón y detectar clic de manera consistente
        if self.back_button.draw():  # Esto detecta el hover y click
            from start_menu import MainMenu
            self.running = False
            MainMenu().run()
        
        self.screen.blit(self.back_label, self.back_rect)
        
        pygame.display.flip()