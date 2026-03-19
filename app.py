import os
import requests
import re
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# --- INTERFAZ CON PUBLICIDAD Y LEGAL ---
HTML_PRO = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Motor de Descarga Pro | Bolivia</title>
    <style>
        :root { --red: #ff0000; --dark: #0a0a0a; --card: #161616; }
        body { background: var(--dark); color: #fff; font-family: 'Segoe UI', sans-serif; margin: 0; text-align: center; }
        nav { background: #000; padding: 15px; border-bottom: 1px solid #333; }
        nav a { color: #888; margin: 0 15px; text-decoration: none; font-size: 14px; cursor: pointer; }
        .ad-slot { background: #111; border: 1px dashed #444; margin: 20px auto; padding: 10px; max-width: 728px; min-height: 90px; color: #555; font-size: 11px; }
        .main-container { background: var(--card); padding: 35px; border-radius: 25px; display: inline-block; border: 1px solid #222; max-width: 480px; width: 90%; margin-top: 20px; box-shadow: 0 20px 50px rgba(0,0,0,0.8); }
        h1 { color: var(--red); margin: 0; font-size: 30px; }
        input { width: 90%; padding: 16px; margin: 20px 0; border-radius: 12px; border: 1px solid #333; background: #222; color: #fff; font-size: 16px; outline: none; }
        button { width: 95%; padding: 16px; background: var(--red); color: white; border: none; border-radius: 12px; font-weight: bold; font-size: 18px; cursor: pointer; }
        button:disabled { background: #444; }
        #status { margin-top: 25px; font-weight: bold; min-height: 30px; }
        footer { padding: 40px; color: #444; font-size: 12px; }
    </style>
</head>
<body>
    <nav><a onclick="location.reload()">Inicio</a><a>Privacidad</a><a>Términos</a></nav>
    <div class="ad-slot">ANUNCIO ADSENSE AQUÍ</div>
    <div class="main-container">
        <h1>🚀 Motor Pro</h1>
        <p style="color:#666;">YouTube • Facebook • TikTok • Instagram</p>
        <input type="text" id="urlIn" placeholder="Pega el link aquí...">
        <button id="btnGo" onclick="start()">DESCARGAR (5s)</button>
        <div id="status"></div>
    </div>
    <footer>© 2026 Descargador Cochabamba 🇧🇴</footer>

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
                s.innerText = `⏳ Generando tunel de descarga en ${c}...`;
                c--;
                if(c < 0) {
                    clearInterval(t);
                    s.innerText = "🚀 Saltando bloqueo 403...";
                    try {
                        const res = await fetch(`/api/down?url=${encodeURIComponent(u)}`);
                        const data = await res.json();
                        if(data.url) {
                            s.style.color = "#00ff88";
                            s.innerText = "✅ ¡Éxito! Iniciando descarga...";
                            // Forzamos la descarga en pestaña nueva
                            const win = window.open(data.url, '_blank');
                            if(!win) window.location.href = data.url;
                        } else {
                            s.style.color = "#ff4444";
                            s.innerText = "❌ " + (data.error || "Error de API");
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

    if "youtube.com" in url or "youtu.be" in url:
        yt_id = get_yt_id(url)
        if not yt_id: return jsonify({"error": "Link de YouTube inválido"}), 400
        
        # NUEVA ESTRATEGIA: Forzar descarga limpia
        api_url = "https://yt-api.p.rapidapi.com/dl"
        headers = {
            "x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585",
            "x-rapidapi-host": "yt-api.p.rapidapi.com"
        }
        try:
            # Pedimos el video (el costo es 6 créditos, recuerda)
            r = requests.get(api_url, params={"id": yt_id}, headers=headers, timeout=20)
            data = r.json()
            
            # Buscamos el link que NO sea de googlevideo si es posible, o el directo
            link = data.get('link')
            if not link and 'formats' in data:
                # Buscamos el primer formato que tenga URL válida
                for f in data['formats']:
                    if 'url' in f:
                        link = f['url']
                        break
            
            if link: return jsonify({"url": link})
            return jsonify({"error": "YouTube bloqueó la petición (403). Intenta otro video."}), 403
        except: return jsonify({"error": "Error en el servidor de YouTube"}), 502
    else:
        # MOTOR LITE (Para FB, TikTok, etc.)
        headers = {
            "x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585",
            "x-rapidapi-host": "download-all-in-one-lite.p.rapidapi.com"
        }
        try:
            r = requests.get("https://download-all-in-one-lite.p.rapidapi.com/autolink", 
                            params={"url": url}, headers=headers, timeout=20)
            data = r.json()
            medias = data.get("medias", data.get("result", []))
            link = medias[0].get('url') if isinstance(medias, list) and medias else None
            return jsonify({"url": link}) if link else jsonify({"error": "No compatible"}), 404
        except: return jsonify({"error": "Error en motor Lite"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
