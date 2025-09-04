import numpy as np

ELECTRON_MASS = 9.11e-31
ELECTRON_CHARGE = 1.602e-19

def campo_electrico(voltage, distancia):
    """E = V/d (modelo placas paralelas ideal)."""
    return voltage / max(1e-9, distancia)

def velocidad_electron(voltaje_aceleracion, masa=ELECTRON_MASS, q=ELECTRON_CHARGE):
    """
    1/2 m v^2 = q V => v = sqrt(2 q V / m).
    (Usado solo para intuición; el render usa una escala a píxeles).
    """
    return np.sqrt(max(0.0, 2.0 * q * voltaje_aceleracion / masa))

def señal_seno(freq, fase, t, amplitud_px):
    """Señal sinusoidal en píxeles."""
    return amplitud_px * np.sin(2*np.pi*freq*t + fase)

def map_range(value, a_min, a_max, b_min, b_max):
    """Mapea value de [a_min,a_max] a [b_min,b_max]."""
    if a_max == a_min:
        return (b_min + b_max) / 2
    t = (value - a_min) / (a_max - a_min)
    return b_min + t * (b_max - b_min)
