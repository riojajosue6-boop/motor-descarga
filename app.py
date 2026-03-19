import os
import requests
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# --- DISEÑO PROFESIONAL MONETIZABLE ---
HTML_PRO = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Descargador Pro | Cochabamba</title>
    <style>
        :root { --red: #ff0000; --dark: #0a0a0a; --card: #161616; }
        body { background: var(--dark); color: #fff; font-family: 'Segoe UI', sans-serif; margin: 0; text-align: center; }
        nav { background: #000; padding: 15px; border-bottom: 1px solid #333; }
        nav a { color: #888; margin: 0 15px; text-decoration: none; font-size: 14px; cursor: pointer; }
        nav a:hover { color: var(--red); }
        .ad-slot { background: #111; border: 1px dashed #444; margin: 20px auto; padding: 10px; max-width: 728px; min-height: 90px; color: #555; font-size: 11px; }
        .main-container { background: var(--card); padding: 35px; border-radius: 25px; display: inline-block; border: 1px solid #222; max-width: 480px; width: 90%; margin-top: 20px; box-shadow: 0 20px 50px rgba(0,0,0,0.8); }
        h1 { color: var(--red); margin: 0 0 5px 0; font-size: 30px; }
        input { width: 90%; padding: 16px; margin: 20px 0; border-radius: 12px; border: 1px solid #333; background: #222; color: #fff; font-size: 16px; outline: none; }
        .options { display: flex; gap: 10px; margin-bottom: 20px; justify-content: center; }
        select { padding: 12px; border-radius: 8px; background: #222; color: white; border: 1px solid #444; flex: 1; }
        button { width: 95%; padding: 16px; background: var(--red); color: white; border: none; border-radius: 12px; font-weight: bold; font-size: 18px; cursor: pointer; transition: 0.3s; }
        button:disabled { background: #444; cursor: not-allowed; }
        #status { margin-top: 25px; font-weight: bold; min-height: 30px; }
        .legal-page { display: none; max-width: 700px; margin: 40px auto; text-align: left; background: #111; padding: 30px; border-radius: 15px; color: #aaa; line-height: 1.6; }
        footer { padding: 40px; color: #444; font-size: 12px; }
    </style>
</head>
<body>

    <nav>
        <a onclick="ir('home')">Inicio</a>
        <a onclick="ir('privacidad')">Privacidad</a>
        <a onclick="ir('terminos')">Términos</a>
    </nav>

    <div class="ad-slot">PUBLICIDAD ADSENSE TOP </div>

    <div id="home">
        <div class="main-container">
            <h1>🚀 Descargador Pro</h1>
            <p style="color:#666; margin-bottom:20px;">YouTube • TikTok • Instagram • FB</p>
            
            <input type="text" id="urlIn" placeholder="Pega el link del video aquí...">
            
            <div class="options">
                <select id="fmtIn">
                    <option value="mp4">🎬 Video MP4</option>
                    <option value="mp3">🎵 Audio MP3</option>
                </select>
            </div>

            <button id="btnGo" onclick="start()">DESCARGAR AHORA</button>
            <div id="status"></div>
        </div>
    </div>

    <div id="privacidad" class="legal-page">
        <h2>Política de Privacidad</h2>
        <p>En Descargador Pro respetamos tu privacidad. No almacenamos registros de tus descargas ni datos personales. Este sitio utiliza cookies de Google AdSense para mostrar anuncios relevantes.</p>
    </div>

    <div id="terminos" class="legal-page">
        <h2>Términos de Uso</h2>
        <p>Esta herramienta es para uso personal. El usuario es responsable de cumplir con las leyes de derechos de autor de su país. No nos hacemos responsables del contenido descargado.</p>
    </div>

    <div class="ad-slot">PUBLICIDAD ADSENSE BOTTOM </div>

    <footer>© 2026 Motor de Descarga | Hecho en Cochabamba 🇧🇴</footer>

    <script>
        function ir(id) {
            ['home','privacidad','terminos'].forEach(p => document.getElementById(p).style.display = (p===id?'block':'none'));
            window.scrollTo(0,0);
        }

        async function start() {
            const u = document.getElementById('urlIn').value;
            const t = document.getElementById('fmtIn').value;
            const b = document.getElementById('btnGo');
            const s = document.getElementById('status');

            if(!u) return alert("Pega un enlace");

            b.disabled = true;
            let count = 5;
            
            const timer = setInterval(async () => {
                s.style.color = "#ffaa00";
                s.innerText = `⏳ Preparando descarga en ${count}...`;
                count--;

                if(count < 0) {
                    clearInterval(timer);
                    s.innerText = "🚀 Conectando con el motor...";
                    try {
                        const res = await fetch(`/api/down?url=${encodeURIComponent(u)}&type=${t}`);
                        const data = await res.json();
                        if(data.url) {
                            s.style.color = "#00ff88";
                            s.innerText = "✅ ¡Listo! Iniciando descarga...";
                            window.location.href = data.url;
                        } else {
                            s.style.color = "#ff4444";
                            s.innerText = "❌ " + (data.error || "Video no disponible");
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

@app.route('/')
def index():
    return render_template_string(HTML_PRO)

@app.route('/api/down')
def api_down():
    url = request.args.get('url')
    fmt = request.args.get('type', 'mp4')
    if not url: return jsonify({"error": "No URL"}), 400

    # Usamos la nueva API LITE que encontraste (es más estable)
    api_url = f"https://download-all-in-one-lite.p.rapidapi.com/autolink"
    headers = {
        "x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585",
        "x-rapidapi-host": "download-all-in-one-lite.p.rapidapi.com"
    }

    try:
        # Petición GET con el parámetro url
        r = requests.get(api_url, params={"url": url}, headers=headers, timeout=25)
        data = r.json()
        
        # Esta API suele devolver una lista en 'medias' o 'result'
        medias = data.get("medias", data.get("result", []))
        
        link = None
        if isinstance(medias, list) and len(medias) > 0:
            for m in medias:
                if fmt == 'mp3' and 'audio' in str(m.get('type','')).lower():
                    link = m.get('url'); break
                if fmt == 'mp4' and 'video' in str(m.get('type','')).lower():
                    link = m.get('url'); break
            if not link: link = medias[0].get('url')
        elif isinstance(medias, dict):
            link = list(medias.values())[0].get('url')

        if link: return jsonify({"url": link})
        return jsonify({"error": "No se encontraron enlaces de descarga."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
