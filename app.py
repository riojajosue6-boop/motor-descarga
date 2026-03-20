import os
import requests
import re
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# --- DISEÑO PREMIUM CON CONTADOR DE APOYO ---
HTML_PREMIUM = """
<!DOCTYPE html>
<html lang="es">
<head>
    <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
    new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    })(window,document,'script','dataLayer','GTM-5P943783');</script>
    
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Motor de Descarga Pro | Bolivia</title>
    
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8532381032470048" crossorigin="anonymous"></script>

    <style>
        :root { --red: #ff0000; --dark: #0a0a0a; --gray: #1a1a1a; --text: #eee; }
        body { background: var(--dark); color: var(--text); font-family: 'Segoe UI', sans-serif; margin: 0; text-align: center; }
        nav { background: #000; padding: 15px; border-bottom: 1px solid #333; position: sticky; top: 0; z-index: 100; }
        nav a { color: #888; margin: 0 15px; text-decoration: none; font-size: 14px; cursor: pointer; transition: 0.3s; }
        nav a:hover { color: var(--red); }
        .container { padding: 20px; max-width: 800px; margin: 0 auto; }
        .main-card { background: var(--gray); padding: 40px; border-radius: 25px; border: 1px solid #333; margin: 10px auto; box-shadow: 0 20px 60px rgba(0,0,0,0.8); }
        h1 { color: var(--red); font-size: 32px; margin-bottom: 20px; }
        input { width: 100%; padding: 18px; border-radius: 12px; border: 1px solid #333; background: #222; color: #fff; font-size: 16px; box-sizing: border-box; margin-bottom: 20px; outline: none; }
        .options { display: flex; gap: 10px; margin-bottom: 25px; }
        select { padding: 15px; border-radius: 10px; background: #222; color: white; border: 1px solid #444; flex: 1; }
        #btnAction { width: 100%; padding: 18px; background: var(--red); color: white; border: none; border-radius: 12px; font-weight: bold; font-size: 18px; cursor: pointer; }
        
        #errorMessage { display: none; background: #2a1010; color: #ff9999; border: 1px solid #ff0000; padding: 20px; border-radius: 15px; margin-top: 20px; line-height: 1.5; text-align: left; }
        
        /* ESTILO MENSAJE DE APOYO */
        #supportBox { display: none; background: #1a2a1a; color: #99ff99; border: 1px solid #00aa00; padding: 20px; border-radius: 15px; margin: 20px 0; font-size: 14px; line-height: 1.5; }
        #countdownText { font-weight: bold; color: #fff; font-size: 18px; margin-top: 10px; display: block; }

        #previewSection { display: none; margin-top: 30px; border-top: 1px solid #333; padding-top: 20px; }
        #videoThumbnail { width: 100%; max-width: 400px; border-radius: 15px; border: 1px solid #444; }
        #finalDownloadBtn { width: 100%; padding: 15px; background: #00aa00; color: white; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; margin-top: 15px; }
        #finalDownloadBtn:disabled { background: #333; color: #777; cursor: not-allowed; }
        
        .ad-slot { margin: 20px auto; min-height: 90px; }
        footer { padding: 40px; color: #444; font-size: 12px; }
    </style>
</head>
<body>
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-5P943783" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

    <nav>
        <a onclick="showSection('home')">Inicio</a>
        <a onclick="showSection('privacy')">Privacidad</a>
        <a onclick="showSection('terms')">Términos</a>
    </nav>

    <div class="container">
        <div id="home-sec">
            <div class="ad-slot">
                <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-8532381032470048" data-ad-slot="5199614767" data-ad-format="auto" data-full-width-responsive="true"></ins>
                <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
            </div>

            <div class="main-card">
                <h1>🚀 MOTOR DE DESCARGA</h1>
                <input type="text" id="urlInput" placeholder="Pega el enlace de video aquí...">
                <div class="options">
                    <select id="formatInput">
                        <option value="mp4">🎬 Video MP4</option>
                        <option value="mp3">🎵 Audio MP3</option>
                    </select>
                </div>
                <button id="btnAction" onclick="processVideo()">PROCESAR VIDEO</button>
                <div id="status" style="margin-top:20px; font-weight:bold;"></div>
                
                <div id="errorMessage">
                    <strong>⚠️ Aviso del Sistema:</strong><br>
                    Lo sentimos, el servidor no pudo procesar la solicitud para este video de YouTube en este momento. Nuestro equipo técnico trabaja para solucionar el inconveniente.<br><br>
                    Recuerda que puedes descargar videos de otras plataformas (TikTok, Instagram, Facebook) sin problemas mientras lo solucionamos. ¡Intenta más tarde con este video!
                </div>

                <div id="previewSection">
                    <img id="videoThumbnail" src="">
                    <div id="videoTitle" style="margin-bottom:15px; font-weight:bold; color:#fff;"></div>
                    
                    <div id="supportBox">
                        ❤️ <strong>Querido usuario:</strong> Muchas gracias por usar esta herramienta. Por favor, toma unos segundos para visitar las publicidades; esto nos ayuda a mantener los servidores a tu servicio y que tengas una experiencia grata. ¡Muchas gracias!
                        <span id="countdownText">El botón se activará en 5...</span>
                    </div>

                    <button id="finalDownloadBtn" disabled>CONFIRMAR DESCARGA</button>
                </div>
            </div>
            
            <div class="ad-slot">
                <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-8532381032470048" data-ad-slot="5199614767" data-ad-format="auto" data-full-width-responsive="true"></ins>
                <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
            </div>
        </div>
        
        <div id="privacy-sec" class="legal-content"><h2>Privacidad</h2><p>Cumplimos con las normativas de Google AdSense.</p></div>
        <div id="terms-sec" class="legal-content"><h2>Términos</h2><p>Uso personal bajo responsabilidad del usuario.</p></div>
    </div>

    <footer>© 2026 Descargador Pro - Cochabamba 🇧🇴</footer>

    <script>
        function showSection(sec) {
            document.getElementById('home-sec').style.display = sec === 'home' ? 'block' : 'none';
            document.getElementById('privacy-sec').style.display = sec === 'privacy' ? 'block' : 'none';
            document.getElementById('terms-sec').style.display = sec === 'terms' ? 'block' : 'none';
        }

        async function processVideo() {
            const url = document.getElementById('urlInput').value;
            const s = document.getElementById('status');
            const p = document.getElementById('previewSection');
            const err = document.getElementById('errorMessage');
            const box = document.getElementById('supportBox');
            const b = document.getElementById('btnAction');
            const dBtn = document.getElementById('finalDownloadBtn');
            
            if(!url) return alert("Pega un link");
            
            b.disabled = true;
            p.style.display = 'none';
            err.style.display = 'none';
            box.style.display = 'none';
            dBtn.disabled = true;
            s.innerText = "⏳ Analizando enlace...";

            try {
                const res = await fetch('/api/info?url=' + encodeURIComponent(url));
                const info = await res.json();
                if(info.success) {
                    document.getElementById('videoThumbnail').src = info.thumbnail;
                    document.getElementById('videoTitle').innerText = info.title;
                    p.style.display = 'block';
                    box.style.display = 'block';
                    s.innerText = "✅ Video detectado";
                    
                    // INICIAR CONTADOR
                    let timeLeft = 5;
                    const countdown = setInterval(() => {
                        timeLeft--;
                        document.getElementById('countdownText').innerText = `El botón se activará en ${timeLeft}...`;
                        if(timeLeft <= 0) {
                            clearInterval(countdown);
                            document.getElementById('countdownText').style.display = 'none';
                            dBtn.disabled = false;
                            dBtn.innerText = "¡LISTO PARA DESCARGAR!";
                        }
                    }, 1000);

                    dBtn.onclick = () => generateDownload(url, document.getElementById('formatInput').value);
                } else {
                    s.innerText = "";
                    err.style.display = 'block';
                }
            } catch (e) {
                s.innerText = "❌ Error de conexión.";
            }
            b.disabled = false;
        }

        async function generateDownload(url, tipo) {
            const s = document.getElementById('status');
            const err = document.getElementById('errorMessage');
            s.innerText = "🚀 Generando descarga...";
            err.style.display = 'none';

            try {
                const res = await fetch(`/api/down?url=${encodeURIComponent(url)}&type=${tipo}`);
                const data = await res.json();
                
                if(data.url) {
                    let hiddenIframe = document.getElementById('hiddenDownloader');
                    if (!hiddenIframe) {
                        hiddenIframe = document.createElement('iframe');
                        hiddenIframe.id = 'hiddenDownloader';
                        hiddenIframe.style.display = 'none';
                        document.body.appendChild(hiddenIframe);
                    }
                    hiddenIframe.src = data.url;
                    s.innerText = "✅ Intento de descarga enviado";
                    setTimeout(() => {
                        if (s.innerText.includes("enviado")) {
                            err.style.display = 'block';
                            s.innerText = "";
                        }
                    }, 4000);
                } else {
                    s.innerText = "";
                    err.style.display = 'block';
                }
            } catch (e) {
                s.innerText = "";
                err.style.display = 'block';
            }
        }
    </script>
</body>
</html>
"""

# ... (El resto de las funciones de Python se mantienen igual)
def get_yt_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

@app.route('/')
def index():
    return render_template_string(HTML_PREMIUM)

@app.route('/api/info')
def api_info():
    url = request.args.get('url')
    if not url: return jsonify({"success": False})
    try:
        headers = {"x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585", "x-rapidapi-host": "download-all-in-one-lite.p.rapidapi.com"}
        r = requests.get("https://download-all-in-one-lite.p.rapidapi.com/autolink", params={"url": url}, headers=headers, timeout=15)
        data = r.json()
        thumb = data.get("thumbnail")
        if not thumb and ("youtube.com" in url or "youtu.be" in url):
            yid = get_yt_id(url)
            thumb = f"https://img.youtube.com/vi/{yid}/hqdefault.jpg"
        return jsonify({"success": True, "title": data.get("title", "Video"), "thumbnail": thumb})
    except: return jsonify({"success": False})

@app.route('/api/down')
def api_down():
    url = request.args.get('url')
    fmt = request.args.get('type', 'mp4')
    headers = {"x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585"}
    try:
        if "youtube.com" in url or "youtu.be" in url:
            yid = get_yt_id(url)
            headers["x-rapidapi-host"] = "yt-api.p.rapidapi.com"
            r = requests.get("https://yt-api.p.rapidapi.com/dl", params={"id": yid}, headers=headers, timeout=20)
            data = r.json()
            link = None
            if fmt == 'mp3':
                for f in data.get('adaptiveFormats', []):
                    if 'audio' in f.get('mimeType', ''): link = f.get('url'); break
            if not link:
                for f in data.get('formats', []):
                    if 'video' in f.get('mimeType', ''): link = f.get('url'); break
            return jsonify({"url": link or data.get('link')})
        else:
            headers["x-rapidapi-host"] = "download-all-in-one-lite.p.rapidapi.com"
            r = requests.get("https://download-all-in-one-lite.p.rapidapi.com/autolink", params={"url": url}, headers=headers, timeout=20)
            data = r.json()
            medias = data.get("medias", [])
            target = None
            if medias:
                for m in medias:
                    if fmt == 'mp3' and 'audio' in str(m.get('type')).lower(): target = m.get('url'); break
                    if fmt == 'mp4' and 'video' in str(m.get('type')).lower(): target = m.get('url'); break
                if not target: target = medias[0].get('url')
            return jsonify({"url": target})
    except: return jsonify({"error": "Error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
