# Simulador de un Tubo de Rayos Catódicos (CRT)

Proyecto 2 - Física 3
---

## Descripción

Este proyecto implementa una **simulación interactiva de un Tubo de Rayos Catódicos (CRT)** utilizando **Python + Pygame**.  
El objetivo es mostrar, de forma didáctica, cómo un haz de electrones es acelerado y desviado por placas, generando figuras en la pantalla frontal.

La simulación incluye:

- **Vista lateral** → permite observar la deflexión vertical del haz.  
- **Vista superior** → muestra la deflexión horizontal.  
- **Pantalla frontal** → donde se forma la figura resultante (osciloscopio).  
- **Persistencia ajustable** → efecto de rastro característico de un CRT real.  
- **Modos de operación**:
  - **Manual**: se controlan los voltajes de placas directamente.  
  - **Sinusoidal**: se aplican señales sinusoidales controlables en frecuencia y fase para obtener **Figuras de Lissajous**.  

---

## Estructura del proyecto

- main.py # Punto de entrada principal
- crt.py # Lógica del CRT (modelo físico simplificado)
- views.py # Dibujo de las 3 vistas en pantalla
- controls.py # Panel de sliders y botones de control
- utils.py # Funciones auxiliares (físicas y mapeos)

---

## Instalación

1. Clona o descarga este repositorio.
   ```bash
   git clone https://github.com/Kapiven/Proyecto2F3.git
   ```
3. Instala las dependencias necesarias:
   ```bash
   pip install pygame numpy

## Autores

Pablo Méndez
Karen Pineda 
Andrés Ismalej
Juan Daniel Ordoñez

:]
