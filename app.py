from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Servidor del Descargador: ONLINE"

@app.route('/descargar', methods=['GET'], strict_slashes=False)
def descargar():
    url_video = request.args.get('url')
    tipo = request.args.get('tipo')
    
    if not url_video:
        return jsonify({"error": "Falta la URL"}), 400

    api_url = "https://auto-download-all-in-one.p.rapidapi.com/v1/social/autolink"
    
    headers = {
        "x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585", 
        "x-rapidapi-host": "auto-download-all-in-one.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    
    payload = { "url": url_video }

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=20)
        data = response.json()
        links = data.get("result", [])
        if links:
            enlace = next((l['url'] for l in links if (tipo == 'mp3' and (l.get('type') == 'audio' or 'mp3' in l.get('extension', ''))) or (tipo == 'mp4' and l.get('extension') == 'mp4')), links[0]['url'])
            return jsonify({"download_url": enlace})
        return jsonify({"error": "No se encontraron enlaces"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
