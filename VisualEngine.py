from typing import Optional
import pygame

from GameEngine import GameEngine, State


class VisualEngine:
    pygame.init()

    PADDING_TOP = 200
    WIDTH, HEIGHT = 600, 600 + PADDING_TOP
    ROWS, COLS = 4, 4

    BOARD_COLOR = (187, 173, 160)   # Main grid background
    EMPTY_TILE = (205, 193, 180)    # 0 / Empty square

    PADDING = 10
    TILE_SIZE = (WIDTH - (ROWS + 1) * PADDING) // ROWS

    # Font colors for contrast
    TEXT_DARK = (119, 110, 101)
    TEXT_LIGHT = (249, 246, 242)

    TILE_COLORS = {
        0: (205, 193, 180),     # Empty cell
        2: (238, 228, 218),     #
        4: (237, 224, 200),     #
        8: (242, 177, 121),     #
        16: (245, 149, 99),     #
        32: (246, 124, 95),     #
        64: (246, 94, 59),      #
        128: (237, 207, 114),   #
        256: (237, 204, 97),    #
        512: (237, 200, 80),    #
        1024: (237, 197, 63),   #
        2048: (237, 194, 46),   #
    }

    SUPER_TILE_COLOR = (60, 58, 50)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2048")
    font = pygame.font.SysFont("arial", 36, bold=True)
    label_font = pygame.font.SysFont("arial", 16, bold=True)
    value_font = pygame.font.SysFont("arial", 20)


    def __init__(self, engine: Optional[GameEngine] = GameEngine()):
        self.score = 0
        self.high_score = 9999
        self.gameEngine = engine


    def draw_text(self, surface, text, font, color, **anchor):
        """Render text and place it using a rect anchor, e.g. center=(x, y)."""
        img = font.render(text, True, color)
        rect = img.get_rect(**anchor)
        surface.blit(img, rect)
        return rect

    def draw_stat_box(self, surface, rect, label, value):
        pygame.draw.rect(surface, (50, 50, 70), rect, border_radius=8)
        self.draw_text(surface, label, self.label_font, (180, 180, 200), midtop=(rect.centerx, rect.top + 6))
        self.draw_text(surface, str(value), self.value_font, (255, 255, 255), midbottom=(rect.centerx, rect.bottom - 6))

    
    def draw_header(self):
        header = pygame.Rect(0,0,self.WIDTH, self.PADDING_TOP)
        pygame.draw.rect(self.screen, self.BOARD_COLOR, header)

        inner = header.inflate(-32,-32)
        self.draw_text(self.screen, "2048(not)", self.font, self.TEXT_DARK, midtop=inner.midtop)
        
        # Details row: "space-between" with two boxes
        box_w, box_h = 150, 55
        score_box = pygame.Rect(inner.left, inner.bottom - box_h, box_w, box_h)
        high_box  = pygame.Rect(inner.right - box_w, inner.bottom - box_h, box_w, box_h)

        self.draw_stat_box(self.screen, score_box, "SCORE", self.score)
        self.draw_stat_box(self.screen, high_box, "HIGH SCORE", self.high_score)

    def draw_board(self, screen):
        screen.fill(self.BOARD_COLOR)

        # title, score, and high score on the top padded area
        self.draw_header()

        for row in range(self.ROWS):
            for col in range(self.COLS):
                value = self.gameEngine.get_grid_val(row, col)
                x = self.PADDING + col * (self.TILE_SIZE + self.PADDING)
                y = self.PADDING + self.PADDING_TOP + row * (self.TILE_SIZE + self.PADDING)
                rect = pygame.Rect(x,y, self.TILE_SIZE, self.TILE_SIZE)

                color = self.TILE_COLORS.get(value, (60, 58, 50))
                pygame.draw.rect(screen, color, rect, border_radius=6)

                if value != 0:
                    text_color = self.TEXT_DARK if value <= 4 else self.TEXT_LIGHT
                    text_surface = self.font.render(str(value), True, text_color)
                    text_rect = text_surface.get_rect(center=rect.center)
                    screen.blit(text_surface, text_rect)
                    

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP: 
                        self.gameEngine.shift(state=State.UP)
                    elif event.key == pygame.K_DOWN:
                        self.gameEngine.shift(state=State.DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.gameEngine.shift(state=State.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.gameEngine.shift(state=State.RIGHT)
        
            self.draw_board(self.screen)
            pygame.display.flip()
        
        pygame.quit()