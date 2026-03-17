from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# --- EL DISEÑO DE TU PÁGINA (Directo en el código para evitar 404) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Descargador Pro - Cochabamba</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0f0f0f; color: white; text-align: center; padding: 50px; }
        .card { background: #1e1e1e; padding: 30px; border-radius: 15px; display: inline-block; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        input { padding: 12px; width: 300px; border-radius: 5px; border: 1px solid #333; background: #2a2a2a; color: white; margin-bottom: 10px; }
        button { padding: 12px 25px; cursor: pointer; background: #cc0000; color: white; border: none; border-radius: 5px; font-weight: bold; }
        button:hover { background: #ff0000; }
        #status { margin-top: 20px; color: #aaa; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 Motor de Descarga</h1>
        <input type="text" id="url" placeholder="Pega el link de YouTube aquí">
        <br>
        <select id="tipo" style="padding: 10px; border-radius: 5px; background: #2a2a2a; color: white; margin-bottom: 10px;">
            <option value="mp4">Video MP4</option>
            <option value="mp3">Audio MP3</option>
        </select>
        <br>
        <button onclick="bajar()">DESCARGAR AHORA</button>
        <div id="status"></div>
    </div>

    <script>
        async function bajar() {
            const videoUrl = document.getElementById('url').value;
            const tipo = document.getElementById('tipo').value;
            const status = document.getElementById('status');

            if(!videoUrl) return alert("Pega un link primero");

            status.innerText = "⏳ Conectando con el servidor...";

            try {
                // LLAMADA RELATIVA (Evita errores de dominio)
                const res = await fetch(`/descargar?url=` + encodeURIComponent(videoUrl) + `&tipo=` + tipo);
                
                if (res.status === 404) {
                    status.innerText = "❌ Error 404: El servidor no encuentra la ruta.";
                    return;
                }

                const data = await res.json();
                if(data.download_url) {
                    status.innerText = "✅ ¡Enlace generado! Iniciando...";
                    window.location.href = data.download_url;
                } else {
                    status.innerText = "❌ Error: " + (data.error || "No se pudo obtener el video");
                }
            } catch (e) {
                status.innerText = "❌ Error de red o servidor apagado.";
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def main():
    return HTML_TEMPLATE

@app.route('/descargar', methods=['GET'])
def descargar():
    url_v = request.args.get('url')
    tipo = request.args.get('tipo', 'mp4')
    
    if not url_v:
        return jsonify({"error": "Falta URL"}), 400

    # Limpieza de URL para evitar errores de API
    url_v = url_v.split('?')[0].split('&')[0]

    headers = {
        "x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585", 
        "x-rapidapi-host": "auto-download-all-in-one.p.rapidapi.com"
    }
    
    try:
        r = requests.post("https://auto-download-all-in-one.p.rapidapi.com/v1/social/autolink", 
                          json={"url": url_v}, headers=headers, timeout=15)
        res_data = r.json()
        links = res_data.get("result", [])
        
        if links:
            # Seleccionamos el link segun tipo
            final = links[0]['url']
            for l in links:
                if tipo == 'mp3' and (l.get('type') == 'audio' or 'mp3' in str(l.get('extension'))):
                    final = l['url']
                    break
                if tipo == 'mp4' and 'mp4' in str(l.get('extension')):
                    final = l['url']
                    break
            return jsonify({"download_url": final})
        
        return jsonify({"error": "Video no encontrado en la API"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
