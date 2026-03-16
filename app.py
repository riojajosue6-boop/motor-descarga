from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/descargar', methods=['GET'])
def descargar():
    url_video = request.args.get('url')
    tipo = request.args.get('tipo') # 'mp4' o 'mp3'
    
    if not url_video:
        return jsonify({"error": "URL no proporcionada"}), 400

    # Usamos la API de Cobalt que es muy buena saltando bloqueos
    api_url = "https://api.cobalt.tools/api/json"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Configuramos lo que queremos pedir
    payload = {
        "url": url_video,
        "vCodec": "h264", # Formato estándar compatible
        "vQuality": "720", # Calidad HD
        "isAudioOnly": True if tipo == 'mp3' else False
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        data = response.json()
        
        if "url" in data:
            # En lugar de descargar el archivo al servidor, 
            # le devolvemos al usuario el link directo de descarga.
            return jsonify({"download_url": data["url"]})
        else:
            return jsonify({"error": "No se pudo obtener el link de descarga"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
