import pygame
import time

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (255, 255, 255)

def draw_frame(screen, rect, radius=18, width=2):
    """Rectángulo con esquinas redondeadas sencillo."""
    x, y, w, h = rect
    pygame.draw.rect(screen, WHITE, (x, y, w, h), width, border_radius=radius)

def draw_views(screen, crt, x_rel, y_rel):
    """
    Dibuja:
      - Vista lateral (izq): deflexión vertical -> punto se mueve en Y
      - Vista superior (centro): deflexión horizontal -> punto en X
      - Pantalla frontal (der): combinación (x_rel, y_rel) con persistencia
    """
    # Paneles
    lateral_rect = (40, 70, 330, 460)
    superior_rect = (420, 70, 330, 460)
    pantalla_rect = (800, 70, 360, 460)

    # Marcos
    draw_frame(screen, lateral_rect)
    draw_frame(screen, superior_rect)
    draw_frame(screen, pantalla_rect)

    # Centros
    lx = lateral_rect[0] + lateral_rect[2] // 2
    ly = lateral_rect[1] + lateral_rect[2] // 2
    sx = superior_rect[0] + superior_rect[2] // 2
    sy = superior_rect[1] + superior_rect[2] // 2
    px = pantalla_rect[0] + pantalla_rect[2] // 2
    py = pantalla_rect[1] + pantalla_rect[3] // 2

    # Vista lateral: solo Y (vertical)
    pygame.draw.circle(screen, GREEN, (lx, int(py + y_rel)), 5)

    # Vista superior: solo X (horizontal)
    pygame.draw.circle(screen, GREEN, (int(px + x_rel) - (800-420), sy), 5)

    # Pantalla frontal con persistencia
    # Nuevo punto
    crt.push_persistencia(x_rel, y_rel)

    # Pintar cola con alpha decreciente según edad
    ahora = time.time()
    nueva = []
    for (xr, yr, ts, bri) in crt.persistencia:
        edad = ahora - ts
        # alpha cae linealmente con edad
        alpha = max(0, int(255 * (1.0 - edad / max(0.001, crt.tiempo_persistencia))))
        if alpha > 0:
            s = pygame.Surface((4, 4), pygame.SRCALPHA)
            s.fill((0, bri, 0, alpha))
            screen.blit(s, (int(px + xr), int(py + yr)))
            nueva.append((xr, yr, ts, bri))
    crt.persistencia = nueva

    # Títulos simples
    _font = pygame.font.SysFont(None, 22)
    screen.blit(_font.render("VISTA LATERAL", True, WHITE), (lateral_rect[0]+80, lateral_rect[1]-24))
    screen.blit(_font.render("VISTA SUPERIOR", True, WHITE), (superior_rect[0]+70, superior_rect[1]-24))
    screen.blit(_font.render("PANTALLA", True, WHITE), (pantalla_rect[0]+120, pantalla_rect[1]-24))
