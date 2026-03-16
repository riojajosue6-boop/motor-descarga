from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/descargar', methods=['GET'])
def descargar():
    url_video = request.args.get('url')
    tipo = request.args.get('tipo')
    
    if not url_video:
        return jsonify({"error": "Falta URL"}), 400

    # Probaremos con una instancia alternativa de Cobalt que suele estar más libre
    # Si esta falla, probaremos otra en el siguiente paso
    instancias = [
        "https://api.cobalt.tools/api/json",
        "https://cobalt.api.unblocker.it/api/json" # Instancia de respaldo
    ]
    
    payload = {
        "url": url_video,
        "videoQuality": "720",
        "downloadMode": "audio" if tipo == 'mp3' else "video",
        "filenameStyle": "pretty"
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    for api_url in instancias:
        try:
            response = requests.post(api_url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return jsonify({"download_url": data.get("url") or data.get("text")})
        except:
            continue # Si una falla, intenta con la siguiente

    return jsonify({"error": "Todos los servidores gratuitos están llenos. Intenta en 5 minutos o consigue una API Key."}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
