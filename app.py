import os
import yt_dlp
from flask import Flask, request, jsonify, render_template_string, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- CONFIGURACIÓN DE PROXIES RESIDENCIALES (USA) ---
def get_ydl_opts():
    # Tu llave maestra de USA que configuramos en Webshare
    user = "ksvyuzxs-us-rotate" 
    pw = "r148qqniiwdz"
    proxy = f"http://{user}:{pw}@p.webshare.io:80"
    
    return {
        'proxy': proxy,
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1',
        'socket_timeout': 30,
        'referer': 'https://www.tiktok.com/'
    }

# --- INTERFAZ PREMIUM (NEÓN + ADSENSE + CONTADOR) ---
HTML_PRO = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Motor Pro 🚀 | Descargas Premium</title>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8532381032470048" crossorigin="anonymous"></script>
    <style>
        :root { --primary: #00f2ea; --secondary: #ff0050; --success: #2ecc71; --dark: #0a0a0a; }
        body { background: var(--dark); color: #fff; font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 10px; text-align: center; }
        .container { max-width: 500px; margin: 0 auto; }
        
        /* Espacios AdSense */
        .ad-slot { background: #111; margin: 15px 0; min-height: 90px; border: 1px dashed #333; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #444; }

        .card { background: #151515; padding: 30px; border-radius: 25px; border: 1px solid #333; box-shadow: 0 15px 50px rgba(0,0,0,0.8); position: relative; }
        h1 { font-size: 26px; margin: 0; background: linear-gradient(to right, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        p.tagline { font-size: 11px; color: #666; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 25px; }

        /* Input con botón X */
        .input-box { position: relative; width: 100%; margin-bottom: 20px; }
        input { width: 100%; padding: 18px; border-radius: 12px; border: 1px solid #333; background: #222; color: #fff; font-size: 16px; box-sizing: border-box; outline: none; transition: 0.3s; }
        input:focus { border-color: var(--primary); }
        .btn-clear { position: absolute; right: 15px; top: 18px; background: #444; border: none; color: #fff; border-radius: 50%; width: 24px; height: 24px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 12px; }

        #mainBtn { width: 100%; padding: 18px; background: #fff; color: #000; border: none; border-radius: 12px; font-weight: bold; font-size: 16px; cursor: pointer; transition: 0.3s; }
        #mainBtn:hover { transform: scale(1.02); background: var(--primary); }
        #mainBtn:disabled { background: #333; color: #666; cursor: not-allowed; }

        /* Resultado y Contador */
        #result { margin-top: 25px; min-height: 120px; }
        .progress-container { margin: 15px 0; background: #222; border-radius: 10px; height: 10px; overflow: hidden; display: none; }
        .progress-bar { width: 0%; height: 100%; background: var(--primary); transition: 1s linear; }
        
        .dl-btn { display: none; background: var(--success); color: #fff; padding: 20px; border-radius: 12px; text-decoration: none; font-weight: bold; font-size: 18px; box-shadow: 0 0 0px var(--success); transition: 0.4s; }
        .dl-btn.glow { display: block; animation: neonGlow 1.5s infinite alternate; }

        @keyframes neonGlow {
            from { box-shadow: 0 0 5px var(--success); }
            to { box-shadow: 0 0 25px var(--success); transform: scale(1.03); }
        }

        .footer { margin-top: 30px; font-size: 11px; color: #444; }
        .footer a { color: #666; text-decoration: none; margin: 0 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="ad-slot">
            <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-8532381032470048" data-ad-slot="TU_SLOT_1" data-ad-format="auto"></ins>
            <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
        </div>

        <div class="card">
            <h1>🚀 MOTOR PRO</h1>
            <p class="tagline">TikTok • Instagram • Facebook</p>
            
            <div class="input-box">
                <input type="text" id="urlInput" placeholder="Pega el link aquí..." autocomplete="off">
                <button class="btn-clear" onclick="document.getElementById('urlInput').value=''">✕</button>
            </div>

            <button id="mainBtn" onclick="procesar()">DESCARGAR VIDEO</button>

            <div id="result">
                <div id="statusText" style="color:#888; font-size: 14px; margin-bottom: 10px;"></div>
                <div class="progress-container" id="pContainer"><div class="progress-bar" id="pBar"></div></div>
                <a id="dlLink" class="dl-btn" href="#" target="_blank">DESCARGAR AHORA</a>
            </div>
        </div>

        <div class="ad-slot">
            <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-8532381032470048" data-ad-slot="TU_SLOT_2" data-ad-format="auto"></ins>
            <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
        </div>

        <div class="footer">
            <a href="/privacidad">Privacidad</a> • <a href="/terminos">Términos</a>
            <p>© 2026 Motor Pro - Cochabamba 🇧🇴</p>
        </div>
    </div>

    <script>
        async function procesar() {
            const url = document.getElementById('urlInput').value.trim();
            const status = document.getElementById('statusText');
            const btn = document.getElementById('mainBtn');
            const pContainer = document.getElementById('pContainer');
            const pBar = document.getElementById('pBar');
            const dlLink = document.getElementById('dlLink');

            if (!url) return;
            if (url.includes("youtube") || url.includes("youtu.be")) {
                status.innerHTML = "⚠️ YouTube no disponible en esta versión.";
                return;
            }

            btn.disabled = true;
            dlLink.classList.remove('glow');
            dlLink.style.display = 'none';
            status.innerHTML = "⏳ Conectando con servidor residencial USA...";

            try {
                const response = await fetch('/api/info?url=' + encodeURIComponent(url));
                const data = await response.json();

                if (data.success) {
                    status.innerHTML = "✅ ¡Video encontrado!<br><span style='color:var(--primary)'>Activando descarga en 8 segundos...</span>";
                    pContainer.style.display = 'block';
                    
                    let timeLeft = 8;
                    pBar.style.width = '0%';
                    
                    const interval = setInterval(() => {
                        timeLeft--;
                        let progress = ((8 - timeLeft) / 8) * 100;
                        pBar.style.width = progress + '%';

                        if (timeLeft <= 0) {
                            clearInterval(interval);
                            status.innerHTML = "<span style='color:var(--success)'>¡ENLACE SEGURO ACTIVADO!</span>";
                            pContainer.style.display = 'none';
                            dlLink.href = data.url;
                            dlLink.style.display = 'block';
                            dlLink.classList.add('glow');
                        }
                    }, 1000);

                } else {
                    status.innerHTML = "❌ Error: Link privado o no soportado.";
                    btn.disabled = false;
                }
            } catch (e) {
                status.innerHTML = "❌ Error de conexión.";
                btn.disabled = false;
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_PRO)

@app.route('/api/info')
def info():
    u = request.args.get('url')
    if not u: return jsonify({"success": False})
    
    # Limpiar link de rastreadores (WhatsApp/App)
    if "?" in u: u = u.split("?")[0]
    
    try:
        with yt_dlp.YoutubeDL(get_ydl_opts()) as ydl:
            i = ydl.extract_info(u, download=False)
            return jsonify({
                "success": True, 
                "url": i.get('url'), 
                "title": i.get('title')
            })
    except Exception as e:
        print(f"Error Log: {e}")
        return jsonify({"success": False})

@app.route('/privacidad')
def privacidad(): return "<h1>Privacidad</h1><p>No almacenamos datos de usuario ni registros de descargas.</p>"

@app.route('/terminos')
def terminos(): return "<h1>Términos</h1><p>Uso personal exclusivamente. No somos responsables por el contenido descargado.</p>"

@app.route('/ads.txt')
def ads_txt(): return Response("google.com, pub-8532381032470048, DIRECT, f08c47fec0942fa0", mimetype='text/plain')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
