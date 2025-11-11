"""
Implementación de un grafo con matriz de adyacencia y lista de adyacencia.
Incluye algoritmos BFS, DFS y Dijkstra.
Cumple con PEP8 y principios de POO.
"""

from collections import deque
import heapq


class Graph:
    """
    Clase que representa un grafo con implementación de matriz de adyacencia
    y lista de adyacencia.
    """

    def __init__(self, directed=False):
        """
        Inicializa un grafo.

        Args:
            directed (bool): True si es dirigido, False si es no dirigido
        """
        self._nodes = {}  # Diccionario: nombre_nodo -> índice
        self._nodes_list = []  # Lista: índice -> nombre_nodo
        self._adjacency_matrix = []  # Matriz de adyacencia
        self._adjacency_list = {}  # Lista de adyacencia
        self._directed = directed
        self._node_count = 0

    # ===== PROPIEDADES =====

    @property
    def directed(self):
        """Retorna si el grafo es dirigido."""
        return self._directed

    @property
    def node_count(self):
        """Retorna el número de nodos en el grafo."""
        return self._node_count

    @property
    def nodes(self):
        """Retorna la lista de nodos (solo lectura)."""
        return self._nodes_list.copy()

    # ===== MÉTODOS PARA NODOS =====

    def add_node(self, node_name):
        """
        Añade un nuevo nodo al grafo.

        Args:
            node_name: Identificador del nodo

        Returns:
            bool: True si se añadió, False si ya existía
        """
        if node_name in self._nodes:
            return False

        self._nodes[node_name] = self._node_count
        self._nodes_list.append(node_name)
        self._node_count += 1

        self._expand_adjacency_matrix()
        self._adjacency_list[node_name] = []

        return True

    def remove_node(self, node_name):
        """
        Elimina un nodo del grafo.

        Args:
            node_name: Identificador del nodo a eliminar

        Returns:
            bool: True si se eliminó, False si no existía
        """
        if node_name not in self._nodes:
            return False

        node_index = self._nodes[node_name]

        # Remover de estructuras de datos
        self._remove_from_dictionaries(node_name, node_index)
        self._remove_from_adjacency_matrix(node_index)
        self._remove_from_adjacency_list(node_name)

        self._node_count -= 1
        return True

    def _expand_adjacency_matrix(self):
        """Expande la matriz de adyacencia para el nuevo nodo."""
        for row in self._adjacency_matrix:
            row.append(0)
        self._adjacency_matrix.append([0] * self._node_count)

    def _remove_from_dictionaries(self, node_name, node_index):
        """Remueve un nodo de los diccionarios y actualiza índices."""
        del self._nodes[node_name]
        self._nodes_list.pop(node_index)

        # Actualizar índices de los nodos restantes
        for i, node in enumerate(self._nodes_list):
            self._nodes[node] = i

    def _remove_from_adjacency_matrix(self, node_index):
        """Remueve un nodo de la matriz de adyacencia."""
        self._adjacency_matrix.pop(node_index)
        for row in self._adjacency_matrix:
            row.pop(node_index)

    def _remove_from_adjacency_list(self, node_name):
        """Remueve un nodo de la lista de adyacencia."""
        del self._adjacency_list[node_name]
        for node in self._adjacency_list:
            self._adjacency_list[node] = [
                neighbor for neighbor in self._adjacency_list[node]
                if neighbor[0] != node_name
            ]

    # ===== MÉTODOS PARA ARISTAS =====

    def add_edge(self, node1, node2, weight=1):
        """
        Añade una arista entre dos nodos.

        Args:
            node1: Primer nodo
            node2: Segundo nodo
            weight: Peso de la arista (default 1)

        Returns:
            bool: True si se añadió, False si algún nodo no existe
        """
        if not self._validate_nodes(node1, node2):
            return False

        idx1, idx2 = self._nodes[node1], self._nodes[node2]

        self._update_adjacency_matrix(idx1, idx2, weight)
        self._update_adjacency_list(node1, node2, weight)

        return True

    def remove_edge(self, node1, node2):
        """
        Elimina una arista entre dos nodos.

        Args:
            node1: Primer nodo
            node2: Segundo nodo

        Returns:
            bool: True si se eliminó, False si algún nodo no existe
        """
        if not self._validate_nodes(node1, node2):
            return False

        idx1, idx2 = self._nodes[node1], self._nodes[node2]

        self._update_adjacency_matrix(idx1, idx2, 0)
        self._remove_from_adjacency_list_edge(node1, node2)

        return True

    def _validate_nodes(self, node1, node2):
        """Valida que ambos nodos existan en el grafo."""
        return node1 in self._nodes and node2 in self._nodes

    def _update_adjacency_matrix(self, idx1, idx2, weight):
        """Actualiza la matriz de adyacencia."""
        self._adjacency_matrix[idx1][idx2] = weight
        if not self._directed:
            self._adjacency_matrix[idx2][idx1] = weight

    def _update_adjacency_list(self, node1, node2, weight):
        """Actualiza la lista de adyacencia al añadir una arista."""
        if not self._has_edge_in_list(node1, node2):
            self._adjacency_list[node1].append((node2, weight))

        if not self._directed and not self._has_edge_in_list(node2, node1):
            self._adjacency_list[node2].append((node1, weight))

    def _has_edge_in_list(self, node1, node2):
        """Verifica si existe una arista en la lista de adyacencia."""
        return any(neighbor[0] == node2 for neighbor in self._adjacency_list[node1])

    def _remove_from_adjacency_list_edge(self, node1, node2):
        """Remueve una arista de la lista de adyacencia."""
        self._adjacency_list[node1] = [
            neighbor for neighbor in self._adjacency_list[node1]
            if neighbor[0] != node2
        ]

        if not self._directed:
            self._adjacency_list[node2] = [
                neighbor for neighbor in self._adjacency_list[node2]
                if neighbor[0] != node1
            ]

    # ===== GETTERS =====

    def get_edges(self):
        """
        Retorna la lista de todas las aristas.

        Returns:
            list: Lista de tuplas (nodo1, nodo2, peso)
        """
        edges = []
        for node1 in self._adjacency_list:
            for node2, weight in self._adjacency_list[node1]:
                if self._directed or node1 < node2:  # Evitar duplicados
                    edges.append((node1, node2, weight))
        return edges

    def get_adjacency_matrix(self):
        """
        Retorna la matriz de adyacencia.

        Returns:
            list: Matriz de adyacencia
        """
        return [row.copy() for row in self._adjacency_matrix]

    def get_adjacency_list(self):
        """
        Retorna la lista de adyacencia.

        Returns:
            dict: Lista de adyacencia
        """
        return {
            node: neighbors.copy()
            for node, neighbors in self._adjacency_list.items()
        }

    def get_neighbors(self, node_name):
        """
        Retorna los vecinos de un nodo.

        Args:
            node_name: Nombre del nodo

        Returns:
            list: Lista de tuplas (vecino, peso)
        """
        if node_name not in self._adjacency_list:
            return []
        return self._adjacency_list[node_name].copy()

    def get_degree(self, node_name):
        """
        Retorna el grado de un nodo.

        Args:
            node_name: Nombre del nodo

        Returns:
            int: Grado del nodo
        """
        if node_name not in self._adjacency_list:
            return 0
        return len(self._adjacency_list[node_name])

    def has_edge(self, node1, node2):
        """
        Verifica si existe una arista entre dos nodos.

        Args:
            node1: Primer nodo
            node2: Segundo nodo

        Returns:
            bool: True si existe la arista
        """
        if not self._validate_nodes(node1, node2):
            return False

        idx1, idx2 = self._nodes[node1], self._nodes[node2]
        return self._adjacency_matrix[idx1][idx2] != 0

    def get_edge_weight(self, node1, node2):
        """
        Retorna el peso de una arista.

        Args:
            node1: Primer nodo
            node2: Segundo nodo

        Returns:
            float or None: Peso de la arista o None si no existe
        """
        if not self._validate_nodes(node1, node2):
            return None

        idx1, idx2 = self._nodes[node1], self._nodes[node2]
        return self._adjacency_matrix[idx1][idx2]

    # ===== SETTERS =====

    def set_directed(self, directed):
        """
        Establece si el grafo es dirigido o no.

        Args:
            directed (bool): True para dirigido, False para no dirigido
        """
        self._directed = directed
        self._rebuild_representations()

    def set_edge_weight(self, node1, node2, weight):
        """
        Establece el peso de una arista.

        Args:
            node1: Primer nodo
            node2: Segundo nodo
            weight: Nuevo peso

        Returns:
            bool: True si se actualizó, False si la arista no existe
        """
        if not self._validate_nodes(node1, node2):
            return False

        idx1, idx2 = self._nodes[node1], self._nodes[node2]

        # Actualizar matriz de adyacencia
        self._adjacency_matrix[idx1][idx2] = weight
        if not self._directed:
            self._adjacency_matrix[idx2][idx1] = weight

        # Actualizar lista de adyacencia
        self._update_adjacency_list_weight(node1, node2, weight)
        if not self._directed:
            self._update_adjacency_list_weight(node2, node1, weight)

        return True

    def _update_adjacency_list_weight(self, node1, node2, weight):
        """Actualiza el peso de una arista en la lista de adyacencia."""
        for i, (neighbor, _) in enumerate(self._adjacency_list[node1]):
            if neighbor == node2:
                self._adjacency_list[node1][i] = (node2, weight)
                break

    # ===== ALGORITMOS DE BÚSQUEDA =====

    def bfs(self, start_node, target_node=None):
        """
        Realiza BFS (Breadth-First Search) desde un nodo inicial.

        Args:
            start_node: Nodo desde donde comenzar la búsqueda
            target_node: Nodo objetivo (opcional). Si se especifica,
                        la búsqueda se detiene cuando se encuentra.

        Returns:
            dict or list: Si no hay target, retorna el orden de visita.
                         Si hay target, retorna el camino más corto o None.
        """
        if start_node not in self._nodes:
            return None if target_node else []

        if target_node and target_node not in self._nodes:
            return None

        visited = set()
        queue = deque([start_node])
        visited.add(start_node)
        
        # Para reconstruir caminos
        parent = {start_node: None}
        
        # Para retornar orden de visita si no hay target
        visit_order = []

        while queue:
            current = queue.popleft()
            visit_order.append(current)

            # Si encontramos el target, reconstruimos el camino
            if target_node and current == target_node:
                path = []
                while current is not None:
                    path.append(current)
                    current = parent[current]
                return path[::-1]  # Invertir para obtener inicio->fin

            # Explorar vecinos
            for neighbor, _ in self._adjacency_list.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

        return visit_order if not target_node else None

    def dfs(self, start_node, target_node=None):
        """
        Realiza DFS (Depth-First Search) desde un nodo inicial.

        Args:
            start_node: Nodo desde donde comenzar la búsqueda
            target_node: Nodo objetivo (opcional). Si se especifica,
                        la búsqueda se detiene cuando se encuentra.

        Returns:
            dict or list: Si no hay target, retorna el orden de visita.
                         Si hay target, retorna el camino o None.
        """
        if start_node not in self._nodes:
            return None if target_node else []

        if target_node and target_node not in self._nodes:
            return None

        visited = set()
        stack = [start_node]
        parent = {start_node: None}
        visit_order = []

        while stack:
            current = stack.pop()

            if current not in visited:
                visited.add(current)
                visit_order.append(current)

                # Si encontramos el target, reconstruimos el camino
                if target_node and current == target_node:
                    path = []
                    while current is not None:
                        path.append(current)
                        current = parent[current]
                    return path[::-1]

                # Explorar vecinos en orden inverso para mantener orden natural
                neighbors = self._adjacency_list.get(current, [])
                for neighbor, _ in reversed(neighbors):
                    if neighbor not in visited:
                        stack.append(neighbor)
                        if neighbor not in parent:
                            parent[neighbor] = current

        return visit_order if not target_node else None

    def dfs_recursive(self, start_node, target_node=None):
        """
        Versión recursiva de DFS.

        Args:
            start_node: Nodo desde donde comenzar la búsqueda
            target_node: Nodo objetivo (opcional)

        Returns:
            list: Orden de visita o camino si se encuentra target
        """
        if start_node not in self._nodes:
            return None if target_node else []

        if target_node and target_node not in self._nodes:
            return None

        visited = set()
        visit_order = []
        path_found = None

        def _dfs_recursive(current, parent_node=None):
            nonlocal path_found

            if current in visited:
                return False

            visited.add(current)
            visit_order.append(current)

            # Verificar si encontramos el target
            if target_node and current == target_node:
                return True

            # Explorar vecinos
            for neighbor, _ in self._adjacency_list.get(current, []):
                if neighbor not in visited:
                    if _dfs_recursive(neighbor, current):
                        if path_found is None:
                            path_found = []
                        path_found.append(neighbor)
                        return True

            return False

        # Ejecutar DFS recursivo
        if target_node:
            if _dfs_recursive(start_node):
                path_found = path_found or []
                path_found.append(start_node)
                return path_found[::-1]
            else:
                return None
        else:
            _dfs_recursive(start_node)
            return visit_order

    # ===== ALGORITMO DIJKSTRA =====

    def dijkstra(self, start_node, target_node=None):
        """
        Implementa el algoritmo de Dijkstra para encontrar el camino más corto.

        Args:
            start_node: Nodo de inicio
            target_node: Nodo objetivo (opcional)

        Returns:
            dict or list: Distancias mínimas o camino más corto
        """
        if start_node not in self._nodes:
            return None if target_node else {}

        # Inicializar distancias
        distances = {node: float('inf') for node in self._nodes_list}
        distances[start_node] = 0
        
        # Cola de prioridad
        priority_queue = [(0, start_node)]
        
        # Para reconstruir caminos
        previous = {node: None for node in self._nodes_list}

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            # Si encontramos el target, reconstruimos el camino
            if target_node and current_node == target_node:
                path = []
                while current_node is not None:
                    path.append(current_node)
                    current_node = previous[current_node]
                return path[::-1]

            # Si la distancia actual es mayor que la almacenada, saltar
            if current_distance > distances[current_node]:
                continue

            # Explorar vecinos
            for neighbor, weight in self._adjacency_list.get(current_node, []):
                distance = current_distance + weight

                # Si encontramos un camino más corto
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances if not target_node else None

    def shortest_path_three_points(self, origin, start, end):
        """
        Encuentra el camino más corto que pasa por tres puntos: origen -> inicio -> fin.
        
        Args:
            origin: Punto de origen (ubicación actual)
            start: Punto de inicio/recojo (pizzería)
            end: Punto final/cliente
            
        Returns:
            dict: Información del camino completo
        """
        # Verificar que todos los nodos existan
        for node in [origin, start, end]:
            if node not in self._nodes:
                return {
                    'success': False,
                    'error': f'El nodo {node} no existe en el grafo'
                }

        # Calcular camino de origen a inicio
        path_origin_to_start = self.dijkstra(origin, start)
        if not path_origin_to_start:
            return {
                'success': False,
                'error': f'No hay camino desde {origin} a {start}'
            }

        # Calcular camino de inicio a fin
        path_start_to_end = self.dijkstra(start, end)
        if not path_start_to_end:
            return {
                'success': False,
                'error': f'No hay camino desde {start} a {end}'
            }

        # Combinar caminos (evitando duplicar el nodo start)
        full_path = path_origin_to_start + path_start_to_end[1:]
        
        # Calcular distancia total
        total_distance = 0
        for i in range(len(full_path) - 1):
            weight = self.get_edge_weight(full_path[i], full_path[i + 1])
            if weight is not None:
                total_distance += weight

        return {
            'success': True,
            'full_path': full_path,
            'path_origin_to_start': path_origin_to_start,
            'path_start_to_end': path_start_to_end,
            'total_distance': total_distance,
            'route_description': f"{origin} → {start} → {end}"
        }

    # ===== MÉTODOS AUXILIARES =====

    def _rebuild_representations(self):
        """Reconstruye las representaciones del grafo."""
        self._adjacency_list = {}
        for node in self._nodes_list:
            self._adjacency_list[node] = []

        for i, node1 in enumerate(self._nodes_list):
            for j, node2 in enumerate(self._nodes_list):
                weight = self._adjacency_matrix[i][j]
                if weight != 0:
                    self._adjacency_list[node1].append((node2, weight))

    def __str__(self):
        """
        Representación en string del grafo.

        Returns:
            str: Representación del grafo
        """
        result = f"Grafo {'Dirigido' if self._directed else 'No Dirigido'}\n"
        result += f"Nodos: {self.nodes}\n"
        result += f"Número de nodos: {self._node_count}\n"
        result += "Aristas:\n"
        for edge in self.get_edges():
            result += f"  {edge[0]} --{edge[2]}--> {edge[1]}\n"
        return result

    def print_adjacency_matrix(self):
        """Imprime la matriz de adyacencia de forma formateada."""
        print("Matriz de Adyacencia:")
        print("   ", end="")
        for node in self._nodes_list:
            print(f"{node:>4}", end="")
        print()

        for i, node in enumerate(self._nodes_list):
            print(f"{node}: ", end="")
            for weight in self._adjacency_matrix[i]:
                print(f"{weight:>4}", end="")
            print()

    def print_adjacency_list(self):
        """Imprime la lista de adyacencia de forma formateada."""
        print("Lista de Adyacencia:")
        for node in sorted(self._nodes_list):
            neighbors = self._adjacency_list.get(node, [])
            neighbor_str = ", ".join([f"({n}, {w})" for n, w in neighbors])
            print(f"  {node}: [{neighbor_str}]")


# ===== EJEMPLO DE USO =====
def main():
    """Función principal con ejemplos de uso."""
    # Crear un grafo no dirigido
    grafo = Graph(directed=False)

    # Añadir nodos
    grafo.add_node("A")
    grafo.add_node("B")
    grafo.add_node("C")
    grafo.add_node("D")
    grafo.add_node("E")
    grafo.add_node("F")

    # Añadir aristas
    grafo.add_edge("A", "B", 2)
    grafo.add_edge("A", "C", 1)
    grafo.add_edge("B", "D", 3)
    grafo.add_edge("C", "E", 4)
    grafo.add_edge("D", "F", 5)
    grafo.add_edge("E", "F", 6)

    # Mostrar información del grafo
    print(grafo)

    # Probar el nuevo algoritmo de tres puntos
    print("=" * 50)
    print("PRUEBA DEL ALGORITMO DE TRES PUNTOS")
    print("=" * 50)
    
    result = grafo.shortest_path_three_points("A", "C", "F")
    print("Camino de A (origen) → C (recojo) → F (cliente):")
    print(f"Éxito: {result['success']}")
    if result['success']:
        print(f"Camino completo: {' → '.join(result['full_path'])}")
        print(f"Descripción: {result['route_description']}")
        print(f"Distancia total: {result['total_distance']}")
        print(f"Origen → Recojo: {' → '.join(result['path_origin_to_start'])}")
        print(f"Recojo → Cliente: {' → '.join(result['path_start_to_end'])}")


if __name__ == "__main__":
    main()