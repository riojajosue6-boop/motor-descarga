from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

# Forzamos a Flask a ser flexible con las rutas
app = Flask(__name__, static_folder='.')
CORS(app)

# 1. RUTA PRINCIPAL (Servir el HTML)
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# 2. RUTA DE DESCARGA (Blindada contra 404)
@app.route('/descargar', methods=['GET', 'POST'], strict_slashes=False)
def descargar():
    url_video = request.args.get('url')
    tipo = request.args.get('tipo', 'mp4')
    
    if not url_video:
        return jsonify({"error": "Falta la URL"}), 400

    # Limpiamos la URL de rastreadores (?si=...)
    url_limpia = url_video.split('?')[0].split('&')[0]

    api_url = "https://auto-download-all-in-one.p.rapidapi.com/v1/social/autolink"
    headers = {
        "x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585", 
        "x-rapidapi-host": "auto-download-all-in-one.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(api_url, json={"url": url_limpia}, headers=headers, timeout=20)
        data = response.json()
        links = data.get("result", [])
        
        if links:
            enlace = links[0]['url']
            for l in links:
                ext = str(l.get('extension', '')).lower()
                if tipo == 'mp3' and ('mp3' in ext or l.get('type') == 'audio'):
                    enlace = l['url']
                    break
                if tipo == 'mp4' and 'mp4' in ext:
                    enlace = l['url']
                    break
            return jsonify({"download_url": enlace})
        
        return jsonify({"error": "No se hallaron enlaces"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Esto ayuda a Render a encontrar el puerto correcto
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
