from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
# Permitimos que cualquier página (tu frontend) llame a este servidor
CORS(app)

# RUTA 1: Para verificar que el servidor está despierto
@app.route('/')
def home():
    return "Servidor del Descargador: ONLINE"

# RUTA 2: El motor de descarga (Acepta con y sin barra final)
@app.route('/descargar', methods=['GET'], strict_slashes=False)
@app.route('/descargar/', methods=['GET'], strict_slashes=False)
def descargar():
    # 1. Obtenemos los datos de la URL
    url_video = request.args.get('url')
    tipo = request.args.get('tipo', 'mp4') # Por defecto mp4
    
    if not url_video:
        return jsonify({"error": "Falta la URL en los parametros"}), 400

    # 2. Limpieza de URL (Elimina basura de rastreo de YouTube para que la API no falle)
    # Transforma: https://youtu.be/video?si=123 -> https://youtu.be/video
    url_limpia = url_video.split('?')[0].split('&')[0]

    # 3. Configuración de RapidAPI
    api_url = "https://auto-download-all-in-one.p.rapidapi.com/v1/social/autolink"
    
    headers = {
        "x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585", 
        "x-rapidapi-host": "auto-download-all-in-one.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    
    payload = { "url": url_limpia }

    try:
        # Llamada a la API externa
        response = requests.post(api_url, json=payload, headers=headers, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            links = data.get("result", [])
            
            if links:
                # Buscamos el mejor enlace según lo que pidió el usuario
                enlace_final = links[0]['url'] # Por defecto el primero
                
                for item in links:
                    ext = str(item.get('extension', '')).lower()
                    tipo_item = str(item.get('type', '')).lower()
                    
                    if tipo == 'mp3':
                        if 'mp3' in ext or tipo_item == 'audio':
                            enlace_final = item['url']
                            break
                    elif tipo == 'mp4':
                        if 'mp4' in ext:
                            enlace_final = item['url']
                            break
                
                return jsonify({"download_url": enlace_final})
            
            return jsonify({"error": "La API no encontró enlaces para este video"}), 404
        
        return jsonify({"error": f"Error de API externa: {response.status_code}"}), response.status_code

    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

# No es necesario app.run() para Gunicorn en Render
