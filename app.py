import os
import yt_dlp
from flask import Flask, request, jsonify, render_template_string, Response
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# --- PROXIES (Usando tus variables de Railway) ---
P_USER = os.environ.get("PROXY_USER", "ksvyuzxs")
P_PASS = os.environ.get("PROXY_PASS", "r148qqniiwdz")
P_HOST = "p.webshare.io"
P_PORT = "80"

def get_proxy():
    p_url = f"http://{P_USER}:{P_PASS}@{P_HOST}:{P_PORT}"
    return {"http": p_url, "https": p_url}

# --- DISEÑO (Mantenemos tu estructura intacta) ---
# [Aquí va el mismo HTML que ya tienes, no lo cambio para no perder tiempo]
# Pero asegúrate de que el fetch en el script apunte a /api/info como abajo.

@app.route('/')
def index():
    # Reutiliza el HTML_PREMIUM que ya tienes en tu app.py
    # Solo asegúrate de que el resto del código sea este:
    return render_template_string(open('app.py', 'r').read().split('HTML_PREMIUM = """')[1].split('"""')[0])

@app.route('/api/info')
def api_info():
    url = request.args.get('url')
    fmt = request.args.get('type', 'mp4')
    if not url: return jsonify({"success": False})

    # CONFIGURACIÓN MAESTRA ANTI-BLOQUEO
    ydl_opts = {
        'proxy': get_proxy()['http'],
        'quiet': True,
        'no_warnings': True,
        'format': 'best', # Cambiado a 'best' para máxima compatibilidad
        'extract_flat': False,
        'force_generic_extractor': False,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Intentamos extraer la info
            info = ydl.extract_info(url, download=False)
            if not info: return jsonify({"success": False})
            
            return jsonify({
                "success": True,
                "title": info.get('title', 'Video Pro'),
                "thumbnail": info.get('thumbnail', ''),
                "download_url": info.get('url')
            })
    except Exception as e:
        print(f"DEBUG ERROR: {str(e)}") # Esto saldrá en tus logs de Railway
        return jsonify({"success": False, "error": str(e)})

@app.route('/ads.txt')
def ads_txt(): return Response("google.com, pub-8532381032470048, DIRECT, f08c47fec0942fa0", mimetype='text/plain')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
