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

    # NUEVA URL DE LA API QUE COMPRASTE
    api_url = "https://auto-download-all-in-one.p.rapidapi.com/v1/social/autolink"
    
    # TUS DATOS REALES DE RAPIDAPI
    headers = {
        "x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585", 
        "x-rapidapi-host": "auto-download-all-in-one.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    
    payload = { "url": url_video }

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            # Analizamos la respuesta de esta API específica
            if "result" in data and len(data["result"]) > 0:
                links = data["result"]
                
                # Intentamos buscar el formato que pidió el usuario
                if tipo == 'mp3':
                    # Buscamos algo que diga audio o mp3
                    enlace = next((l['url'] for l in links if l.get('type') == 'audio' or 'mp3' in l.get('extension', '')), links[0]['url'])
                else:
                    # Buscamos video mp4
                    enlace = next((l['url'] for l in links if l.get('extension') == 'mp4'), links[0]['url'])
                
                return jsonify({"download_url": enlace})
            
            return jsonify({"error": "No se encontraron enlaces"}), 404
        
        return jsonify({"error": f"Error de API: {response.status_code}"}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
