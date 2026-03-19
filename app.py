import os
import requests
import re
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# --- INTERFAZ PROFESIONAL ---
HTML_PRO = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Motor de Descarga Pro</title>
    <style>
        :root { --red: #ff0000; --dark: #0a0a0a; --card: #161616; }
        body { background: var(--dark); color: #fff; font-family: 'Segoe UI', sans-serif; margin: 0; text-align: center; padding: 20px; }
        .main-container { background: var(--card); padding: 35px; border-radius: 25px; display: inline-block; border: 1px solid #222; max-width: 450px; width: 95%; box-shadow: 0 20px 50px rgba(0,0,0,0.8); }
        h1 { color: var(--red); font-size: 28px; margin-bottom: 10px; }
        input { width: 90%; padding: 15px; margin: 20px 0; border-radius: 10px; border: 1px solid #333; background: #222; color: #fff; font-size: 16px; outline: none; }
        button { width: 95%; padding: 15px; background: var(--red); color: white; border: none; border-radius: 10px; font-weight: bold; font-size: 18px; cursor: pointer; }
        button:disabled { background: #444; }
        #status { margin-top: 25px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="main-container">
        <h1>🚀 Motor de Descarga</h1>
        <p style="color:#888;">YouTube • Facebook • TikTok</p>
        <input type="text" id="urlIn" placeholder="Pega el link aquí...">
        <button id="btnGo" onclick="start()">DESCARGAR (5s)</button>
        <div id="status"></div>
    </div>

    <script>
        async function start() {
            const u = document.getElementById('urlIn').value;
            const b = document.getElementById('btnGo');
            const s = document.getElementById('status');
            if(!u) return alert("Pega un link");
            
            b.disabled = true;
            let c = 5;
            const t = setInterval(async () => {
                s.style.color = "#ffaa00";
                s.innerText = `⏳ Evitando bloqueo de Google en ${c}...`;
                c--;
                if(c < 0) {
                    clearInterval(t);
                    s.innerText = "🚀 Solicitando tunel de datos...";
                    try {
                        const res = await fetch(`/api/down?url=${encodeURIComponent(u)}`);
                        const data = await res.json();
                        if(data.url) {
                            s.style.color = "#00ff88";
                            s.innerText = "✅ ¡Enlace obtenido! Descargando...";
                            // TRUCO FINAL: Forzar descarga directa
                            const a = document.createElement('a');
                            a.href = data.url;
                            a.download = "video.mp4";
                            document.body.appendChild(a);
                            a.click();
                            document.body.removeChild(a);
                        } else {
                            s.style.color = "#ff4444";
                            s.innerText = "❌ " + (data.error || "Error de servidor");
                        }
                    } catch(e) { s.innerText = "❌ Error de conexión."; }
                    b.disabled = false;
                }
            }, 1000);
        }
    </script>
</body>
</html>
"""

def get_yt_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

@app.route('/')
def index():
    return render_template_string(HTML_PRO)

@app.route('/api/down')
def api_down():
    url = request.args.get('url')
    if not url: return jsonify({"error": "Falta URL"}), 400

    headers = {
        "x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585",
        "x-rapidapi-host": "yt-api.p.rapidapi.com"
    }

    if "youtube.com" in url or "youtu.be" in url:
        yt_id = get_yt_id(url)
        # Probamos el endpoint que genera links más compatibles
        try:
            # Usamos el endpoint que devuelve todos los formatos
            r = requests.get("https://yt-api.p.rapidapi.com/dl", params={"id": yt_id}, headers=headers, timeout=20)
            data = r.json()
            
            # Buscamos formatos que NO tengan restricción de IP (non-n-encoded)
            link = None
            if 'formats' in data:
                # Prioridad: Buscar un formato de video que tenga URL
                for f in data['formats']:
                    if f.get('url') and 'video' in f.get('mimeType', ''):
                        link = f['url']
                        break
            
            if not link: link = data.get('link')
            
            if link: return jsonify({"url": link})
            return jsonify({"error": "Google bloqueó este link por IP. Prueba un video más corto."}), 403
        except: return jsonify({"error": "Error de YouTube"}), 502
    else:
        # MOTOR LITE (Para redes sociales)
        lite_headers = {
            "x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585",
            "x-rapidapi-host": "download-all-in-one-lite.p.rapidapi.com"
        }
        try:
            r = requests.get("https://download-all-in-one-lite.p.rapidapi.com/autolink", 
                            params={"url": url}, headers=lite_headers, timeout=20)
            data = r.json()
            medias = data.get("medias", data.get("result", []))
            link = medias[0].get('url') if isinstance(medias, list) and medias else None
            return jsonify({"url": link})
        except: return jsonify({"error": "Error de Motor Lite"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
