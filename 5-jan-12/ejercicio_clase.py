import numpy as np


def normalize_by_column(m: np.ndarray) -> np.ndarray:
    if len(np.shape(m)) != 2:
        raise ValueError("The input matrix should be bidimensional (2D)")
    if not isinstance(m, np.ndarray):
        raise TypeError("The input should be a numpy matrix")
    maximo = m.max(axis=0)
    minimo = m.min(axis=0)
    dif = np.where(maximo - minimo == 0, 1, maximo - minimo)
    m_normalized = (m - minimo) / dif
    return m_normalized

m = np.array([
    [10,  0,  5],
    [20,  0, 15],
    [30,  0, 25],
], dtype=float)


resultado = normalize_by_column(m)
print (resultado)
print(np.shape(m))

maximo = m.max(axis=0)
minimo = m.min(axis=0)
dif = maximo - minimo.reshape((3,1))
print(f"{dif=}, {maximo=}, {minimo.reshape((3,1))=}")