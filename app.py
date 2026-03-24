import os
import yt_dlp
from flask import Flask, request, jsonify, render_template_string, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- CONFIGURACIÓN DE PROXIES RESIDENCIALES (WEBSHARE USA) ---
def get_ydl_opts():
    user = "ksvyuzxs-rotate" 
    pw = "r148qqniiwdz"
    proxy = f"http://{user}:{pw}@p.webshare.io:80"
    
    return {
        'proxy': proxy,
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'socket_timeout': 30,
        'referer': 'https://www.tiktok.com/'
    }

# --- DISEÑO DE LA PÁGINA ---
# Asegúrate de que esta variable exista tal cual
HTML_PRO = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Motor Pro 🚀 | Descargas</title>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8532381032470048" crossorigin="anonymous"></script>
    <style>
        :root { --primary: #00f2ea; --secondary: #ff0050; --dark: #0a0a0a; }
        body { background: var(--dark); color: #fff; font-family: sans-serif; text-align: center; margin: 0; padding: 20px; }
        .card { background: #151515; padding: 30px; border-radius: 25px; border: 1px solid #333; max-width: 450px; margin: 50px auto; }
        h1 { background: linear-gradient(to right, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        input { width: 100%; padding: 15px; border-radius: 12px; border: 1px solid #444; background: #222; color: #fff; box-sizing: border-box; }
        button { width: 100%; padding: 15px; background: #fff; color: #000; border: none; border-radius: 12px; margin-top: 20px; font-weight: bold; cursor: pointer; }
        #result { margin-top: 25px; min-height: 80px; }
        .dl-btn { display: block; background: linear-gradient(45deg, var(--primary), var(--secondary)); color: #fff; padding: 15px; border-radius: 12px; text-decoration: none; font-weight: bold; }
        .dl-btn.disabled { background: #333; pointer-events: none; opacity: 0.5; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 MOTOR PRO</h1>
        <p style="color:#666; font-size:12px">TikTok • Instagram • Facebook</p>
        <input type="text" id="urlInput" placeholder="Pega el link aquí...">
        <button id="mainBtn" onclick="procesar()">OBTENER VIDEO</button>
        <div id="result"></div>
    </div>
    <div style="font-size: 12px; color: #444; margin-top: 20px;">
        <a href="/privacidad" style="color:#666">Privacidad</a> | <a href="/terminos" style="color:#666">Términos</a>
    </div>
    <script>
        async function procesar() {
            const url = document.getElementById('urlInput').value.trim();
            const res = document.getElementById('result');
            const btn = document.getElementById('mainBtn');
            if(!url) return;
            btn.disabled = true;
            res.innerHTML = "⏳ Extrayendo video...";
            try {
                const response = await fetch('/api/info?url=' + encodeURIComponent(url));
                const data = await response.json();
                if(data.success) {
                    res.innerHTML = `
                        <div style="margin-bottom:10px; font-size:12px">Contenido listo. El botón se activará en 8s...</div>
                        <b id="timer">8s</b><br><br>
                        <a id="dlLink" class="dl-btn disabled" href="${data.url}" target="_blank">DESCARGAR AHORA</a>`;
                    let timeLeft = 8;
                    const i = setInterval(() => {
                        timeLeft--;
                        document.getElementById('timer').innerText = timeLeft + "s";
                        if(timeLeft <= 0) {
                            clearInterval(i);
                            document.getElementById('timer').innerText = "¡LISTO!";
                            document.getElementById('dlLink').classList.remove('disabled');
                        }
                    }, 1000);
                } else { res.innerHTML = "❌ Error. Prueba con otro link público."; }
            } catch(e) { res.innerHTML = "❌ Error de conexión."; }
            btn.disabled = false;
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    # CAMBIO: Ahora enviamos HTML_PRO directamente para evitar el IndexError
    return render_template_string(HTML_PRO)

@app.route('/api/info')
def info():
    u = request.args.get('url')
    if not u or "youtube" in u or "youtu.be" in u: return jsonify({"success": False})
    try:
        with yt_dlp.YoutubeDL(get_ydl_opts()) as ydl:
            i = ydl.extract_info(u, download=False)
            return jsonify({"success": True, "url": i.get('url'), "title": i.get('title')})
    except: return jsonify({"success": False})

@app.route('/privacidad')
def privacidad(): return "<h1>Privacidad</h1><p>No guardamos tus datos.</p>"

@app.route('/terminos')
def terminos(): return "<h1>Términos</h1><p>Uso personal solamente.</p>"

@app.route('/ads.txt')
def ads_txt(): return Response("google.com, pub-8532381032470048, DIRECT, f08c47fec0942fa0", mimetype='text/plain')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
