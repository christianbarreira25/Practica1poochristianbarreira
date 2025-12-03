## archivo: gestor_payload.py
from typing import TypeVar, Generic

# Definimos un tipo genérico
T = TypeVar('T')

class GestorPayload(Generic[T]):
    def __init__(self, payload: T):
        self._payload = payload

    def mostrar_payload(self) -> T:
        return self._payload

    def actualizar_payload(self, nuevo_payload: T):
        self._payload = nuevo_payload


