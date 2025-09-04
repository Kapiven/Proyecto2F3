import pygame
from crt import CRT
from views import draw_views
from controls import ControlPanel

# Configuración de ventana
WIDTH, HEIGHT = 1500, 680
FPS = 60
BLACK = (0, 0, 0)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulador CRT – con sliders")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    crt = CRT()
    panel = ControlPanel(WIDTH, HEIGHT)

    t = 0.0
    running = True
    while running:
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            panel.handle_event(event, crt)

        # Actualización de estado
        x_rel, y_rel = crt.calcular_posicion(t)
        crt.depurar_persistencia()

        screen.fill(BLACK)
        draw_views(screen, crt, x_rel, y_rel)

        # Encabezado
        header = f"Modo: {crt.modo.upper()}   |   V_acel={int(crt.voltaje_aceleracion)}V   " \
                 f"Vx={crt.voltaje_horizontal:.1f}V  Vy={crt.voltaje_vertical:.1f}V   " \
                 f"fx={crt.freq_x:.2f}Hz  fy={crt.freq_y:.2f}Hz  fase_y={crt.phase_y:.2f}rad   " \
                 f"persist={crt.tiempo_persistencia:.2f}s"
        screen.blit(font.render(header, True, (200,200,200)), (20, 20))

        panel.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
        t += 1.0/FPS

    pygame.quit()

if __name__ == "__main__":
    main()
