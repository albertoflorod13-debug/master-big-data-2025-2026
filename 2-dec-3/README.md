# Ejercicio extra APIs con FastAPI y Pydantic:

Imagina que tu API se usa desde una pequeña web/app en la oficina para gestionar una **cola de canciones compartida**: cualquiera puede proponer canciones y ver qué viene después. No hay base de datos: todo vive en memoria mientras el servidor está levantado.

## Objetivo

Crear un mini-servicio con FastAPI + Pydantic que permita a usuarios finales:

- Ver la cola actual de canciones pendientes.
- Añadir nuevas canciones a la cola.
- Ver cuál es la siguiente canción que sonará.
- Votar positivo/negativo una canción para reordenar la cola.

## Requisitos funcionales

Tu API debe exponer, como mínimo, estos endpoints:

1. **GET /queue**
   - Devuelve la cola completa de canciones en el orden en que se reproducirán.
   - Cada elemento debe incluir al menos: título, artista, quién la ha añadido (nombre o nick) y un contador de votos.

2. **POST /queue**
   - Recibe los datos de una nueva canción (título, artista, usuario que la propone).
   - La añade al final de la cola con votos iniciales a 0.
   - Responde con la canción añadida y su posición en la cola.

3. **GET /queue/next**
   - Devuelve la siguiente canción que “toca”.
   - Si la cola está vacía, devuelve un mensaje apropiado.

4. **POST /queue/{posicion}/vote**
   - Recibe un voto (+1 o -1) para la canción en esa posición.
   - Actualiza el contador de votos.
   - Puedes usar los votos para reordenar la cola (por ejemplo, las canciones con más votos suben posiciones).

## Requisitos técnicos

- Usa **modelos Pydantic** para validar las canciones y, si quieres, las peticiones de voto.
- El almacenamiento debe ser en memoria, usando:
  - Una **lista de modelos Pydantic**
- Debes manejar casos de error:
  - Votar una posición que no existe.
  - Consultar la siguiente canción cuando la cola está vacía.

## Extensiones opcionales

- Añadir un campo “duración (segundos)” y devolver el **tiempo total aproximado** de la cola.

## Documentación útil

- [Docs avanzados FastAPI](https://fastapi.tiangolo.com/tutorial/)
- [Pydantic Models](https://docs.pydantic.dev/latest/)