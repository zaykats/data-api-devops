"""
API de Données Simple avec Flask
Démonstration DevOps sur Google Cloud Platform
"""

from flask import Flask, jsonify, request
from datetime import datetime
import os

app = Flask(__name__)

API_VERSION = "1.0.0"

# Variable d'environnement
ENVIRONMENT = os.getenv('ENV', 'development')