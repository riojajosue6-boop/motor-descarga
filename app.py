from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/descargar', methods=['GET'])
def descargar():
    url_video = request.args.get('url')
    tipo = request.args.get('tipo') # Recibe 'mp4' o 'mp3'
    
    if not url_video:
        return jsonify({"error": "Falta la URL del video"}), 400

    # CONFIGURACIÓN PROFESIONAL DE RAPIDAPI
    api_url = "https://social-all-in-one.p.rapidapi.com/v1/social/autolink"
    
    # IMPORTANTE: Reemplaza 'TU_LLAVE_DE_RAPIDAPI' con la clave que copiaste de RapidAPI
    headers = {
        "x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed14058", 
        "x-rapidapi-host": "social-all-in-one.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    
    payload = { "url": url_video }

    try:
        # Petición a la API de Social All In One
        response = requests.post(api_url, json=payload, headers=headers, timeout=15)
        
        # Si la API responde correctamente
        if response.status_code == 200:
            data = response.json()
            
            if "result" in data and len(data["result"]) > 0:
                links = data["result"]
                enlace_final = None

                if tipo == 'mp3':
                    # Buscamos la mejor opción de audio disponible
                    enlace_final = next((l['url'] for l in links if l.get('type') == 'audio' or 'mp3' in l.get('extension', '')), links[0]['url'])
                else:
                    # Buscamos video en formato MP4
                    # Intentamos priorizar alta calidad (720p o 1080p si la API lo entrega)
                    video_links = [l for l in links if l.get('type') == 'video' and l.get('extension') == 'mp4']
                    if video_links:
                        # Ordenamos por calidad de mayor a menor
                        video_links.sort(key=lambda x: int(x.get('quality', '0').replace('p', '') or 0), reverse=True)
                        enlace_final = video_links[0]['url']
                    else:
                        enlace_final = links[0]['url']

                return jsonify({"download_url": enlace_final})
            
            return jsonify({"error": "No se encontraron enlaces para este video."}), 404
        
        else:
            # Captura errores de límite de cuota o problemas de la API
            return jsonify({"error": f"Error de API: {response.status_code}"}), response.status_code

    except Exception as e:
        # Error interno del servidor
        return jsonify({"error": f"Error en el servidor: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
