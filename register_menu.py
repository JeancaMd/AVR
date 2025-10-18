import pygame
import pygame_gui
from src.window import Window

pygame.init()


class MenuRegistro(Window):
    def __init__(self):
        super().__init__()
        from src import Button

        self.clock = pygame.time.Clock()
        self.manager = pygame_gui.UIManager(self.RESOLUTION)
        self.running = True
        self.s = pygame.Surface(self.RESOLUTION) ##Fondo negro para el label
        self.s.set_alpha(110) ##Transparencia del fondo

        ##-- Textbox y label de USERNAME
        self.username_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((self.RESOLUTION[0]/2.8 , self.RESOLUTION[1] / 1.85), (400, 30)), manager=self.manager, object_id="#username_text_entry")
        self.label_username = self.font.render("Username:", 1, (206,143,31))
        self.username_rect = self.label_username.get_rect(center=(self.username_input.rect.centerx-270, self.username_input.rect.centery))

        ##-- Textbox y label de EMAIL
        self.email_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((self.RESOLUTION[0] /2.8, self.RESOLUTION[1] / 1.6), (400, 30)), manager=self.manager, object_id="#email_text_entry")
        self.label_email = self.font.render("Correo:", 1, (206,143,31))
        self.email_rect = self.label_email.get_rect(center=(self.email_input.rect.centerx-250, self.email_input.rect.centery))
        
        ##-- Textbox y label de CONTRASEÑA
        self.password_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((self.RESOLUTION[0] /2.8, self.RESOLUTION[1] / 1.4), (400, 30)), manager=self.manager, object_id="#password_text_entry")
        self.label_password = self.font.render("Contraseña:", 1, (206,143,31))
        self.password_rect = self.label_password.get_rect(center=(self.password_input.rect.centerx-280, self.password_input.rect.centery))

        ##-- Boton de aceptar
        self.accept_button = Button.Button(self.RESOLUTION[0] / 2, self.RESOLUTION[1] / 1.18, self.menu_button, self.screen, 0.12)

    def handle_events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.next_window = None

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.accept_button.rect.collidepoint(event.pos):
                        from start_menu import MainMenu

                        ## Obtener valores ingresados en los textbox
                        ## Se mandan a database.py para verificarlos
                        self.username_text = self.username_input.get_text()
                        self.email_text = self.email_input.get_text()
                        self.password_text = self.password_input.get_text()

                        ## Verifica que los datos sean válidos antes de enviarlos a database.py
                        ## Si la verificación es correcta, cambia de ventana
                        if self.verificar_datos(self.username_text, self.email_text, self.password_text):
                            self.cambiar_ventana(MainMenu)

                self.manager.process_events(event)

    def mostrar_error(self, mensaje_error):
        pygame_gui.windows.UIMessageWindow(
            rect=pygame.Rect((150, 220), (500, 150)),
            html_message=f"<font color='#FF0000'><b>Error de Registro</b></font><br>{mensaje_error}",
            manager=self.manager,
            window_title="Error"
        )

    def verificar_datos(self, username, email, password):
        from database import GrupoCajetaDB

        ## Validaciones básicas para garantizar un formato válido
        ## antes de consultar a la base de datos
        if not username or not email or not password:
            self.mostrar_error('Debe ingresar todos los datos')
            return False
        if '@' not in email or '.' not in email:
            self.mostrar_error('Ingrese un correo valido')
            return False
        if len(password)<6:
            self.mostrar_error('La contraseña debe ser mayor a 6 carácteres')
            return False
        
        db = GrupoCajetaDB()
        try: 
            if not db.conectar():
                self.mostrar_error('Error de conexión a la base de datos')
                return False
            if db.verificar_usuario(username, email, password):
                return True
            
        except Exception as e:
            print("Error:", e)
            self.mostrar_error('Error al verificar datos')
            return False
        finally:
            db.cerrar()

    def render(self):
        self.screen.blit(self.menu_image, (0, 0))
        
        self.screen.blit(self.s, (0,0))
        self.screen.blit(self.label_username, self.username_rect)
        self.screen.blit(self.label_email, self.email_rect)
        self.screen.blit(self.label_password, self.password_rect)
        
        self.accept_button.draw()

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
    











