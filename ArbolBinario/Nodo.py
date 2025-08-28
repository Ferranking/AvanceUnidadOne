"""
Módulo que define la clase Nodo para un árbol binario.

Este módulo proporciona la estructura básica de un nodo con valor
y referencias a sus hijos izquierdo y derecho.
"""


class Nodo:
    """
    Representa un nodo en un árbol binario.
    
    Un nodo contiene un valor y referencias a sus subárboles
    izquierdo y derecho.
    
    Attributes:
        valor: Dato almacenado en el nodo
        hijo_izquierdo: Referencia al nodo hijo izquierdo
        hijo_derecho: Referencia al nodo hijo derecho
    """
    
    def __init__(self, valor):
        """
        Inicializa un nuevo nodo con el valor especificado.
        
        Args:
            valor: El valor a almacenar en el nodo.
            
        Example:
            >>> nodo = Nodo(10)
            >>> nodo.get_valor()
            10
        """
        self.valor = valor
        self.hijo_izquierdo = None
        self.hijo_derecho = None
        
    def get_hijo_izquierdo(self):
        """
        Obtiene el nodo hijo izquierdo.
        
        Returns:
            Nodo: El nodo hijo izquierdo o None si no existe.
            
        Example:
            >>> nodo = Nodo(10)
            >>> nodo.get_hijo_izquierdo() is None
            True
        """
        return self.hijo_izquierdo
    
    def get_hijo_derecho(self):
        """
        Obtiene el nodo hijo derecho.
        
        Returns:
            Nodo: El nodo hijo derecho o None si no existe.
        """
        return self.hijo_derecho
    
    def set_hijo_izquierdo(self, nodo):
        """
        Establece el nodo hijo izquierdo.
        
        Args:
            nodo: Instancia de Nodo a establecer como hijo izquierdo.
            
        Example:
            >>> padre = Nodo(10)
            >>> hijo = Nodo(5)
            >>> padre.set_hijo_izquierdo(hijo)
            >>> padre.get_hijo_izquierdo().get_valor()
            5
        """
        self.hijo_izquierdo = nodo
    
    def set_hijo_derecho(self, nodo):
        """
        Establece el nodo hijo derecho.
        
        Args:
            nodo: Instancia de Nodo a establecer como hijo derecho.
            
        Raises:
            TypeError: Si el argumento no es una instancia de Nodo o None.
        """
        if nodo is not None and not isinstance(nodo, Nodo):
            raise TypeError("El argumento debe ser una instancia de Nodo o None")
        self.hijo_derecho = nodo
    
    def get_valor(self):
        """
        Obtiene el valor almacenado en el nodo.
        
        Returns:
            any: El valor almacenado en el nodo.
        """
        return self.valor
    
    def set_valor(self, valor):
        """
        Establece un nuevo valor para el nodo.
        
        Args:
            valor: Nuevo valor a almacenar en el nodo.
        """
        self.valor = valor
    
    def es_hoja(self):
        """
        Verifica si el nodo es una hoja (no tiene hijos).
        
        Returns:
            bool: True si el nodo es hoja, False en caso contrario.
            
        Example:
            >>> nodo = Nodo(10)
            >>> nodo.es_hoja()
            True
        """
        return self.hijo_izquierdo is None and self.hijo_derecho is None
    
    def __str__(self):
        """
        Representación en string del nodo.
        
        Returns:
            str: Representación del nodo con su valor.
        """
        return f"Nodo({self.valor})"
    
    def __repr__(self):
        """
        Representación oficial del nodo para debugging.
        
        Returns:
            str: Representación detallada del nodo.
        """
        return (f"Nodo(valor={self.valor}, "
                f"hijo_izquierdo={self.hijo_izquierdo}, "
                f"hijo_derecho={self.hijo_derecho})")


# Ejemplo de uso y pruebas
if __name__ == "__main__":
    # Crear nodos de ejemplo
    raiz = Nodo(10)
    hijo_izq = Nodo(5)
    hijo_der = Nodo(15)
    
    # Establecer relaciones
    raiz.set_hijo_izquierdo(hijo_izq)
    raiz.set_hijo_derecho(hijo_der)
    
    # Mostrar información
    print(f"Raiz: {raiz}")
    print(f"Hijo izquierdo: {raiz.get_hijo_izquierdo()}")
    print(f"Hijo derecho: {raiz.get_hijo_derecho()}")
    print(f"¿Es hoja la raiz?: {raiz.es_hoja()}")
    print(f"¿Es hoja el hijo izquierdo?: {hijo_izq.es_hoja()}")