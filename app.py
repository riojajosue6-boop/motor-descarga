from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging

app = Flask(__name__)
CORS(app)

# Esto nos ayudará a ver errores detallados en los Logs de Render
logging.basicConfig(level=logging.INFO)

@app.route('/descargar', methods=['GET'])
def descargar():
    url_video = request.args.get('url')
    tipo = request.args.get('tipo')
    
    if not url_video:
        return jsonify({"error": "Falta la URL"}), 400

    app.logger.info(f"Procesando URL: {url_video} para tipo: {tipo}")

    # Nueva URL de la API de Cobalt y configuración más compatible
    api_url = "https://api.cobalt.tools/api/json"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Configuración optimizada
    payload = {
        "url": url_video,
        "videoQuality": "720",
        "downloadMode": "audio" if tipo == 'mp3' else "video",
        "filenameStyle": "pretty"
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        
        # Si la API de Cobalt nos da error, lo capturamos aquí
        if response.status_code != 200:
            app.logger.error(f"Error de Cobalt: {response.text}")
            return jsonify({"error": "La API externa está saturada, intenta en un momento"}), 502
            
        data = response.json()
        
        if "url" in data:
            return jsonify({"download_url": data["url"]})
        else:
            return jsonify({"error": "No se encontró el enlace de descarga en la respuesta"}), 500
            
    except Exception as e:
        app.logger.error(f"Error interno: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
