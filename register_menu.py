import pygame, pygame_gui
from src.window import Window
import re

pygame.init()

class MenuRegistro(Window):
    def __init__(self):
        super().__init__()
        
        # Configurar título de la ventana
        pygame.display.set_caption("Registro - Grupo Cajeta")

        from src import Button

        self.clock = pygame.time.Clock()
        self.manager = pygame_gui.UIManager(self.RESOLUTION)
        self.running = True
        self.s = pygame.Surface(self.RESOLUTION) ##Fondo negro para el label
        self.s.set_alpha(110) ##Transparencia del fondo

        # Paleta de colores dorado/café (misma que en login)
        self.DORADO = (206, 143, 31)      # Color dorado original
        self.DORADO_OSCURO = (160, 110, 20)  # Dorado más oscuro
        self.CAFE = (101, 67, 33)         # Color café madera
        self.CAFE_CLARO = (120, 80, 40)   # Café más claro
        self.BEIGE = (222, 184, 135)      # Beige para fondos
        self.BLANCO = (255, 255, 255)     # Blanco puro
        self.GRIS_SUAVE = (80, 80, 80)    # Gris suave para placeholders

        # Estados de los campos de entrada
        self.username_activo = False
        self.email_activo = False
        self.password_activo = False
        
        # Texto de los campos
        self.username_text = ""
        self.email_text = ""
        self.password_text = ""

        ##-- Rectángulos para los campos de entrada (sin pygame_gui)
        username_y = self.RESOLUTION[1] / 2.5
        self.username_rect = pygame.Rect(self.RESOLUTION[0]/2 - 200, username_y + 50, 400, 50)
       
        email_y = username_y + 80
        self.email_rect = pygame.Rect(self.RESOLUTION[0]/2 - 200, email_y + 60, 400, 50)
        
        password_y = email_y + 80
        self.password_rect = pygame.Rect(self.RESOLUTION[0]/2 - 200, password_y + 70, 400, 50)

        ##-- Boton de aceptar
        button_y = password_y + 200
        self.accept_button = Button.Button(self.RESOLUTION[0] / 2, button_y, self.menu_button, self.screen, 0.15)
        self.label_accept = self.font.render("Registrarse", 1, self.DORADO)
        self.accept_rect = self.label_accept.get_rect(center=(self.accept_button.rect.centerx, self.accept_button.rect.centery))

        ##-- Boton de volver
        self.back_buttonx = Button.Button(self.RESOLUTION[0]/12, self.RESOLUTION[1]/1.05, self.back_button, self.screen, 0.07)

    def dibujar_caja_entrada(self, rect, texto, activo, etiqueta, texto_placeholder="Escribe aquí..."):
        # Dibujar etiqueta
        etiqueta_surf = self.font.render(etiqueta, True, self.DORADO)
        self.screen.blit(etiqueta_surf, (rect.x, rect.y - 30))
        
        # Fondo del campo (café madera)
        pygame.draw.rect(self.screen, self.CAFE, rect, border_radius=8)
        
        # Borde (dorado cuando está activo, café claro cuando no)
        color_borde = self.DORADO if activo else self.CAFE_CLARO
        pygame.draw.rect(self.screen, color_borde, rect, 2, border_radius=8)
        
        # Texto
        texto_mostrar = texto if texto else texto_placeholder
        color_texto = self.BLANCO if texto else self.GRIS_SUAVE
        texto_surf = self.font.render(texto_mostrar, True, color_texto)
        
        # Recortar texto si es muy largo
        if texto_surf.get_width() > rect.width - 20:
            texto_surf = self.font.render(texto_mostrar, True, color_texto)
        
        self.screen.blit(texto_surf, (rect.x + 10, rect.y + (rect.height - texto_surf.get_height()) // 2))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.next_window = None

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Verificar clic en campos de texto
                if self.username_rect.collidepoint(event.pos):
                    self.username_activo = True
                    self.email_activo = False
                    self.password_activo = False
                elif self.email_rect.collidepoint(event.pos):
                    self.email_activo = True
                    self.username_activo = False
                    self.password_activo = False
                elif self.password_rect.collidepoint(event.pos):
                    self.password_activo = True
                    self.username_activo = False
                    self.email_activo = False
                else:
                    self.username_activo = False
                    self.email_activo = False
                    self.password_activo = False

                if self.accept_button.rect.collidepoint(event.pos):
                    from start_menu import MainMenu

                    ## Verifica que los datos sean válidos antes de enviarlos a database.py
                    ## Si la verificación es correcta, cambia de ventana
                    if self.verificar_datos(self.username_text, self.email_text, self.password_text):
                        self.cambiar_ventana(MainMenu)

                if self.back_buttonx.rect.collidepoint(event.pos):
                    from main import Main
                    self.cambiar_ventana(Main)
                    
            # Manejar entrada de texto
            if event.type == pygame.KEYDOWN:
                if self.username_activo:
                    if event.key == pygame.K_BACKSPACE:
                        self.username_text = self.username_text[:-1]
                    else:
                        self.username_text += event.unicode
                
                elif self.email_activo:
                    if event.key == pygame.K_BACKSPACE:
                        self.email_text = self.email_text[:-1]
                    else:
                        self.email_text += event.unicode
                
                elif self.password_activo:
                    if event.key == pygame.K_BACKSPACE:
                        self.password_text = self.password_text[:-1]
                    else:
                        self.password_text += event.unicode
                
                # Manejar la tecla ENTER para registrarse
                if event.key == pygame.K_RETURN:
                    from start_menu import MainMenu
                    if self.verificar_datos(self.username_text, self.email_text, self.password_text):
                        self.cambiar_ventana(MainMenu)

            # PROCESAR EVENTOS DE PYGAME_GUI (IMPORTANTE)
            self.manager.process_events(event)


    def mostrar_error(self, mensaje_error):
        # Limpiar cualquier ventana de error anterior
        for window in self.manager.get_root_container().elements:
            if hasattr(window, 'window_title') and window.window_title == "Error":
                window.kill()
        
        # Crear nueva ventana de error
        error_window = pygame_gui.windows.UIMessageWindow(
            rect=pygame.Rect((self.RESOLUTION[0]/2 - 250, self.RESOLUTION[1]/2 - 75), (500, 150)),
            html_message=f"<font color='#FF3333'><b>Error de Registro</b></font><br>{mensaje_error}",
            manager=self.manager,
            window_title="Error",
            object_id="#error_window"
        )
        
        # Asegurarse de que la ventana esté enfocada
        error_window.focus()

    def validar_username(self, username):
        if len(username) < 3:
            return False, "El username debe tener al menos 3 caracteres"
        if len(username) > 20:
            return False, "El username no puede tener más de 20 caracteres"
        if not re.match("^[a-zA-Z0-9_]+$", username):
            return False, "El username solo puede contener letras, números y guión bajo"
        return True, ""

    def validar_email(self, email):
        if not email:
            return False, "Debe ingresar un correo"
        
        patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron_email, email):
            return False, "Formato de correo inválido"
        
        return True, ""

    def validar_contraseña(self, password):

        # - Mínimo 8 caracteres
        # - Al menos una letra mayúscula
        # - Al menos una letra minúscula
        # - Al menos un número
        # - Al menos un carácter especial

        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres"
        
        if len(password) > 128:
            return False, "La contraseña no puede tener más de 128 caracteres"
        
        if not re.search(r'[A-Z]', password):
            return False, "La contraseña debe contener al menos una mayúscula"
        
        if not re.search(r'[a-z]', password):
            return False, "La contraseña debe contener al menos una minúscula"
        
        if not re.search(r'\d', password):
            return False, "La contraseña debe contener al menos un número"
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/;`~]', password):
            return False, "La contraseña debe contener al menos un carácter especial (!@#$%...)"
        
        return True, ""


    def verificar_datos(self, username, email, password):
        from database import GrupoCajetaDB

        if not username or not email or not password:
            self.mostrar_error('Debe ingresar todos los datos')
            return False
        if '@' not in email or '.' not in email:
            self.mostrar_error('Ingrese un correo válido')
            return False
        if len(password) < 6:
            self.mostrar_error('La contraseña debe ser mayor a 6 carácteres')
            return False
        
        db = GrupoCajetaDB()
        try: 
            if not db.conectar():
                self.mostrar_error('Error de conexión a la base de datos')
                return False
            
            if db.verificar_usuario(username, email, password):
                Window.user = username
                return True
            else:
                self.mostrar_error('El username o email ya está registrado')
                return False
            
        except Exception as e:
            print("Error:", e)
            self.mostrar_error('Error al verificar datos')
            return False
        finally:
            db.cerrar()


    def render(self):
        self.screen.blit(self.menu_image, (0, 0))
        self.screen.blit(self.s, (0,0))
        
        # Dibujar campos de entrada personalizados
        self.dibujar_caja_entrada(
            self.username_rect, 
            self.username_text, 
            self.username_activo, 
            "Usuario:",
            "Ingrese su nombre de usuario"
        )
        
        self.dibujar_caja_entrada(
            self.email_rect, 
            self.email_text, 
            self.email_activo, 
            "Correo:",
            "ejemplo@correo.com"
        )
        
        # Para la contraseña, mostrar asteriscos
        password_display = "*" * len(self.password_text) if self.password_text else ""
        self.dibujar_caja_entrada(
            self.password_rect, 
            password_display, 
            self.password_activo, 
            "Contraseña:",
            "Mínimo 6 caracteres"
        )
        
        self.accept_button.draw()
        self.back_buttonx.draw()
        self.screen.blit(self.label_accept, self.accept_rect)
    
        # Interfaz de usuario (para ventanas de error)
        self.manager.draw_ui(self.screen)
        pygame.display.flip()


    def run(self):
        pygame.event.clear()
        pygame.time.wait(100)
        while self.running:
            refresh_rate = self.clock.tick(60)
            self.handle_events()
            self.render()
            self.manager.update(refresh_rate)  # Esto es importante para pygame_gui

        if self.next_window:
            nueva_ventana = self.next_window()
            nueva_ventana.run()