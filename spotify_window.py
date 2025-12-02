import pygame
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from src.window import Window
from src import Button

class SpotifyWindow(Window):
    def __init__(self):
        super().__init__()
        
        print("🎵 Inicializando ventana de Spotify...")
        
        # Autenticación con Spotify
        try:
            print("🔑 Intentando autenticar con Spotify...")
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id="dd8746ef3a5e42efa74626031f699f28",
                client_secret="4262ef2a915e49619f1fd1395f12f9fd",
                redirect_uri="http://127.0.0.1:8888/callback",
                scope="user-modify-playback-state user-read-playback-state"
            ))
            self.spotify_connected = True
            print("✅ Spotify conectado exitosamente!")
            
            # Verificar dispositivos disponibles
            self.verificar_dispositivos()
            
        except Exception as e:
            print(f"❌ Error conectando a Spotify: {e}")
            self.spotify_connected = False

        # Colores
        self.FONDO_OSCURO = (18, 18, 18)
        self.VERDE_SPOTIFY = (30, 215, 96)
        self.GRIS_CLARO = (40, 40, 40)
        self.BLANCO = (255, 255, 255)
        self.GRIS = (170, 170, 170)
        self.VERDE_BRILLANTE = (60, 235, 116)
        self.GRIS_MÁS_OSCURO = (30, 30, 30)

        # Fuentes
        self.fuente_titulo = pygame.font.SysFont("Arial", 32, bold=True)
        self.fuente = pygame.font.SysFont("Arial", 24)
        self.fuente_pequeña = pygame.font.SysFont("Arial", 18)
        self.fuente_muy_pequeña = pygame.font.SysFont("Arial", 14)
        self.fuente_iconos = pygame.font.SysFont("DejaVu Sans", 16)

        # Variables de estado
        self.input_cancion = ""
        self.input_artista = ""
        self.activo_cancion = False
        self.activo_artista = False
        self.repetir = False
        self.mensaje = ""
        self.tiempo_mensaje = 0
        self.lista_reproduccion = []
        self.indice_reproduccion_actual = -1
        self.scroll_offset = 0
        self.scroll_velocidad = 20

        # Borrado rápido
        self.tecla_backspace_presionada = False
        self.tiempo_ultimo_backspace = 0
        self.intervalo_backspace_inicial = 300
        self.intervalo_backspace_rapido = 10

        # Inicializar áreas de la interfaz
        self.recalcular_interfaz(self.RESOLUTION[0], self.RESOLUTION[1])

        # Botón de volver
        self.back_buttonx = Button.Button(self.RESOLUTION[0]/12, self.RESOLUTION[1]/1.05, self.back_button, self.screen, 0.07)

        self.ultima_actualizacion = 0
        self.intervalo_actualizacion = 1000  # Actualizar cada segundo

        # Caches de rendimiento
        self.cache_cancion_actual = None
        self.cache_timestamp = 0
        self.cache_interval = 3000  # ms entre lecturas Spotify

        self.ui_estatica = None  # Render de UI que no cambia

        # Cache del render de la lista
        self.cache_lista_surface = None
        self.cache_lista_scroll = None
        self.cache_lista_len = 0


    def verificar_dispositivos(self):
        """Verifica los dispositivos disponibles"""
        try:
            print("📱 Verificando dispositivos de Spotify...")
            dispositivos = self.sp.devices()
            print(f"Dispositivos encontrados: {len(dispositivos['devices'])}")
            
            for i, dispositivo in enumerate(dispositivos['devices']):
                estado = "ACTIVO" if dispositivo['is_active'] else "inactivo"
                print(f"  {i+1}. {dispositivo['name']} - {estado} (Vol: {dispositivo['volume_percent']}%)")
                
            if not dispositivos['devices']:
                print("⚠️  No hay dispositivos de Spotify disponibles")
                print("💡 Abre la app de Spotify en tu teléfono o computadora")
                
        except Exception as e:
            print(f"❌ Error al verificar dispositivos: {e}")

    def recalcular_interfaz(self, ancho, alto):
        margen = ancho * 0.05
        ancho_caja = ancho * 0.45
        alto_caja = alto * 0.07
        separacion_vertical = alto * 0.05
        y_base = alto * 0.15

        self.caja_cancion = pygame.Rect(ancho * 0.25, y_base, ancho_caja, alto_caja)
        self.caja_artista = pygame.Rect(ancho * 0.25, y_base + alto_caja + separacion_vertical, ancho_caja, alto_caja)

        y_botones = y_base + alto_caja * 2 + separacion_vertical * 1.5

        self.boton_reproducir = pygame.Rect(ancho * 0.1, y_botones, ancho * 0.13, alto * 0.06)
        self.boton_pausar = pygame.Rect(ancho * 0.25, y_botones, ancho * 0.13, alto * 0.06)
        self.boton_reanudar = pygame.Rect(ancho * 0.40, y_botones, ancho * 0.13, alto * 0.06)
        self.boton_repetir = pygame.Rect(ancho * 0.55, y_botones, ancho * 0.13, alto * 0.06)

        self.boton_anadir = pygame.Rect(ancho * 0.72, y_base + alto_caja - 54, ancho * 0.15, alto * 0.06)
        self.boton_limpiar = pygame.Rect(ancho * 0.72, y_base + alto_caja + 30.5, ancho * 0.15, alto * 0.06)
        self.boton_reproducir_lista = pygame.Rect(ancho * 0.72, y_base + alto_caja + 115, ancho * 0.15, alto * 0.06)

        # Área para la canción actual (arriba de la lista)
        nuevo_ancho = (ancho - 2 * margen) * 0.45
        x = (ancho - nuevo_ancho) / 2
        self.area_actual = pygame.Rect(x, alto * 0.48, nuevo_ancho, alto * 0.06)

        
        # Área de la lista de reproducción (más abajo)
        self.area_lista = pygame.Rect(margen, alto * 0.60, ancho - 2 * margen, alto * 0.31)

    def obtener_reproduccion_actual(self):
        """Consulta la canción actual usando cache para evitar ralentizar el juego."""
        if not self.spotify_connected:
            return self.cache_cancion_actual

        t = pygame.time.get_ticks()

        # Si el cache está fresco, no consultar Spotify
        if t - self.cache_timestamp < self.cache_interval:
            return self.cache_cancion_actual

        try:
            estado_actual = self.sp.current_playback()
            self.cache_timestamp = t

            if estado_actual and estado_actual["item"]:
                track = estado_actual["item"]

                self.cache_cancion_actual = {
                    "nombre": track["name"],
                    "artista": track["artists"][0]["name"],
                    "album": track["album"]["name"],
                    "duracion_ms": track["duration_ms"],
                    "progreso_ms": estado_actual["progress_ms"],
                    "en_reproduccion": estado_actual["is_playing"]
                }
            else:
                self.cache_cancion_actual = None

        except Exception as e:
            print(f"❌ Error al consultar reproducción: {e}")

        return self.cache_cancion_actual

    
    def dibujar_reproduccion_actual(self):
        """Dibuja solo el nombre y artista usando cache para máximo rendimiento."""
        cancion_actual = self.obtener_reproduccion_actual()

        pygame.draw.rect(self.screen, self.GRIS_CLARO, self.area_actual, border_radius=8)
        pygame.draw.rect(self.screen, self.VERDE_SPOTIFY, self.area_actual, 2, border_radius=8)

        if cancion_actual:
            texto = f"{cancion_actual['nombre']} - {cancion_actual['artista']}"
        else:
            texto = "No se está reproduciendo nada"

        if len(texto) > 50:
            texto = texto[:47] + "..."

        texto_surf = self.fuente_pequeña.render(texto, True, self.BLANCO)
        self.screen.blit(texto_surf, (self.area_actual.x + 20, self.area_actual.y + 15))



    def dibujar_texto(self, texto, fuente, color, x, y, sombra=False):
        if sombra:
            superficie_sombra = fuente.render(texto, True, (0, 0, 0))
            self.screen.blit(superficie_sombra, (x+2, y+2))
        superficie_texto = fuente.render(texto, True, color)
        self.screen.blit(superficie_texto, (x, y))
        return superficie_texto.get_rect(topleft=(x, y))

    def dibujar_boton(self, rect, texto, color, hover_color, texto_color=None):
        if texto_color is None:
            texto_color = self.BLANCO  # Usar el BLANCO definido en la clase
        pos_mouse = pygame.mouse.get_pos()
        es_hover = rect.collidepoint(pos_mouse)
        
        color_boton = hover_color if es_hover else color
        pygame.draw.rect(self.screen, color_boton, rect, border_radius=8)
        pygame.draw.rect(self.screen, self.BLANCO, rect, 2, border_radius=8)
        
        texto_surf = self.fuente_pequeña.render(texto, True, texto_color)
        texto_rect = texto_surf.get_rect(center=rect.center)
        self.screen.blit(texto_surf, texto_rect)
        
        return es_hover
    
    def formatear_tiempo(self, milisegundos):
        """Convierte milisegundos a formato minutos:segundos"""
        segundos = int(milisegundos / 1000)
        minutos = segundos // 60
        segundos = segundos % 60
        return f"{minutos}:{segundos:02d}"

    def dibujar_caja_entrada(self, rect, texto, activo, etiqueta, texto_placeholder="Escribe aquí..."):
        self.dibujar_texto(etiqueta, self.fuente_pequeña, self.GRIS, rect.x, rect.y - 25)
        
        # Fondo del campo
        pygame.draw.rect(self.screen, self.GRIS_CLARO, rect, border_radius=8)
        
        # Borde
        color_borde = self.VERDE_SPOTIFY if activo else self.GRIS
        pygame.draw.rect(self.screen, color_borde, rect, 2, border_radius=8)
        
        # Texto
        texto_surf = self.fuente.render(texto if texto else texto_placeholder, True, self.BLANCO if texto else self.GRIS)
        self.screen.blit(texto_surf, (rect.x + 10, rect.y + 8))

    def buscar_cancion(self, nombre, artista=""):
        if not self.spotify_connected:
            print("❌ Spotify no está conectado")
            return None, "Spotify no conectado"
            
        try:
            print(f"🔍 Buscando canción: '{nombre}' artista: '{artista}'")
            fila_de_reproduccion = f"track:{nombre}"
            if artista:
                fila_de_reproduccion += f" artist:{artista}"
            
            resultados = self.sp.search(q=fila_de_reproduccion, type="track", limit=1)
            
            if len(resultados["tracks"]["items"]) == 0:
                print("❌ Canción no encontrada en Spotify")
                return None, "Canción no encontrada"
            
            track = resultados["tracks"]["items"][0]
            print(f"✅ Encontrada: '{track['name']}' - '{track['artists'][0]['name']}'")
            return {
                "nombre": track["name"],
                "artista": track["artists"][0]["name"],
                "uri": track["uri"],
                "duracion": track["duration_ms"],
                "album": track["album"]["name"]
            }, "Éxito"
        
        except Exception as e:
            print(f"❌ Error en búsqueda: {e}")
            return None, f"Error: {str(e)}"

    def reproducir_lista(self, inicio_indice=0):
        if not self.spotify_connected:
            print("❌ Spotify no está conectado")
            return "Spotify no conectado"
            
        if not self.lista_reproduccion:
            print("❌ Lista de reproducción vacía")
            return "La lista de reproducción está vacía"
        
        try:
            print(f"▶️ Intentando reproducir lista desde índice {inicio_indice}")
            dispositivos = self.sp.devices()
            id_dispositivo = None
            
            for d in dispositivos["devices"]:
                if d["is_active"]:
                    id_dispositivo = d["id"]
                    print(f"🎯 Dispositivo activo encontrado: {d['name']}")
                    break
            
            if not id_dispositivo:
                print("❌ No hay dispositivo activo de Spotify")
                return "No hay dispositivo activo. Abre Spotify en algún dispositivo."
            
            # Obtener todas las URIs de la lista de reproducción
            uris = [track[2] for track in self.lista_reproduccion]
            print(f"🎵 Reproduciendo {len(uris)} canciones...")
            
            # Configurar repetición
            estado_repetir = "context" if self.repetir else "off"
            print(f"🔁 Estado de repetición: {estado_repetir}")
            self.sp.repeat(state=estado_repetir, device_id=id_dispositivo)
            
            # Reproducir desde el índice especificado
            self.sp.start_playback(device_id=id_dispositivo, uris=uris, offset={"position": inicio_indice})
            self.indice_reproduccion_actual = inicio_indice
            
            mensaje = f"Reproduciendo: {self.lista_reproduccion[inicio_indice][0]}"
            print(f"✅ {mensaje}")
            return mensaje
        
        except Exception as e:
            print(f"❌ Error al reproducir: {e}")
            return f"Error al reproducir: {str(e)}"

    def manejar_borrado_rapido(self):
        tiempo_actual = pygame.time.get_ticks()
        
        if self.tecla_backspace_presionada:
            tiempo_desde_ultimo_borrado = tiempo_actual - self.tiempo_ultimo_backspace
            
            if tiempo_desde_ultimo_borrado > self.intervalo_backspace_rapido:
                if self.activo_cancion and self.input_cancion:
                    self.input_cancion = self.input_cancion[:-1]
                    self.tiempo_ultimo_backspace = tiempo_actual
                elif self.activo_artista and self.input_artista:
                    self.input_artista = self.input_artista[:-1]
                    self.tiempo_ultimo_backspace = tiempo_actual

    def render(self):
        tiempo_actual = pygame.time.get_ticks()

        # Actualizar información de reproducción cada segundo
        if tiempo_actual - self.ultima_actualizacion > self.intervalo_actualizacion:
            self.ultima_actualizacion = tiempo_actual
            # La información se actualizará automáticamente en dibujar_reproduccion_actual
        
        # Manejar borrado rápido
        self.manejar_borrado_rapido()
        
        # Limpiar mensaje después de 3 segundos
        if self.mensaje and tiempo_actual - self.tiempo_mensaje > 3000:
            self.mensaje = ""
        
        self.screen.fill(self.FONDO_OSCURO)
        
        # Título
        self.dibujar_texto("Reproductor de Spotify", self.fuente_titulo, self.VERDE_SPOTIFY, 
                        self.RESOLUTION[0]//2 - 200, 35, sombra=True)
        
        # Campos de entrada
        self.dibujar_caja_entrada(self.caja_cancion, self.input_cancion, self.activo_cancion, "Canción", "¿Qué quieres reproducir?")
        self.dibujar_caja_entrada(self.caja_artista, self.input_artista, self.activo_artista, "Artista", "¿Y de quién?")
        
        # Botones principales
        hover_reproducir = self.dibujar_boton(self.boton_reproducir, "Reproducir", self.VERDE_SPOTIFY, self.VERDE_BRILLANTE)
        hover_pausar = self.dibujar_boton(self.boton_pausar, "Pausar", self.GRIS_CLARO, self.GRIS)
        hover_reanudar = self.dibujar_boton(self.boton_reanudar, "Reanudar", self.VERDE_SPOTIFY, self.VERDE_BRILLANTE)
        
        # Botón de repetir con estado visual
        color_repetir = self.VERDE_SPOTIFY if self.repetir else self.GRIS_CLARO
        color_hover_repetir = self.VERDE_BRILLANTE if self.repetir else self.GRIS
        hover_repetir = self.dibujar_boton(self.boton_repetir, f"Repetir", color_repetir, color_hover_repetir)
        
        # Botones de lista de reproducción
        hover_anadir = self.dibujar_boton(self.boton_anadir, "Añadir a Lista", self.VERDE_SPOTIFY, self.VERDE_BRILLANTE)
        hover_limpiar = self.dibujar_boton(self.boton_limpiar, "Limpiar Lista", (200, 60, 60), (255, 100, 100))
        hover_reproducir_lista = self.dibujar_boton(self.boton_reproducir_lista, "Reproducir Lista", self.VERDE_SPOTIFY, self.VERDE_BRILLANTE)

        # Dibujar información de reproducción actual
        self.dibujar_reproduccion_actual()
        
        # Dibujar área de la lista de reproducción
        pygame.draw.rect(self.screen, self.GRIS_MÁS_OSCURO, self.area_lista, border_radius=10)
        pygame.draw.rect(self.screen, self.GRIS, self.area_lista, 2, border_radius=10)
        
        # Título de la lista
        self.dibujar_texto(f"Lista de Reproducción ({len(self.lista_reproduccion)} canciones)", 
                        self.fuente_pequeña, self.VERDE_SPOTIFY, self.area_lista.x + 10, self.area_lista.y + 10)
        
        # Dibujar canciones en la lista con scroll y botones
        if self.lista_reproduccion:
            # Calcular qué elementos son visibles
            inicio_visible = self.scroll_offset // 32
            fin_visible = inicio_visible + (self.area_lista.height // 32) + 2
            
            # Crear superficie temporal para el contenido desplazable
            altura_total = len(self.lista_reproduccion) * 32 + 50
            superficie_lista = pygame.Surface((self.area_lista.width - 20, altura_total))
            superficie_lista.fill(self.GRIS_MÁS_OSCURO)

            # Dibujar solo los elementos visibles (mejora rendimiento)
            for i in range(max(0, inicio_visible), min(len(self.lista_reproduccion), fin_visible)):
                nombre, artista, uri = self.lista_reproduccion[i]
                pos_y = 40 + i * 32
                rect_item = pygame.Rect(10, pos_y, self.area_lista.width - 30, 30)

                # Fondo del ítem
                color_item = self.GRIS_CLARO if i == self.indice_reproduccion_actual else self.GRIS_MÁS_OSCURO
                pygame.draw.rect(superficie_lista, color_item, rect_item, border_radius=5)

                # Texto de la canción
                texto_mostrar = f"{i+1}. {nombre} - {artista}"
                if len(texto_mostrar) > 60:
                    texto_mostrar = texto_mostrar[:57] + "..."
                superficie_lista.blit(self.fuente_muy_pequeña.render(texto_mostrar, True, self.BLANCO), (15, pos_y + 5))

                # --- Botones más grandes ---
                x_base = rect_item.right - 90
                y_centro = pos_y + 2

                # Subir 🔼
                pygame.draw.rect(superficie_lista, (80, 80, 80), (x_base, y_centro, 24, 24), border_radius=5)
                superficie_lista.blit(self.fuente_iconos.render("▲", True, self.BLANCO), (x_base + 6, y_centro + 1))

                # Bajar 🔽
                pygame.draw.rect(superficie_lista, (80, 80, 80), (x_base + 29, y_centro, 24, 24), border_radius=5)
                superficie_lista.blit(self.fuente_iconos.render("▼", True, self.BLANCO), (x_base + 35, y_centro + 1))

                # Eliminar ❌
                pygame.draw.rect(superficie_lista, (120, 50, 50), (x_base + 58, y_centro, 24, 24), border_radius=5)
                superficie_lista.blit(self.fuente_iconos.render("✖", True, self.BLANCO), (x_base + 64, y_centro + 1))

            # Mostrar el contenido recortado en el área visible
            self.screen.blit(superficie_lista, (self.area_lista.x + 5, self.area_lista.y + 5),
                            (0, self.scroll_offset, self.area_lista.width - 20, self.area_lista.height - 10))

            # Dibujar borde
            pygame.draw.rect(self.screen, self.GRIS, self.area_lista, 2, border_radius=10)
        
        # Mensaje de estado
        if self.mensaje:
            self.dibujar_texto(self.mensaje, self.fuente_pequeña, self.VERDE_SPOTIFY, 
                            self.RESOLUTION[0]//2 - len(self.mensaje)*4, 300)
        
        # Instrucciones
        self.dibujar_texto("Añade canciones a la lista y reprodúcelas en orden", self.fuente_pequeña, self.GRIS, self.RESOLUTION[0]//2 - 180, 660)
        
        # Botón de volver
        if self.back_buttonx.draw():
            from options_menu import OptionsMenu
            self.cambiar_ventana(OptionsMenu)

        pygame.display.flip()

    def handle_events(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.running = False
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.running = False
                
                # Manejar Backspace
                elif evento.key == pygame.K_BACKSPACE:
                    self.tecla_backspace_presionada = True
                    self.tiempo_ultimo_backspace = pygame.time.get_ticks() + self.intervalo_backspace_inicial
                    
                    if self.activo_cancion and self.input_cancion:
                        self.input_cancion = self.input_cancion[:-1]
                    elif self.activo_artista and self.input_artista:
                        self.input_artista = self.input_artista[:-1]
                        
                # Manejar entrada de texto normal
                elif self.activo_cancion:
                    if evento.key == pygame.K_RETURN:
                        self.activo_cancion = False
                        self.activo_artista = True
                    elif evento.key != pygame.K_BACKSPACE:
                        self.input_cancion += evento.unicode
                        
                elif self.activo_artista:
                    if evento.key == pygame.K_RETURN:
                        self.activo_artista = False
                    elif evento.key != pygame.K_BACKSPACE:
                        self.input_artista += evento.unicode

            elif evento.type == pygame.VIDEORESIZE:
                self.RESOLUTION = (evento.w, evento.h)
                self.screen = pygame.display.set_mode(self.RESOLUTION, pygame.RESIZABLE)
                self.recalcular_interfaz(evento.w, evento.h)

            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_BACKSPACE:
                    self.tecla_backspace_presionada = False

            elif evento.type == pygame.MOUSEWHEEL:
                if self.area_lista.collidepoint(pygame.mouse.get_pos()):
                    self.scroll_offset -= evento.y * self.scroll_velocidad
                    altura_total_lista = len(self.lista_reproduccion) * 32 + 40
                    max_scroll = max(0, altura_total_lista - self.area_lista.height + 10)
                    self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button != 1:
                    continue
                    
                # Manejar clics en campos de texto
                if self.caja_cancion.collidepoint(evento.pos):
                    self.activo_cancion = True
                    self.activo_artista = False
                elif self.caja_artista.collidepoint(evento.pos):
                    self.activo_artista = True
                    self.activo_cancion = False
                else:
                    self.activo_cancion = self.activo_artista = False
                
                # Botón de repetir
                if self.boton_repetir.collidepoint(evento.pos):
                    self.repetir = not self.repetir
                    self.mensaje = f"Repetición: {'Activada' if self.repetir else 'Desactivada'}"
                    self.tiempo_mensaje = pygame.time.get_ticks()
                
                # BOTÓN REPRODUCIR CANCIÓN INDIVIDUAL - CORREGIDO
                if self.boton_reproducir.collidepoint(evento.pos) and self.input_cancion.strip():
                    print("🎵 Botón Reproducir presionado")
                    info_cancion, resultado = self.buscar_cancion(self.input_cancion, self.input_artista)
                    if info_cancion:
                        try:
                            print("▶️ Intentando reproducir canción individual...")
                            dispositivos = self.sp.devices()
                            id_dispositivo = None
                            for d in dispositivos["devices"]:
                                if d["is_active"]:
                                    id_dispositivo = d["id"]
                                    print(f"🎯 Usando dispositivo: {d['name']}")
                                    break
                            
                            if id_dispositivo:
                                estado_repetir = "track" if self.repetir else "off"
                                print(f"🔁 Configurando repetición: {estado_repetir}")
                                self.sp.repeat(state=estado_repetir, device_id=id_dispositivo)
                                
                                print(f"🎶 Reproduciendo URI: {info_cancion['uri']}")
                                self.sp.start_playback(device_id=id_dispositivo, uris=[info_cancion["uri"]])
                                
                                self.mensaje = f"Reproduciendo: {info_cancion['nombre']}"
                                print(f"✅ Canción individual en reproducción: {info_cancion['nombre']}")
                            else:
                                self.mensaje = "Active un dispositivo de Spotify"
                                print("❌ No hay dispositivo activo")
                        except Exception as e:
                            self.mensaje = f"Error: {str(e)}"
                            print(f"❌ Error reproduciendo canción individual: {e}")
                    else:
                        self.mensaje = resultado
                    self.tiempo_mensaje = pygame.time.get_ticks()
                
                # BOTÓN PAUSAR - CORREGIDO
                if self.boton_pausar.collidepoint(evento.pos):
                    print("⏸️ Botón Pausar presionado")
                    try:
                        dispositivos = self.sp.devices()
                        id_dispositivo = None
                        for d in dispositivos["devices"]:
                            if d["is_active"]:
                                id_dispositivo = d["id"]
                                break
                        
                        if id_dispositivo:
                            self.sp.pause_playback(device_id=id_dispositivo)
                            self.mensaje = "Música pausada"
                            print("✅ Música pausada")
                        else:
                            self.mensaje = "No hay dispositivo activo"
                            print("❌ No hay dispositivo activo para pausar")
                    except Exception as e:
                        self.mensaje = f"Error al pausar: {str(e)}"
                        print(f"❌ Error al pausar: {e}")
                    self.tiempo_mensaje = pygame.time.get_ticks()
                
                # BOTÓN REANUDAR - CORREGIDO
                if self.boton_reanudar.collidepoint(evento.pos):
                    print("▶️ Botón Reanudar presionado")
                    try:
                        dispositivos = self.sp.devices()
                        id_dispositivo = None
                        for d in dispositivos["devices"]:
                            if d["is_active"]:
                                id_dispositivo = d["id"]
                                break
                        
                        if id_dispositivo:
                            self.sp.start_playback(device_id=id_dispositivo)
                            self.mensaje = "Música reanudada"
                            print("✅ Música reanudada")
                        else:
                            self.mensaje = "No hay dispositivo activo"
                            print("❌ No hay dispositivo activo para reanudar")
                    except Exception as e:
                        self.mensaje = f"Error al reanudar: {str(e)}"
                        print(f"❌ Error al reanudar: {e}")
                    self.tiempo_mensaje = pygame.time.get_ticks()
                
                # Añadir a la lista
                if self.boton_anadir.collidepoint(evento.pos) and self.input_cancion.strip():
                    info_cancion, resultado = self.buscar_cancion(self.input_cancion, self.input_artista)
                    if info_cancion:
                        self.lista_reproduccion.append([info_cancion["nombre"], info_cancion["artista"], info_cancion["uri"]])
                        self.mensaje = f"Añadido: {info_cancion['nombre']}"
                        self.input_cancion = ""
                        self.input_artista = ""
                    else:
                        self.mensaje = resultado
                    self.tiempo_mensaje = pygame.time.get_ticks()
                
                # Limpiar lista
                if self.boton_limpiar.collidepoint(evento.pos):
                    self.lista_reproduccion.clear()
                    self.indice_reproduccion_actual = -1
                    self.mensaje = "Lista de reproducción limpiada"
                    self.tiempo_mensaje = pygame.time.get_ticks()
                
                # Reproducir lista completa
                if self.boton_reproducir_lista.collidepoint(evento.pos):
                    if self.lista_reproduccion:
                        self.mensaje = self.reproducir_lista(0)
                    else:
                        self.mensaje = "La lista de reproducción está vacía"
                    self.tiempo_mensaje = pygame.time.get_ticks()

                # Manejar clics en elementos de la lista
                if self.area_lista.collidepoint(evento.pos) and self.lista_reproduccion:
                    # Ajustar la posición Y considerando el scroll
                    mouse_y_relativo = evento.pos[1] - self.area_lista.y - 5 + self.scroll_offset
                    indice_item = (mouse_y_relativo - 40) // 32
                    
                    if 0 <= indice_item < len(self.lista_reproduccion):
                        # Calcular posición X relativa dentro del área de la lista
                        mouse_x_relativo = evento.pos[0] - self.area_lista.x - 5
                        
                        # Coordenadas de los botones para este ítem
                        x_base = (self.area_lista.width - 20) - 90  # Nueva posición relativa
                        item_y = 40 + indice_item * 32

                        # Verificar clics en botones (áreas de 24x24)
                        if x_base <= mouse_x_relativo <= x_base + 24 and item_y <= mouse_y_relativo <= item_y + 24:
                            # Botón subir ▲
                            if indice_item > 0:
                                self.lista_reproduccion[indice_item], self.lista_reproduccion[indice_item-1] = self.lista_reproduccion[indice_item-1], self.lista_reproduccion[indice_item]
                                if self.indice_reproduccion_actual == indice_item:
                                    self.indice_reproduccion_actual -= 1
                                elif self.indice_reproduccion_actual == indice_item - 1:
                                    self.indice_reproduccion_actual += 1
                                self.mensaje = "Canción movida hacia arriba"
                                self.tiempo_mensaje = pygame.time.get_ticks()

                        elif x_base + 29 <= mouse_x_relativo <= x_base + 53 and item_y <= mouse_y_relativo <= item_y + 24:
                            # Botón bajar ▼
                            if indice_item < len(self.lista_reproduccion) - 1:
                                self.lista_reproduccion[indice_item], self.lista_reproduccion[indice_item+1] = self.lista_reproduccion[indice_item+1], self.lista_reproduccion[indice_item]
                                if self.indice_reproduccion_actual == indice_item:
                                    self.indice_reproduccion_actual += 1
                                elif self.indice_reproduccion_actual == indice_item + 1:
                                    self.indice_reproduccion_actual -= 1
                                self.mensaje = "Canción movida hacia abajo"
                                self.tiempo_mensaje = pygame.time.get_ticks()

                        elif x_base + 58 <= mouse_x_relativo <= x_base + 82 and item_y <= mouse_y_relativo <= item_y + 24:
                            # Botón eliminar ❌
                            cancion_eliminada = self.lista_reproduccion.pop(indice_item)
                            if self.indice_reproduccion_actual == indice_item:
                                self.indice_reproduccion_actual = -1
                            elif self.indice_reproduccion_actual > indice_item:
                                self.indice_reproduccion_actual -= 1
                            self.mensaje = f"Eliminado: {cancion_eliminada[0]}"
                            self.tiempo_mensaje = pygame.time.get_ticks()

                        else:
                            # Clic en el elemento de la lista (no en botones) para reproducir
                            self.mensaje = self.reproducir_lista(indice_item)
                            self.tiempo_mensaje = pygame.time.get_ticks()