import pygame, pygame_gui
from src.window import Window
from src import Button
import re

pygame.init()

class MenuRegistro(Window):
    def __init__(self):
        super().__init__()
        pygame.display.set_caption("Menú de registro")


        self.clock = pygame.time.Clock()
        self.manager = pygame_gui.UIManager(self.RESOLUTION)
        self.running = True
        self.s = pygame.Surface(self.RESOLUTION) ##Fondo negro para el label
        self.s.set_alpha(110) ##Transparencia del fondo

        self.DORADO = (206, 143, 31)      # Color dorado original
        self.DORADO_OSCURO = (160, 110, 20)  # Dorado más oscuro
        self.CAFE = (101, 67, 33)         # Color café madera
        self.CAFE_CLARO = (120, 80, 40)   # Café más claro
        self.BEIGE = (222, 184, 135)      # Beige para fondos
        self.BLANCO = (255, 255, 255)     # Blanco puro
        self.GRIS_SUAVE = (150, 150, 150)    # Gris suave para placeholders

        # Estados de los campos de entrada
        self.username_activo = False
        self.email_activo = False
        self.password_activo = False
        
        # Texto de los campos
        self.username_text = ""
        self.email_text = ""
        self.password_text = ""

        self.mostrar_password = False

        # Variables para controlar el borrado continuo
        self.backspace_pressed = False
        self.backspace_initial_delay = 500  # Milisegundos antes del borrado continuo
        self.backspace_repeat_delay = 50    # Milisegundos entre borrados continuos
        self.backspace_timer = 0

        ## Rectángulos para los campos de entrada
        username_y = self.RESOLUTION[1] / 2.5
        self.username_rect = pygame.Rect(self.RESOLUTION[0]/2 - 200, username_y + 50, 400, 50)
       
        email_y = username_y + 80
        self.email_rect = pygame.Rect(self.RESOLUTION[0]/2 - 200, email_y + 60, 400, 50)
        
        password_y = email_y + 80
        self.password_rect = pygame.Rect(self.RESOLUTION[0]/2 - 200, password_y + 70, 400, 50)

        self.password_toggle_rect = pygame.Rect(
            self.password_rect.right + 30,
            self.password_rect.y,
            110,
            self.password_rect.height
        )

        ## Boton de aceptar
        button_y = password_y + 200
        self.accept_button = Button.Button(self.RESOLUTION[0] / 2, button_y, self.menu_button, self.screen, 0.15)
        self.label_accept = self.font.render("Registrarse", 1, self.DORADO)
        self.accept_rect = self.label_accept.get_rect(center=(self.accept_button.rect.centerx, self.accept_button.rect.centery))

        ## Boton de volver
        self.back_buttonx = Button.Button(self.RESOLUTION[0]/12, self.RESOLUTION[1]/1.05, self.back_button, self.screen, 0.07)

    def dibujar_caja_entrada(self, rect, texto, activo, etiqueta, texto_placeholder="Escribe aquí..."):
        # Dibujar etiqueta
        etiqueta_surf = self.font.render(etiqueta, True, self.DORADO)
        self.screen.blit(etiqueta_surf, (rect.x, rect.y - 30))
        
        # Fondo del campo
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

    def dibujar_boton_password(self):
        # Dibujar el botón de mostrar/ocultar contraseña
        pygame.draw.rect(self.screen, self.CAFE_CLARO, self.password_toggle_rect, border_radius=5)
        pygame.draw.rect(self.screen, self.DORADO, self.password_toggle_rect, 2, border_radius=5)
        
        # Texto del botón
        texto_boton = "Mostrar" if not self.mostrar_password else "Ocultar"
        texto_surf = self.font.render(texto_boton, True, self.BLANCO)
        texto_rect = texto_surf.get_rect(center=self.password_toggle_rect.center)
        self.screen.blit(texto_surf, texto_rect)

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
                # Verificar clic en el botón de mostrar/ocultar contraseña
                elif self.password_toggle_rect.collidepoint(event.pos):
                    self.mostrar_password = not self.mostrar_password
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
                        self.backspace_pressed = True
                        self.backspace_timer = pygame.time.get_ticks() + self.backspace_initial_delay
                    else:
                        self.username_text += event.unicode
                
                elif self.email_activo:
                    if event.key == pygame.K_BACKSPACE:
                        self.email_text = self.email_text[:-1]
                        self.backspace_pressed = True
                        self.backspace_timer = pygame.time.get_ticks() + self.backspace_initial_delay
                    else:
                        self.email_text += event.unicode
                
                elif self.password_activo:
                    if event.key == pygame.K_BACKSPACE:
                        self.password_text = self.password_text[:-1]
                        self.backspace_pressed = True
                        self.backspace_timer = pygame.time.get_ticks() + self.backspace_initial_delay
                    else:
                        self.password_text += event.unicode
                
                # Manejar la tecla ENTER para registrarse
                if event.key == pygame.K_RETURN:
                    from start_menu import MainMenu
                    if self.verificar_datos(self.username_text, self.email_text, self.password_text):
                        self.cambiar_ventana(MainMenu)
            
            # Detectar cuando se suelta la tecla de borrado
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    self.backspace_pressed = False

            self.manager.process_events(event)
        
        # Lógica para borrado continuo 
        current_time = pygame.time.get_ticks()
        if self.backspace_pressed and current_time >= self.backspace_timer:
            if self.username_activo and self.username_text:
                self.username_text = self.username_text[:-1]
                self.backspace_timer = current_time + self.backspace_repeat_delay
            elif self.email_activo and self.email_text:
                self.email_text = self.email_text[:-1]
                self.backspace_timer = current_time + self.backspace_repeat_delay
            elif self.password_activo and self.password_text:
                self.password_text = self.password_text[:-1]
                self.backspace_timer = current_time + self.backspace_repeat_delay

    def mostrar_error(self, mensaje_error):
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
            return False, "Formato de correo inválido. Ejemplo: usuario@dominio.com"
        
        # Validación adicional razonable
        local_part, domain = email.split('@')
        
        if len(domain) < 4:  # Dominios muy cortos como "b.c" (3 caracteres)
            return False, "El dominio del correo parece inválido"
        
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

        # Validar username
        valido, mensaje = self.validar_username(username)
        if not valido:
            self.mostrar_error(mensaje)
            return False

        # Validar email
        valido, mensaje = self.validar_email(email)
        if not valido:
            self.mostrar_error(mensaje)
            return False

        # Validar contraseña
        valido, mensaje = self.validar_contraseña(password)
        if not valido:
            self.mostrar_error(mensaje)
            return False

        # Si las tres validaciones son correctas, conecta con la base de datos
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
            "Correo electrónico:",
            "ejemplo@correo.com"
        )
        
        # Para la contraseña, mostrar asteriscos o texto según el estado
        if self.mostrar_password:
            password_display = self.password_text
        else:
            password_display = "*" * len(self.password_text) if self.password_text else ""
            
        self.dibujar_caja_entrada(
            self.password_rect, 
            password_display, 
            self.password_activo, 
            "Contraseña:",
            "Mínimo 6 caracteres"
        )
        
        # Dibujar el botón de mostrar/ocultar contraseña
        self.dibujar_boton_password()
        
        self.accept_button.draw()
        self.back_buttonx.draw()
        self.screen.blit(self.label_accept, self.accept_rect)
    
        # Interfaz de usuario 
        self.manager.draw_ui(self.screen)
        pygame.display.flip()


    def run(self):
        pygame.event.clear()
        pygame.time.wait(100)
        while self.running:
            refresh_rate = self.clock.tick(60)
            self.handle_events()
            self.render()
            self.manager.update(refresh_rate)

        if self.next_window:
            nueva_ventana = self.next_window()
            nueva_ventana.run()