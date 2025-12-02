"""
API de Données Simple avec Flask
Démonstration DevOps sur Google Cloud Platform
"""

from flask import Flask, jsonify, request
from datetime import datetime
import os

app = Flask(__name__)

# Version de l'API (à changer pour la démonstration)
API_VERSION = "2.0.0"

# Variable d'environnement
ENVIRONMENT = os.getenv('ENV', 'development')


@app.route('/')
def home():
    """Endpoint principal"""
    return jsonify({
        'message': 'Bienvenue sur notre API de données DevOps',
        'version': API_VERSION,
        'environment': ENVIRONMENT,
        'timestamp': datetime.now().isoformat(),
        'endpoints': {
            '/': 'Page d\'accueil',
            '/health': 'Vérification de santé',
            '/data': 'Récupération de données',
            '/stats': 'Statistiques de l\'API'
        }
    })


@app.route('/health')
def health():
    """Endpoint de santé pour le monitoring"""
    return jsonify({
        'status': 'healthy',
        'version': API_VERSION,
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/data')
def get_data():
    """Endpoint pour récupérer des données"""
    # Simuler des données
    sample_data = [
        {'id': 1, 'nom': 'Produit A', 'prix': 29.99, 'stock': 150},
        {'id': 2, 'nom': 'Produit B', 'prix': 49.99, 'stock': 75},
        {'id': 3, 'nom': 'Produit C', 'prix': 19.99, 'stock': 200},
        {'id': 4, 'nom': 'Produit D', 'prix': 99.99, 'stock': 30},
        {'id': 5, 'nom': 'Produit E', 'prix': 39.99, 'stock': 120}
    ]
    
    return jsonify({
        'status': 'success',
        'count': len(sample_data),
        'data': sample_data,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/data/<int:item_id>')
def get_data_by_id(item_id):
    """Endpoint pour récupérer un élément spécifique"""
    # Simuler des données
    sample_data = {
        1: {'id': 1, 'nom': 'Produit A', 'prix': 29.99, 'stock': 150},
        2: {'id': 2, 'nom': 'Produit B', 'prix': 49.99, 'stock': 75},
        3: {'id': 3, 'nom': 'Produit C', 'prix': 19.99, 'stock': 200},
        4: {'id': 4, 'nom': 'Produit D', 'prix': 99.99, 'stock': 30},
        5: {'id': 5, 'nom': 'Produit E', 'prix': 39.99, 'stock': 120}
    }
    
    if item_id in sample_data:
        return jsonify({
            'status': 'success',
            'data': sample_data[item_id],
            'timestamp': datetime.now().isoformat()
        })
    else:
        return jsonify({
            'status': 'error',
            'message': f'Produit avec ID {item_id} non trouvé',
            'timestamp': datetime.now().isoformat()
        }), 404


@app.route('/stats')
def get_stats():
    """Endpoint pour les statistiques"""
    return jsonify({
        'status': 'success',
        'stats': {
            'total_products': 5,
            'average_price': 47.99,
            'total_stock': 575,
            'api_version': API_VERSION,
            'environment': ENVIRONMENT
        },
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/v1/search')
def search():
    """Endpoint de recherche avec paramètres"""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({
            'status': 'error',
            'message': 'Paramètre de recherche "q" requis',
            'timestamp': datetime.now().isoformat()
        }), 400
    
    # Simuler une recherche simple
    all_products = [
        {'id': 1, 'nom': 'Produit A', 'prix': 29.99},
        {'id': 2, 'nom': 'Produit B', 'prix': 49.99},
        {'id': 3, 'nom': 'Produit C', 'prix': 19.99},
        {'id': 4, 'nom': 'Produit D', 'prix': 99.99},
        {'id': 5, 'nom': 'Produit E', 'prix': 39.99}
    ]
    
    results = [p for p in all_products if query.lower() in p['nom'].lower()]
    
    return jsonify({
        'status': 'success',
        'query': query,
        'count': len(results),
        'results': results,
        'timestamp': datetime.now().isoformat()
    })


@app.errorhandler(404)
def not_found(error):
    """Gestionnaire d'erreur 404"""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint non trouvé',
        'timestamp': datetime.now().isoformat()
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Gestionnaire d'erreur 500"""
    return jsonify({
        'status': 'error',
        'message': 'Erreur interne du serveur',
        'timestamp': datetime.now().isoformat()
    }), 500


if __name__ == '__main__':
    # Configuration pour le développement local
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)