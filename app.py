"""
Aplicación principal Flask para el sistema de delivery con grafos.
"""

from flask import Flask, render_template, request, jsonify
from controllers.home_controller import controller

app = Flask(__name__)


@app.route('/')
def index():
    """Página principal de la aplicación."""
    return render_template('index.html')


@app.route('/map')
def map_view():
    """Página con mapa interactivo."""
    return render_template('map_view.html')  # <- NUEVA RUTA AGREGADA


@app.route('/get_nodes')
def get_nodes():
    """Endpoint para obtener los nodos disponibles."""
    nodes = controller.get_available_nodes()
    return jsonify({'nodes': nodes})


@app.route('/calculate_route', methods=['POST'])
def calculate_route():
    """Endpoint para calcular la ruta de delivery."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se recibieron datos'
            })
        
        origin = data.get('origin', '').strip()
        start = data.get('start', '').strip()
        end = data.get('end', '').strip()
        
        if not origin or not start or not end:
            return jsonify({
                'success': False,
                'error': 'Todos los campos son requeridos'
            })
        
        # Calcular la ruta
        result = controller.calculate_delivery_route(origin, start, end)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}'
        })


@app.route('/graph_info')
def graph_info():
    """Endpoint para obtener información del grafo."""
    nodes = controller.get_available_nodes()
    edges = controller.graph.get_edges()
    
    return jsonify({
        'node_count': len(nodes),
        'edge_count': len(edges),
        'nodes': nodes,
        'edges': edges
    })


if __name__ == '__main__':
    print("🚀 Iniciando servidor de Delivery con Grafos...")
    print("📍 Vista Original: http://localhost:5000")
    print("🗺️ Vista Mapa: http://localhost:5000/map")  # <- NUEVO MENSAJE
    print("📊 Grafo cargado con:", len(controller.get_available_nodes()), "ubicaciones")
    app.run(debug=True, host='0.0.0.0', port=5000)