from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "ONLINE"

# Esta configuracion acepta /descargar y /descargar/ por igual
@app.route('/descargar', methods=['GET'], strict_slashes=False)
@app.route('/descargar/', methods=['GET'], strict_slashes=False)
def descargar():
    # ... (todo el resto de tu codigo de descarga aqui abajo)
