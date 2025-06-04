class ProductoPerecedero:
    def __init__(self, id, nombre, peso, valor, fecha_expiracion):
        self._id = id
        self._nombre = nombre
        self._peso = peso
        self._valor = valor
        self._fecha_expiracion = fecha_expiracion

    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @property
    def peso(self):
        return self._peso

    @property
    def valor(self):
        return self._valor

    @property
    def fecha_expiracion(self):
        return self._fecha_expiracion

class ProductoElectronico:
    def __init__(self, id, nombre, peso, valor, voltaje):
        self._id = id
        self._nombre = nombre
        self._peso = peso
        self._valor = valor
        self._voltaje = voltaje

    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @property
    def peso(self):
        return self._peso

    @property
    def valor(self):
        return self._valor

    @property
    def voltaje(self):
        return self._voltaje
