import time
import numpy as np
from utils import señal_seno, map_range, velocidad_electron

class CRT:
    """
    Modelo didáctico (simplificado) de un CRT controlado por placas.
    - 'modo': 'manual' o 'sinusoidal'
    - Voltajes de placas mapean a deflexión en píxeles.
    - Voltaje de aceleración mapea a brillo.
    """
    def __init__(self):
        # Parámetros fijos de escena
        self.ancho_pantalla_px = 300   # tamaño del "display" en pixeles
        self.alto_pantalla_px  = 400
        self.amplitud_max_px   = 140   # deflexión máxima visible (dentro del marco)

        # Estado controlable por usuario
        self.modo = "manual"  # "manual" | "sinusoidal"

        # Rangos físicos (ajustables)
        self.Vacc_min, self.Vacc_max = 500.0, 5000.0       # V
        self.Vx_min, self.Vx_max     = -150.0, 150.0       # V (placas horizontales)
        self.Vy_min, self.Vy_max     = -150.0, 150.0       # V (placas verticales)
        self.persist_min, self.persist_max = 0.05, 2.5     # s

        # Valores actuales
        self.voltaje_aceleracion = 2000.0
        self.voltaje_horizontal  = 0.0
        self.voltaje_vertical    = 0.0
        self.tiempo_persistencia = 0.6

        # Señales sinusoidales
        self.freq_x = 2.0
        self.freq_y = 3.0
        self.phase_y = np.pi/2
        self.freq_min, self.freq_max = 0.1, 15.0
        self.phase_min, self.phase_max = -np.pi, np.pi

        # Persistencia: lista de (x_pix_rel, y_pix_rel, timestamp, brillo 0..255)
        self.persistencia = []

    # Cálculo de posición del haz
    def _deflexion_px_desde_voltaje(self, vx, vy):
        """
        Mapea voltajes de placas a desplazamientos en píxeles (modelo lineal).
        vx -> desplazamiento horizontal; vy -> vertical (signo según convención).
        """
        dx = map_range(vx, self.Vx_min, self.Vx_max, -self.amplitud_max_px, self.amplitud_max_px)
        dy = map_range(vy, self.Vy_min, self.Vy_max, -self.amplitud_max_px, self.amplitud_max_px)
        return dx, dy

    def calcular_posicion(self, t):
        """Posición del haz relativa al centro del display, en píxeles."""
        if self.modo == "sinusoidal":
            x = señal_seno(self.freq_x, 0.0, t, self.amplitud_max_px)
            y = señal_seno(self.freq_y, self.phase_y, t, self.amplitud_max_px)
        else:
            x, y = self._deflexion_px_desde_voltaje(self.voltaje_horizontal, self.voltaje_vertical)
        return x, y

    # Persistencia y brillo
    def brillo_actual(self):
        """
        Brillo ~ velocidad de electrones (mapeo simple Vacc -> 100..255).
        """
        # Podemos usar v como guía pero solo hacemos un mapeo lineal por simplicidad.
        _ = velocidad_electron(self.voltaje_aceleracion)  # por cultura general :)
        return int(map_range(self.voltaje_aceleracion, self.Vacc_min, self.Vacc_max, 100, 255))

    def push_persistencia(self, x_rel, y_rel):
        """Guarda el punto del haz con su timestamp y brillo actual."""
        self.persistencia.append((x_rel, y_rel, time.time(), self.brillo_actual()))

    def depurar_persistencia(self):
        """Elimina puntos cuyo tiempo exceda el tiempo de persistencia."""
        ahora = time.time()
        self.persistencia = [(x, y, ts, bri) for (x, y, ts, bri) in self.persistencia
                             if (ahora - ts) <= self.tiempo_persistencia]