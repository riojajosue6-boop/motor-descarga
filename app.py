import os
import requests
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

HTML_FINAL = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Motor de Descarga</title>
    <style>
        body { background: #0f0f0f; color: white; font-family: 'Segoe UI', sans-serif; text-align: center; padding: 40px; }
        .card { background: #1a1a1a; padding: 30px; border-radius: 20px; display: inline-block; border: 1px solid #333; max-width: 400px; width: 90%; }
        input { width: 90%; padding: 12px; margin: 15px 0; border-radius: 8px; border: none; background: #2a2a2a; color: white; }
        button { width: 95%; padding: 12px; background: #cc0000; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; }
        #status { margin-top: 20px; font-size: 14px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 Motor de Descarga</h1>
        <p>YouTube, TikTok e Instagram</p>
        <input type="text" id="urlInput" placeholder="Pega el link aquí...">
        <button onclick="descargar()">DESCARGAR AHORA</button>
        <div id="status"></div>
    </div>
    <script>
        async function descargar() {
            const url = document.getElementById('urlInput').value;
            const status = document.getElementById('status');
            if(!url) return alert("Pega un link");
            status.style.color = "white";
            status.innerText = "⏳ Procesando... espera un momento.";
            try {
                const response = await fetch('/api/bajar?url=' + encodeURIComponent(url));
                const data = await response.json();
                if(data.download_url) {
                    status.style.color = "#44ff44";
                    status.innerText = "✅ ¡Enlace generado! Descargando...";
                    window.location.href = data.download_url;
                } else {
                    status.style.color = "#ff4444";
                    status.innerText = "❌ " + (data.error || "No se encontró el video");
                }
            } catch (e) { status.innerText = "❌ Error de conexión."; }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_FINAL)

@app.route('/api/bajar')
def bajar():
    video_url = request.args.get('url')
    if not video_url: return jsonify({"error": "Falta URL"}), 400
    
    video_url = video_url.split('?')[0].split('&')[0]
    headers = {
        "x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585",
        "x-rapidapi-host": "auto-download-all-in-one.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post("https://auto-download-all-in-one.p.rapidapi.com/v1/social/autolink",
                          json={"url": video_url}, headers=headers, timeout=25)
        data = r.json()
        medias = data.get("medias", [])
        
        # --- LÓGICA FLEXIBLE (Detecta si es Lista o Diccionario) ---
        link_final = None
        
        if isinstance(medias, list) and len(medias) > 0:
            # Formato YouTube (Lista)
            link_final = medias[0].get("url")
        elif isinstance(medias, dict) and len(medias) > 0:
            # Formato TikTok (Diccionario)
            primer_key = list(medias.keys())[0]
            link_final = medias[primer_key].get("url")
            
        if link_final:
            return jsonify({"download_url": link_final})
        
        return jsonify({"error": "Video no disponible o privado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
