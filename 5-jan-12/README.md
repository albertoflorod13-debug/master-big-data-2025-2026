# 12 de Enero - NumPy

Ejercicios con NumPy y optimización de código.

## Contenido

- Notebook introductorio: `numpy_basico.ipynb`
- Ejercicio práctico: Normalización de columnas

## Ejercicio: Normalización de Columnas

### Enunciado

Implementa una función `normalize_by_column` que normalice cada columna de una matriz NumPy.

**Especificaciones:**

1. **Función**: `normalize_by_column(m: np.ndarray) -> np.ndarray`
2. **Entrada**: Una matriz NumPy bidimensional (2D)
3. **Salida**: Una nueva matriz con las mismas dimensiones, donde cada columna está normalizada entre 0 y 1
4. **Fórmula de normalización**: Para cada columna, aplicar Min-Max
5. **Caso especial**: Si una columna tiene todos los valores iguales, todos los valores normalizados deben ser 0, evitar hacer división por 0

Controle las excepciones necesarias.

m - min / (max - min)

**Ejemplo:**

```python
import numpy as np

m = np.array([
    [10,  0,  5],
    [20,  0, 15],
    [30,  0, 25],
], dtype=float)

resultado = normalize_by_column(m)
# Resultado esperado:
# [[0.0, 0.0, 0.0],
#  [0.5, 0.0, 0.5],
#  [1.0, 0.0, 1.0]]
```
