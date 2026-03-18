import os
import requests
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- TU PÁGINA WEB INTEGRADA ---
HTML_DISENO = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Descargador Pro - Cochabamba</title>
    <style>
        body { background: #0f0f0f; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; padding: 40px; }
        .container { background: #1a1a1a; padding: 30px; border-radius: 20px; display: inline-block; border: 1px solid #333; max-width: 450px; width: 90%; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        h1 { color: #ff0000; margin-bottom: 10px; }
        input { width: 90%; padding: 12px; margin: 15px 0; border-radius: 8px; border: 1px solid #444; background: #2a2a2a; color: white; outline: none; }
        select { width: 95%; padding: 10px; margin-bottom: 15px; border-radius: 8px; background: #2a2a2a; color: white; border: 1px solid #444; }
        button { width: 95%; padding: 12px; background: #cc0000; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.3s; font-size: 16px; }
        button:hover { background: #ff0000; transform: scale(1.02); }
        #status { margin-top: 20px; font-size: 14px; color: #aaa; min-height: 40px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Motor de Descarga</h1>
        <p>Pega el enlace de YouTube o TikTok abajo:</p>
        <input type="text" id="urlInput" placeholder="https://www.youtube.com/watch?v=...">
        <select id="formatInput">
            <option value="mp4">Video MP4 (Alta Calidad)</option>
            <option value="mp3">Solo Audio MP3</option>
        </select>
        <button onclick="procesar()">DESCARGAR AHORA</button>
        <div id="status"></div>
    </div>

    <script>
        async function procesar() {
            const url = document.getElementById('urlInput').value;
            const tipo = document.getElementById('formatInput').value;
            const status = document.getElementById('status');

            if(!url) {
                status.innerText = "❌ Por favor, pega un enlace válido.";
                return;
            }
            
            status.innerText = "⏳ Procesando en el servidor... espera un momento.";

            try {
                // Llamada a la API interna de Flask
                const response = await fetch(`/api/descargar?url=${encodeURIComponent(url)}&tipo=${tipo}`);
                const data = await response.json();

                if(data.download_url) {
                    status.innerHTML = "✅ ¡Enlace generado con éxito!<br>Iniciando descarga...";
                    // Abrir el link en una pestaña nueva o descarga directa
                    window.location.href = data.download_url;
                } else {
                    status.innerText = "❌ Error: " + (data.error || "No se encontraron enlaces disponibles.");
                }
            } catch (e) {
                status.innerText = "❌ Error crítico: El servidor no responde.";
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    # Esta ruta carga el diseño visual automáticamente
    return render_template_string(HTML_DISENO)

@app.route('/api/descargar')
def api_proxy():
    video_url = request.args.get('url')
    formato = request.args.get('tipo', 'mp4')

    if not video_url:
        return jsonify({"error": "No se proporcionó una URL"}), 400

    # Limpiamos la URL de YouTube (quitamos parámetros extras de rastreo)
    if "youtube.com" in video_url or "youtu.be" in video_url:
        video_url = video_url.split('?')[0].split('&')[0]

    # CONFIGURACIÓN SEGÚN TU CURL DE RAPIDAPI
    api_endpoint = "https://auto-download-all-in-one.p.rapidapi.com/v1/social/autolink"
    api_headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "auto-download-all-in-one.p.rapidapi.com",
        "x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585"
    }
    payload = {"url": video_url}

    try:
        # Petición POST a RapidAPI
        response = requests.post(api_endpoint, json=payload, headers=api_headers, timeout=25)
        
        if response.status_code != 200:
            return jsonify({"error": "La API respondió con un error. Verifica tu suscripción."}), response.status_code
            
        data = response.json()
        links = data.get("result", [])
        
        if not links:
            return jsonify({"error": "No se encontraron enlaces para este video específico."}), 404

        # Lógica para elegir el formato correcto
        enlace_final = links[0]['url'] # Por defecto el primero
        
        for item in links:
            ext = str(item.get('extension', '')).lower()
            tipo_item = str(item.get('type', '')).lower()
            
            if formato == 'mp3':
                if 'mp3' in ext or tipo_item == 'audio':
                    enlace_final = item['url']
                    break
            else: # mp4
                if 'mp4' in ext:
                    enlace_final = item['url']
                    break

        return jsonify({"download_url": enlace_final})

    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

if __name__ == "__main__":
    # Render asigna el puerto automáticamente
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
