"""
Controlador principal para la aplicación de delivery con grafos.
"""

import sys
import os

# Agregar el directorio raíz al path para importar Grafos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Grafos import Graph


class HomeController:
    """Controlador para la página principal del delivery."""
    
    def __init__(self):
        """Inicializa el controlador con un grafo predefinido."""
        self.graph = Graph(directed=False)
        self._initialize_sample_graph()
    
    def _initialize_sample_graph(self):
        """Inicializa un grafo de ejemplo para demostración."""
        # Agregar nodos (lugares en la ciudad)
        locations = [
            "Casa", "Pizzería", "Oficina", "Parque", "Escuela", 
            "Hospital", "Centro", "Mercado", "Estadio", "Universidad"
        ]
        
        for location in locations:
            self.graph.add_node(location)
        
        # Agregar conexiones (calles con distancias)
        connections = [
            ("Casa", "Pizzería", 3),
            ("Casa", "Oficina", 5),
            ("Casa", "Parque", 2),
            ("Pizzería", "Centro", 4),
            ("Pizzería", "Mercado", 3),
            ("Oficina", "Escuela", 6),
            ("Oficina", "Hospital", 4),
            ("Parque", "Escuela", 3),
            ("Parque", "Estadio", 5),
            ("Centro", "Hospital", 2),
            ("Centro", "Universidad", 7),
            ("Mercado", "Universidad", 4),
            ("Escuela", "Estadio", 3),
            ("Hospital", "Universidad", 5),
            ("Estadio", "Universidad", 6)
        ]
        
        for node1, node2, weight in connections:
            self.graph.add_edge(node1, node2, weight)
    
    def get_available_nodes(self):
        """Retorna la lista de nodos disponibles."""
        return self.graph.nodes
    
    def calculate_delivery_route(self, origin, start, end):
        """
        Calcula la ruta de delivery: origen → inicio → fin.
        
        Args:
            origin (str): Punto de origen
            start (str): Punto de recojo (pizzería)
            end (str): Punto de entrega (cliente)
            
        Returns:
            dict: Resultado del cálculo
        """
        return self.graph.shortest_path_three_points(origin, start, end)


# Instancia global del controlador
controller = HomeController()