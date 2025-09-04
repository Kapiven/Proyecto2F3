import pygame
from utils import map_range
import math

WHITE = (255, 255, 255)
GREY  = (150, 150, 150)
DARK  = (60, 60, 60)
GREEN = (0, 255, 0)
BLACK = (255, 255, 255)

class Slider:
    def __init__(self, x, y, w, name, vmin, vmax, value, decimals=2, units=""):
        self.rect = pygame.Rect(x, y, w, 28)
        self.track = pygame.Rect(x, y+18, w, 4)
        self.name = name
        self.vmin = vmin
        self.vmax = vmax
        self.value = value
        self.decimals = decimals
        self.units = units
        self.dragging = False
        self.font = pygame.font.SysFont(None, 20)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.track.collidepoint(event.pos):
            self.dragging = True
            self._update_from_mouse(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._update_from_mouse(event.pos[0])

    def _update_from_mouse(self, mx):
        t = (mx - self.track.left) / max(1, self.track.width)
        t = max(0.0, min(1.0, t))
        self.value = self.vmin + t*(self.vmax - self.vmin)

    def draw(self, screen):
        # etiqueta
        label = f"{self.name}: {round(self.value, self.decimals)}{self.units}"
        screen.blit(self.font.render(label, True, WHITE), (self.rect.x, self.rect.y))
        # carril
        pygame.draw.rect(screen, GREY, self.track)
        # knob
        t = (self.value - self.vmin) / (self.vmax - self.vmin)
        kx = int(self.track.left + t*self.track.width)
        pygame.draw.circle(screen, GREEN, (kx, self.track.centery), 7)

class ToggleButton:
    def __init__(self, x, y, w, h, labels=("MANUAL","SINUS"), initial=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.on = initial
        self.labels = labels
        self.font = pygame.font.SysFont(None, 20)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.on = not self.on

    def draw(self, screen):
        pygame.draw.rect(screen, (30,130,30) if self.on else (130,30,30), self.rect, border_radius=10)
        text = self.labels[1] if self.on else self.labels[0]
        surf = self.font.render(text, True, WHITE)
        screen.blit(surf, (self.rect.centerx - surf.get_width()//2, self.rect.centery - surf.get_height()//2))

class ControlPanel:
    """
    Panel de control en la parte inferior con sliders y modo.
    Sin dependencias extra; todo en pygame.
    """
    def __init__(self, screen_width, screen_height):
        self.rect = pygame.Rect(0, screen_height-120, screen_width, 120)
        x0 = 24
        gap = 200

        # sliders
        self.s_vacc = Slider(x0+0*gap,  screen_height-112, 180, "V_acel",   500, 5000, 2000, 0, " V")
        self.s_vy   = Slider(x0+1*gap,  screen_height-112, 180, "V_vertical", -150, 150,   0, 1, " V")
        self.s_vx   = Slider(x0+2*gap,  screen_height-112, 180, "V_horizontal", -150, 150, 0, 1, " V")
        self.s_pers = Slider(x0+3*gap,  screen_height-112, 180, "Persistencia", 0.05, 2.5, 0.6, 2, " s")
        self.s_fx   = Slider(x0+4*gap,  screen_height-112, 180, "f_x", 0.1, 15.0, 2.0, 2, " Hz")
        self.s_fy   = Slider(x0+5*gap,  screen_height-112, 180, "f_y", 0.1, 15.0, 3.0, 2, " Hz")
        self.s_phi  = Slider(x0+6*gap,  screen_height-112, 180, "fase_y", -math.pi, math.pi, math.pi/2, 2, " rad")

        self.toggle = ToggleButton(screen_width-150, screen_height-75, 120, 32, labels=("MANUAL","SINUS"), initial=False)
        self.font = pygame.font.SysFont(None, 22)

        self.sliders = [self.s_vacc, self.s_vy, self.s_vx, self.s_pers, self.s_fx, self.s_fy, self.s_phi]

    def handle_event(self, event, crt):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
            for s in self.sliders:
                s.handle_event(event)
            self.toggle.handle_event(event)
            # aplicar a CRT
            crt.voltaje_aceleracion = self.s_vacc.value
            crt.voltaje_vertical    = self.s_vy.value
            crt.voltaje_horizontal  = self.s_vx.value
            crt.tiempo_persistencia = self.s_pers.value
            crt.freq_x              = self.s_fx.value
            crt.freq_y              = self.s_fy.value
            crt.phase_y             = self.s_phi.value
            crt.modo                = "sinusoidal" if self.toggle.on else "manual"

    def draw(self, screen):
        pygame.draw.rect(screen, DARK, self.rect)
        for s in self.sliders:
            s.draw(screen)
        self.toggle.draw(screen)
        help_txt = "Click y arrastra los sliders | Botón: MANUAL/SINUS"
        screen.blit(self.font.render(help_txt, True, WHITE), (14, self.rect.y+88))
