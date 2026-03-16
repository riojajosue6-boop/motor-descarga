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
        return jsonify({"error": "Falta la URL"}), 400

    # LIMPIEZA DE URL: Eliminamos rastreadores y parámetros extra
    # Ejemplo: transforma https://youtu.be/qrO4...si=123 en https://youtu.be/qrO4...
    url_video = url_video.split('?')[0]

    api_url = "https://auto-download-all-in-one.p.rapidapi.com/v1/social/autolink"
    
    headers = {
        "x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585", 
        "x-rapidapi-host": "auto-download-all-in-one.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    
    payload = { "url": url_video }

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            
            # Verificamos si existe la lista de resultados
            links = data.get("result", [])
            
            if links:
                enlace_final = None
                
                if tipo == 'mp3':
                    # Buscamos audio o mp3
                    enlace_final = next((l['url'] for l in links if l.get('type') == 'audio' or 'mp3' in l.get('extension', '')), links[0]['url'])
                else:
                    # Buscamos video mp4 o simplemente el primer video disponible
                    enlace_final = next((l['url'] for l in links if l.get('extension') == 'mp4'), links[0]['url'])
                
                return jsonify({"download_url": enlace_final})
            
            return jsonify({"error": "La API no devolvió enlaces para este video."}), 404
        
        # Si la API devuelve 404 o 403 directamente
        return jsonify({"error": f"Error de la API externa: {response.status_code}"}), response.status_code

    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
