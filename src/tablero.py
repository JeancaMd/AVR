import pygame

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (100, 150, 255)


class Celda:
    def __init__(self, fila, columna, tamaño, offset_x=0, offset_y=0):
        self.fila = fila
        self.columna = columna
        self.tamaño = tamaño
        self.color = WHITE
        self.rook = None
        self.rect = pygame.Rect(
            offset_x + columna * tamaño,
            offset_y + fila * tamaño,
            tamaño,
            tamaño
        )

    def draw(self, screen):
        pygame.draw.rect(screen, (240, 240, 240), self.rect)
        pygame.draw.rect(screen, (180, 180, 180), self.rect, 1)

        if self.rook:
            self.rook.draw(screen)

    def handle_click(self, pos, rook_class=None):
        if self.rect.collidepoint(pos):
            if self.rook is not None:
                return False

            if rook_class is None:
                return False

            size = self.rect.width
            top_left_x = self.rect.x
            top_left_y = self.rect.y
            self.rook = rook_class(top_left_x, top_left_y, size)
            return True

        return False


class Tablero:
    FILAS = 9
    COLUMNAS = 5
    TAMAÑO_CELDA = 60

    def __init__(self, window_size):
        self.window_width, self.window_height = window_size

        self.tablero_width = self.COLUMNAS * self.TAMAÑO_CELDA
        self.tablero_height = self.FILAS * self.TAMAÑO_CELDA

        self.offset_x = (self.window_width - self.tablero_width) // 2
        self.offset_y = (self.window_height - self.tablero_height) // 2

        self.celdas = [
            [
                Celda(f, c, self.TAMAÑO_CELDA, self.offset_x, self.offset_y)
                for c in range(self.COLUMNAS)
            ]
            for f in range(self.FILAS)
        ]

    def draw(self, surface):
        # Dibujar todas las celdas y rooks
        for fila in self.celdas:
            for celda in fila:
                celda.draw(surface)

    def draw_attacks(self, surface):
        """Dibuja los sprites de ataque de todos los rooks (llamar después de dibujar avatares)"""
        for fila in self.celdas:
            for celda in fila:
                if celda.rook:
                    celda.rook.draw_attack(surface)

    def handle_click(self, pos, rook_class):
        for fila in self.celdas:
            for celda in fila:
                if celda.rect.collidepoint(pos):
                    colocado = celda.handle_click(pos, rook_class)
                    return colocado
        return False
    
    def update(self):
        for fila in self.celdas:
            for celda in fila:
                if celda.rook:
                    celda.rook.update()

    def limpiar_rooks_muertos(self):
        for fila in self.celdas:
            for celda in fila:
                if celda.rook and celda.rook.vida <= 0:
                    celda.rook = None