# Práctica: Procesamiento de Logs en Python

Este repositorio contiene una práctica guiada donde trabajarás con un archivo `logs.json` (no es más que una lista de diccionarios) que simula un conjunto de logs reales. A partir de este dataset deberás realizar varias tareas descritas, tanto dentro de un **notebook Jupyter** como posteriormente desde un **script ejecutable** por terminal.

---

## 1. Set-up del repositorio

1. Haz **fork** de este repositorio en tu propia cuenta de GitHub.  
2. Clona tu fork
3. No olvides crear tu entorno virtual de python. **Obligatorio usar python 3.12 en esta práctica**

---

## 2. Estructura del proyecto

El proyecto contiene:

- `logs.ipynb` → Notebook con las tareas.  
- `logs.json` → Archivo con datos simulados (lista de diccionarios).  
- `test.py` → Tests automáticos para validar tu solución.  
- `README.md` → Este documento.

---

## 3. El notebook: `logs.ipynb`

Dentro del notebook encontrarás varias celdas **vacías** donde debes implementar funciones que trabajarán sobre los datos de `logs.json`.

Cada ejercicio indica exactamente qué debe implementarse.

---

## 4. Exportar el notebook a `.py`

Cuando termines el notebook debes exportarlo a un archivo Python:

### Opción 1 — Desde VSCode
Menu: **File → Save as → Notebook as Python**


---

## 5. Crear un `main` ejecutable desde terminal

Ahora debes modificar tu archivo `.py` para que los dos últimos ejercicios puedan ejecutarse desde la terminal usando **sys.argv**.

El objetivo es que el script pueda ejecutar las funciones que programaste en el notebook según los parámetros de entrada.

Ejemplo

`python -m logs.py --jsonpath logs.json --exercisenumber 1`

La salida debe ser:

{'failed_login': 475, 'api_request': 519, 'view_page': 531, 'delete_item': 514, 'update_profile': 477, 'upload_file': 520, 'change_password': 486, 'login': 471, 'logout': 534, 'download_file': 473}
---

## 6. Ejecutar los tests

Cuando tengas listo tu módulo en `.py`, ejecuta los tests:

```bash
python test.py
```

Los tests deben pasar correctamente para considerar la práctica completada.

---

## 7. Entrega

Crear un commit con la solución a tu repositorio (no olvides el mensaje!).

Suerte!
