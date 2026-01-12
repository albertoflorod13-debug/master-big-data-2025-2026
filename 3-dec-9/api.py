from datetime import time

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


class Vote(BaseModel):
    """Modelo que representa un voto sobre una canción.

    Attributes:
        voto (bool): True para voto positivo, False para voto negativo.
    """
    voto: bool


class Cancion(BaseModel):
    """Modelo que representa una canción de la cola.

    Attributes:
        votos (int): Número de votos recibidos por la canción.
        usuario (str): Usuario que añadió la canción.
        titulo (str): Título de la canción.
        artista (str): Artista de la canción.
        duracion (time): Duración de la canción.
    """
    votos: int = 0
    usuario: str
    titulo: str
    artista: str
    duracion: time


db: list[Cancion] = []

app = FastAPI()


@app.post("/queue", status_code=status.HTTP_201_CREATED, response_model=Cancion)
def add_song(song: Cancion):
    """Añade una canción a la cola.

    Args:
        song (Cancion): Canción que se desea agregar.

    Returns:
        Cancion: La canción añadida.
    """
    db.append(song)
    return song


@app.get("/queue", response_model=list[Cancion])
def get_queue():
    """Obtiene la cola actual de canciones.

    Returns:
        list[Cancion]: Lista de canciones en cola.
    """
    return db


@app.get("/queue/next", response_model=Cancion)
def get_next():
    """Obtiene y elimina la siguiente canción en la cola.

    Returns:
        Cancion: La siguiente canción disponible.

    Raises:
        HTTPException: Si la cola está vacía.
    """
    if not db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay canciones",
        )
    # Con list usamos pop(0), no popleft()
    return db.pop(0)


@app.post("/queue/{position}/vote", status_code=status.HTTP_201_CREATED)
def vote_song(position: int, vote: Vote):
    """Vota positiva o negativamente una canción según su posición.

    El voto se recibe en el cuerpo de la petición como un objeto `Vote`.

    Args:
        position (int): Índice de la canción en la cola.
        vote (Vote): Objeto con el campo ``voto`` (True para positivo, False para negativo).

    Returns:
        dict: Confirmación de voto y total de votos actualizados.

    Raises:
        HTTPException: Si la posición es inválida.
    """
    if position < 0 or position >= len(db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Posición no válida",
        )

    if vote.voto:
        db[position].votos += 1
    else:
        db[position].votos -= 1

    votos = db[position].votos

    db.sort(key=lambda x: x.votos, reverse=True)

    return {"ok": True, "votos": votos}