import pygame, pygame_gui
from src.window import Window
from src import Button


pygame.init()

class LoginMenu(Window):
    def __init__(self):
        super().__init__()
        pygame.display.set_caption("Menú de inicio de sesión")

        self.clock = pygame.time.Clock()
        self.manager = pygame_gui.UIManager(self.RESOLUTION)
        self.running = True
        self.s = pygame.Surface(self.RESOLUTION)
        self.s.set_alpha(110)

        ### Paleta de colores dorado/café
        self.DORADO = (206, 143, 31)      # Color dorado original
        self.DORADO_OSCURO = (160, 110, 20)  # Dorado más oscuro
        self.CAFE = (101, 67, 33)         # Color café madera
        self.CAFE_CLARO = (120, 80, 40)   # Café más claro
        self.BEIGE = (222, 184, 135)      # Beige para fondos
        self.BLANCO = (255, 255, 255)     # Blanco puro
        self.GRIS_SUAVE = (150, 150, 150)    # Gris para placeholders

        ### Estados de los campos de entrada
        self.username_activo = False
        self.password_activo = False
        
        ### Texto de los campos
        self.username_text = ""
        self.password_text = ""

        ### Variables para controlar el borrado
        self.backspace_pressed = False
        self.backspace_initial_delay = 500  ### Milisegundos antes del borrado continuo
        self.backspace_repeat_delay = 50    ### Milisegundos entre borrados continuos
        self.backspace_timer = 0

        ### Rectángulos para los campos de entrada
        username_y = self.RESOLUTION[1] / 2.2
        self.username_rect = pygame.Rect(self.RESOLUTION[0]/2 - 200, username_y + 70, 400, 50)
       
        password_y = username_y + 80
        self.password_rect = pygame.Rect(self.RESOLUTION[0]/2 - 200, password_y + 80, 400, 50)

        self.mostrar_password = False

        self.password_toggle_rect = pygame.Rect(
            self.password_rect.right + 30,
            self.password_rect.y,
            110,
            self.password_rect.height
            )

        ### Boton de aceptar
        button_y = password_y + 210
        self.accept_button = Button.Button(self.RESOLUTION[0] / 2, button_y, self.menu_button, self.screen, 0.15)
        self.label_accept = self.font.render("Iniciar Sesión", 1, self.DORADO)
        self.accept_rect = self.label_accept.get_rect(center=(self.accept_button.rect.centerx, self.accept_button.rect.centery))

        ### Boton de volver
        self.back_buttonx = Button.Button(self.RESOLUTION[0]/12, self.RESOLUTION[1]/1.05, self.back_button, self.screen, 0.07)

    def dibujar_caja_entrada(self, rect, texto, activo, etiqueta, texto_placeholder="Escribe aquí..."):
        ### Dibujar etiqueta
        etiqueta_surf = self.font.render(etiqueta, True, self.DORADO)
        self.screen.blit(etiqueta_surf, (rect.x, rect.y - 30))
        
        ### Fondo del campo
        pygame.draw.rect(self.screen, self.CAFE, rect, border_radius=8)
        
        ### Borde
        color_borde = self.DORADO if activo else self.CAFE_CLARO
        pygame.draw.rect(self.screen, color_borde, rect, 2, border_radius=8)
        
        ### Texto
        texto_mostrar = texto if texto else texto_placeholder
        color_texto = self.BLANCO if texto else self.GRIS_SUAVE
        texto_surf = self.font.render(texto_mostrar, True, color_texto)
        
        ### Recortar texto si es muy largo
        if texto_surf.get_width() > rect.width - 20:
            texto_surf = self.font.render(texto_mostrar, True, color_texto)
        
        self.screen.blit(texto_surf, (rect.x + 10, rect.y + (rect.height - texto_surf.get_height()) // 2))

    def dibujar_boton_password(self):
        ### Dibujar botón de mostrar/ocultar
        color_fondo = self.DORADO_OSCURO if self.password_toggle_rect.collidepoint(pygame.mouse.get_pos()) else self.CAFE_CLARO
        pygame.draw.rect(self.screen, color_fondo, self.password_toggle_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.DORADO, self.password_toggle_rect, 2, border_radius=8)
        
        ### Texto del botón
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
                ### Verificar clic en campos de texto
                if self.password_toggle_rect.collidepoint(event.pos):
                    self.mostrar_password = not self.mostrar_password
                if self.username_rect.collidepoint(event.pos):
                    self.username_activo = True
                    self.password_activo = False
                elif self.password_rect.collidepoint(event.pos):
                    self.password_activo = True
                    self.username_activo = False
                else:
                    self.username_activo = False
                    self.password_activo = False

                if self.accept_button.rect.collidepoint(event.pos):
                    from start_menu import MainMenu

                    ## Verifica que los datos sean válidos antes de enviarlos a database.py
                    ## Si la verificación es correcta, cambia de ventana
                    if self.verificar_datos(self.username_text, self.password_text):
                        self.actualizar_tema(self.tema)
                        self.cambiar_ventana(MainMenu)

                if self.back_buttonx.rect.collidepoint(event.pos):
                    from main import Main
                    self.cambiar_ventana(Main)
                    
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    from start_menu import MainMenu
                    if self.verificar_datos(self.username_text, self.password_text):
                        self.actualizar_tema(self.tema)
                        self.cambiar_ventana(MainMenu)
                        
                if self.username_activo:
                    if event.key == pygame.K_BACKSPACE:
                        self.username_text = self.username_text[:-1]
                        self.backspace_pressed = True
                        self.backspace_timer = pygame.time.get_ticks() + self.backspace_initial_delay
                    else:
                        self.username_text += event.unicode
                
                elif self.password_activo:
                    if event.key == pygame.K_BACKSPACE:
                        self.password_text = self.password_text[:-1]
                        self.backspace_pressed = True
                        self.backspace_timer = pygame.time.get_ticks() + self.backspace_initial_delay
                    else:
                        self.password_text += event.unicode
            
            ### Detectar cuando se suelta la tecla de borrado
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    self.backspace_pressed = False

            self.manager.process_events(event)
        
        ### Lógica para borrado continuo
        current_time = pygame.time.get_ticks()
        if self.backspace_pressed and current_time >= self.backspace_timer:
            if self.username_activo and self.username_text:
                self.username_text = self.username_text[:-1]
                self.backspace_timer = current_time + self.backspace_repeat_delay
            elif self.password_activo and self.password_text:
                self.password_text = self.password_text[:-1]
                self.backspace_timer = current_time + self.backspace_repeat_delay

    def mostrar_error(self, mensaje_error):
        for window in self.manager.get_root_container().elements:
            if hasattr(window, 'window_title') and window.window_title == "Error":
                window.kill()
        
        ### Crear nueva ventana de error
        error_window = pygame_gui.windows.UIMessageWindow(
            rect=pygame.Rect((self.RESOLUTION[0]/2 - 250, self.RESOLUTION[1]/2 - 75), (500, 150)),
            html_message=f"<font color='#FF3333'><b>Error de Inicio de Sesión</b></font><br>{mensaje_error}",
            manager=self.manager,
            window_title="Error",
            object_id="#error_window"
        )
        error_window.focus()

    def verificar_datos(self, username, password):
        from database import GrupoCajetaDB
        
        if not username or not password:
            self.mostrar_error('Debe ingresar todos los datos')
            return False
        
        db = GrupoCajetaDB()
        try: 
            if not db.conectar():
                self.mostrar_error('Error de conexión a la base de datos')
                return False
            
            ### Cargar y aplicar el tema guardado
            tema_usuario = db.verificar_usuario_existente(username, password)
            if tema_usuario is not None:
                Window.tema = tema_usuario
                Window.user = username
                return True
            else:
                self.mostrar_error('Usuario o contraseña incorrectos')
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
        
        ### Dibujar campos de entrada personalizados
        self.dibujar_caja_entrada(
            self.username_rect, 
            self.username_text, 
            self.username_activo, 
            "Usuario:",
            "Ingrese su nombre de usuario"
        )
        
        ### Para la contraseña, mostrar asteriscos
        password_display = self.password_text if self.mostrar_password else "*" * len(self.password_text)
        self.dibujar_caja_entrada(
            self.password_rect, 
            password_display, 
            self.password_activo, 
            "Contraseña:",
            "Ingrese su contraseña"
        )

        self.dibujar_boton_password()
        
        ### Botones
        self.accept_button.draw()
        self.back_buttonx.draw()
        self.screen.blit(self.label_accept, self.accept_rect)

        ### Interfaz de usuario (para ventanas de error)
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