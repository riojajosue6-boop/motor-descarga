from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
# Configuramos CORS de forma abierta para evitar bloqueos
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return "Servidor del Descargador: ONLINE"

# Quitamos la barra final y forzamos que no sea estricto
@app.route('/descargar', methods=['GET', 'POST'], strict_slashes=False)
def descargar():
    url_video = request.args.get('url')
    tipo = request.args.get('tipo')
    
    if not url_video:
        return jsonify({"error": "Falta la URL en los parametros"}), 400

    api_url = "https://auto-download-all-in-one.p.rapidapi.com/v1/social/autolink"
    
    headers = {
        "x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585", 
        "x-rapidapi-host": "auto-download-all-in-one.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    
   # Limpiamos la URL para que sea solo el link base
    url_limpia = url_video.split('&')[0].split('?si=')[0]
    
    payload = { "url": url_limpia }

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=20)
        data = response.json()
        
        links = data.get("result", [])
        if links:
            # Busqueda robusta del enlace
            enlace = links[0]['url'] # Por defecto el primero
            for l in links:
                if tipo == 'mp3' and (l.get('type') == 'audio' or 'mp3' in l.get('extension', '')):
                    enlace = l['url']
                    break
                if tipo == 'mp4' and l.get('extension') == 'mp4':
                    enlace = l['url']
                    break
            
            return jsonify({"download_url": enlace})
        
        return jsonify({"error": "API no encontro enlaces"}), 404
    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

if __name__ == '__main__':
    app.run()
