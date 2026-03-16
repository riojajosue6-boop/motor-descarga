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
        return jsonify({"error": "Falta la URL"}), 400

    # API de Cobalt (Gratis y sin tarjeta)
    api_url = "https://api.cobalt.tools/api/json"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    payload = {
        "url": url_video,
        "videoQuality": "720",
        "downloadMode": "audio" if tipo == 'mp3' else "video",
        "filenameStyle": "pretty",
        "isNoTTWatermark": True
    }

    try:
        # Intentamos la petición
        response = requests.post(api_url, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if "url" in data:
                return jsonify({"download_url": data["url"]})
            elif "text" in data: # A veces Cobalt devuelve el link en este campo
                return jsonify({"download_url": data["text"]})
        
        # Si Cobalt falla por saturación, intentamos un servidor alternativo de ellos
        return jsonify({"error": "El servidor está saturado. Intenta con otro video o espera 1 minuto."}), 503
            
    except Exception as e:
        return jsonify({"error": "Conexión lenta, reintenta ahora."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
