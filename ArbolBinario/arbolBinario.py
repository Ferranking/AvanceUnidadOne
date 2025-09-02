"""
Módulo que implementa un árbol binario con versiones recursivas e iterativas.
"""

from collections import deque
from Nodo import Nodo


class ArbolBinario:
    def __init__(self):
        self.raiz = None

    # OPERACIONES BÁSICAS
    def es_vacio(self):
        """Versión iterativa (aunque es tan simple que no hay diferencia)"""
        return self.raiz is None

    # INSERTAR - Ambas versiones
    def insertar_nodo_recursivo(self, valor):
        """Versión recursiva de inserción"""
        self.raiz = self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo_actual, valor):
        if nodo_actual is None:
            return Nodo(valor)
        
        if valor < nodo_actual.get_valor():
            nodo_actual.set_hijo_izquierdo(
                self._insertar_recursivo(nodo_actual.get_hijo_izquierdo(), valor)
            )
        else:
            nodo_actual.set_hijo_derecho(
                self._insertar_recursivo(nodo_actual.get_hijo_derecho(), valor)
            )
        return nodo_actual

    def insertar_nodo_iterativo(self, valor):
        """Versión iterativa de inserción"""
        nuevo_nodo = Nodo(valor)
        
        if self.es_vacio():
            self.raiz = nuevo_nodo
            return
            
        actual = self.raiz
        padre = None
        
        while actual is not None:
            padre = actual
            if valor < actual.get_valor():
                actual = actual.get_hijo_izquierdo()
            else:
                actual = actual.get_hijo_derecho()
        
        if valor < padre.get_valor():
            padre.set_hijo_izquierdo(nuevo_nodo)
        else:
            padre.set_hijo_derecho(nuevo_nodo)

    # BUSCAR - Ambas versiones
    def buscar_x_recursivo(self, valor):
        """Versión recursiva de búsqueda"""
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, nodo_actual, valor):
        if nodo_actual is None:
            return False
            
        if valor == nodo_actual.get_valor():
            return True
            
        if valor < nodo_actual.get_valor():
            return self._buscar_recursivo(nodo_actual.get_hijo_izquierdo(), valor)
        else:
            return self._buscar_recursivo(nodo_actual.get_hijo_derecho(), valor)

    def buscar_x_iterativo(self, valor):
        """Versión iterativa de búsqueda"""
        actual = self.raiz
        
        while actual is not None:
            if valor == actual.get_valor():
                return True
            elif valor < actual.get_valor():
                actual = actual.get_hijo_izquierdo()
            else:
                actual = actual.get_hijo_derecho()
                
        return False

    # ES HOJA - Ambas versiones
    def es_hoja_recursivo(self, valor):
        """Versión recursiva para verificar si un nodo es hoja"""
        nodo = self._buscar_nodo_recursivo(self.raiz, valor)
        if nodo is None:
            return False
        return nodo.get_hijo_izquierdo() is None and nodo.get_hijo_derecho() is None

    def es_hoja_iterativo(self, valor):
        """Versión iterativa para verificar si un nodo es hoja"""
        nodo = self._buscar_nodo_iterativo(valor)
        if nodo is None:
            return False
        return nodo.get_hijo_izquierdo() is None and nodo.get_hijo_derecho() is None

    def _buscar_nodo_recursivo(self, nodo_actual, valor):
        """Búsqueda recursiva de nodo (retorna el nodo, no boolean)"""
        if nodo_actual is None:
            return None
            
        if valor == nodo_actual.get_valor():
            return nodo_actual
            
        if valor < nodo_actual.get_valor():
            return self._buscar_nodo_recursivo(nodo_actual.get_hijo_izquierdo(), valor)
        else:
            return self._buscar_nodo_recursivo(nodo_actual.get_hijo_derecho(), valor)

    def _buscar_nodo_iterativo(self, valor):
        """Búsqueda iterativa de nodo (retorna el nodo, no boolean)"""
        actual = self.raiz
        
        while actual is not None:
            if valor == actual.get_valor():
                return actual
            elif valor < actual.get_valor():
                actual = actual.get_hijo_izquierdo()
            else:
                actual = actual.get_hijo_derecho()
                
        return None

    # ALTURA - Ambas versiones
    def altura_recursivo(self):
        """Versión recursiva para calcular la altura del árbol"""
        return self._altura_recursivo(self.raiz)

    def _altura_recursivo(self, nodo_actual):
        if nodo_actual is None:
            return 0
        altura_izq = self._altura_recursivo(nodo_actual.get_hijo_izquierdo())
        altura_der = self._altura_recursivo(nodo_actual.get_hijo_derecho())
        return 1 + max(altura_izq, altura_der)

    def altura_iterativo(self):
        """Versión iterativa para calcular la altura del árbol usando BFS"""
        if self.es_vacio():
            return 0
            
        altura = 0
        cola = deque([self.raiz])
        
        while cola:
            nivel_size = len(cola)
            for _ in range(nivel_size):
                nodo_actual = cola.popleft()
                if nodo_actual.get_hijo_izquierdo() is not None:
                    cola.append(nodo_actual.get_hijo_izquierdo())
                if nodo_actual.get_hijo_derecho() is not None:
                    cola.append(nodo_actual.get_hijo_derecho())
            altura += 1
            
        return altura

    # CANTIDAD DE NODOS - Ambas versiones
    def cantidad_nodos_recursivo(self):
        """Versión recursiva para contar la cantidad de nodos"""
        return self._cantidad_nodos_recursivo(self.raiz)

    def _cantidad_nodos_recursivo(self, nodo_actual):
        if nodo_actual is None:
            return 0
        return (1 + 
                self._cantidad_nodos_recursivo(nodo_actual.get_hijo_izquierdo()) + 
                self._cantidad_nodos_recursivo(nodo_actual.get_hijo_derecho()))

    def cantidad_nodos_iterativo(self):
        """Versión iterativa para contar la cantidad de nodos usando BFS"""
        if self.es_vacio():
            return 0
            
        contador = 0
        cola = deque([self.raiz])
        
        while cola:
            nodo_actual = cola.popleft()
            contador += 1
            
            if nodo_actual.get_hijo_izquierdo() is not None:
                cola.append(nodo_actual.get_hijo_izquierdo())
            if nodo_actual.get_hijo_derecho() is not None:
                cola.append(nodo_actual.get_hijo_derecho())
                
        return contador

    # AMPLITUD (Recorrido por niveles) - Versión iterativa
    def amplitud(self):
        """Recorrido por niveles (BFS) - Solo versión iterativa"""
        if self.es_vacio():
            return []
            
        resultado = []
        cola = deque([self.raiz])
        
        while cola:
            nodo_actual = cola.popleft()
            resultado.append(nodo_actual.get_valor())
            
            if nodo_actual.get_hijo_izquierdo() is not None:
                cola.append(nodo_actual.get_hijo_izquierdo())
            if nodo_actual.get_hijo_derecho() is not None:
                cola.append(nodo_actual.get_hijo_derecho())
                
        return resultado

    # RECORRIDOS - Ambas versiones
    # IN-ORDEN
    def in_orden_recursivo(self):
        """Recorrido in-orden recursivo"""
        resultado = []
        self._in_orden_recursivo(self.raiz, resultado)
        return resultado

    def _in_orden_recursivo(self, nodo_actual, resultado):
        if nodo_actual is not None:
            self._in_orden_recursivo(nodo_actual.get_hijo_izquierdo(), resultado)
            resultado.append(nodo_actual.get_valor())
            self._in_orden_recursivo(nodo_actual.get_hijo_derecho(), resultado)

    def in_orden_iterativo(self):
        """Recorrido in-orden iterativo usando pila"""
        resultado = []
        pila = []
        actual = self.raiz
        
        while actual is not None or pila:
            # Ir lo más a la izquierda posible
            while actual is not None:
                pila.append(actual)
                actual = actual.get_hijo_izquierdo()
            
            # Procesar el nodo
            actual = pila.pop()
            resultado.append(actual.get_valor())
            
            # Mover al subárbol derecho
            actual = actual.get_hijo_derecho()
            
        return resultado

    # PRE-ORDEN
    def pre_orden_recursivo(self):
        """Recorrido pre-orden recursivo"""
        resultado = []
        self._pre_orden_recursivo(self.raiz, resultado)
        return resultado

    def _pre_orden_recursivo(self, nodo_actual, resultado):
        if nodo_actual is not None:
            resultado.append(nodo_actual.get_valor())
            self._pre_orden_recursivo(nodo_actual.get_hijo_izquierdo(), resultado)
            self._pre_orden_recursivo(nodo_actual.get_hijo_derecho(), resultado)

    def pre_orden_iterativo(self):
        """Recorrido pre-orden iterativo usando pila"""
        if self.es_vacio():
            return []
            
        resultado = []
        pila = [self.raiz]
        
        while pila:
            actual = pila.pop()
            resultado.append(actual.get_valor())
            
            # Apilar primero derecho, luego izquierdo (para procesar izquierdo primero)
            if actual.get_hijo_derecho() is not None:
                pila.append(actual.get_hijo_derecho())
            if actual.get_hijo_izquierdo() is not None:
                pila.append(actual.get_hijo_izquierdo())
                
        return resultado

    # POST-ORDEN
    def post_orden_recursivo(self):
        """Recorrido post-orden recursivo"""
        resultado = []
        self._post_orden_recursivo(self.raiz, resultado)
        return resultado

    def _post_orden_recursivo(self, nodo_actual, resultado):
        if nodo_actual is not None:
            self._post_orden_recursivo(nodo_actual.get_hijo_izquierdo(), resultado)
            self._post_orden_recursivo(nodo_actual.get_hijo_derecho(), resultado)
            resultado.append(nodo_actual.get_valor())

    def post_orden_iterativo(self):
        """Recorrido post-orden iterativo usando dos pilas"""
        if self.es_vacio():
            return []
            
        pila1 = [self.raiz]
        pila2 = []
        resultado = []
        
        while pila1:
            actual = pila1.pop()
            pila2.append(actual)
            
            if actual.get_hijo_izquierdo() is not None:
                pila1.append(actual.get_hijo_izquierdo())
            if actual.get_hijo_derecho() is not None:
                pila1.append(actual.get_hijo_derecho())
        
        while pila2:
            resultado.append(pila2.pop().get_valor())
            
        return resultado

    # MÉTODOS DE CONVENIENCIA
    def insertar_nodo(self, valor, recursivo=True):
        """Método unificado de inserción"""
        if recursivo:
            self.insertar_nodo_recursivo(valor)
        else:
            self.insertar_nodo_iterativo(valor)

    def buscar_x(self, valor, recursivo=True):
        """Método unificado de búsqueda"""
        if recursivo:
            return self.buscar_x_recursivo(valor)
        else:
            return self.buscar_x_iterativo(valor)

    def es_hoja(self, valor, recursivo=True):
        """Método unificado para verificar si un nodo es hoja"""
        if recursivo:
            return self.es_hoja_recursivo(valor)
        else:
            return self.es_hoja_iterativo(valor)

    def altura(self, recursivo=True):
        """Método unificado para calcular la altura"""
        if recursivo:
            return self.altura_recursivo()
        else:
            return self.altura_iterativo()

    def cantidad_nodos(self, recursivo=True):
        """Método unificado para contar nodos"""
        if recursivo:
            return self.cantidad_nodos_recursivo()
        else:
            return self.cantidad_nodos_iterativo()

    def in_orden(self, recursivo=True):
        """Método unificado de in-orden"""
        if recursivo:
            return self.in_orden_recursivo()
        else:
            return self.in_orden_iterativo()

    def pre_orden(self, recursivo=True):
        """Método unificado de pre-orden"""
        if recursivo:
            return self.pre_orden_recursivo()
        else:
            return self.pre_orden_iterativo()

    def post_orden(self, recursivo=True):
        """Método unificado de post-orden"""
        if recursivo:
            return self.post_orden_recursivo()
        else:
            return self.post_orden_iterativo()