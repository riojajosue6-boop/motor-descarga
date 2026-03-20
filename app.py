import os
import requests
import re
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# --- DISEÑO PREMIUM CORREGIDO ---
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
        .container { padding: 20px; max-width: 800px; margin: 0 auto; }
        .main-card { background: var(--gray); padding: 40px; border-radius: 25px; border: 1px solid #333; margin: 10px auto; box-shadow: 0 20px 60px rgba(0,0,0,0.8); }
        h1 { color: var(--red); font-size: 32px; margin-bottom: 20px; }
        input { width: 100%; padding: 18px; border-radius: 12px; border: 1px solid #333; background: #222; color: #fff; font-size: 16px; box-sizing: border-box; margin-bottom: 20px; outline: none; }
        #btnAction { width: 100%; padding: 18px; background: var(--red); color: white; border: none; border-radius: 12px; font-weight: bold; font-size: 18px; cursor: pointer; }
        
        #errorMessage { display: none; background: #2a1010; color: #ff9999; border: 1px solid #ff0000; padding: 20px; border-radius: 15px; margin-top: 20px; text-align: left; }
        #supportBox { display: none; background: #1a2a1a; color: #99ff99; border: 1px solid #00aa00; padding: 20px; border-radius: 15px; margin: 20px 0; font-size: 14px; }
        #countdownText { font-weight: bold; color: #fff; font-size: 16px; margin-top: 10px; display: block; }

        #previewSection { display: none; margin-top: 30px; border-top: 1px solid #333; padding-top: 20px; }
        #videoThumbnail { width: 100%; max-width: 400px; border-radius: 15px; border: 1px solid #444; }
        #finalDownloadBtn { width: 100%; padding: 15px; background: #00aa00; color: white; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; margin-top: 15px; }
        #finalDownloadBtn:disabled { background: #333; color: #777; cursor: not-allowed; }
        
        footer { padding: 40px; color: #444; font-size: 12px; }
    </style>
</head>
<body>
    <nav><a onclick="location.reload()">Inicio</a></nav>

    <div class="container">
        <div class="main-card">
            <h1>🚀 MOTOR DE DESCARGA</h1>
            <input type="text" id="urlInput" placeholder="Pega el enlace aquí...">
            <div style="display:flex; gap:10px; margin-bottom:20px;">
                <select id="formatInput" style="padding:15px; border-radius:10px; background:#222; color:white; border:1px solid #444; flex:1;">
                    <option value="mp4">🎬 Video MP4</option>
                    <option value="mp3">🎵 Audio MP3</option>
                </select>
            </div>
            <button id="btnAction" onclick="processVideo()">PROCESAR VIDEO</button>
            <div id="status" style="margin-top:20px; font-weight:bold;"></div>
            
            <div id="errorMessage">
                <strong>⚠️ Aviso del Sistema:</strong><br>
                No pudimos procesar este enlace específico. Esto ocurre a veces por restricciones de la plataforma original. ¡Intenta con otro video!
            </div>

            <div id="previewSection">
                <img id="videoThumbnail" src="">
                <div id="videoTitle" style="margin-bottom:15px; font-weight:bold; color:#fff;"></div>
                
                <div id="supportBox">
                    ❤️ <strong>¡Gracias por tu apoyo!</strong><br>
                    Tómate unos segundos para ver nuestra publicidad, esto mantiene el servicio gratuito.
                    <span id="countdownText">El botón se activará en 5...</span>
                </div>

                <button id="finalDownloadBtn" disabled>CONFIRMAR DESCARGA</button>
            </div>
        </div>
    </div>

    <footer>© 2026 Descargador Pro - Cochabamba 🇧🇴</footer>

    <script>
        let globalUrl = "";

        async function processVideo() {
            const url = document.getElementById('urlInput').value;
            const s = document.getElementById('status');
            const p = document.getElementById('previewSection');
            const err = document.getElementById('errorMessage');
            const box = document.getElementById('supportBox');
            const dBtn = document.getElementById('finalDownloadBtn');
            
            if(!url) return alert("Pega un link");
            globalUrl = url;
            
            p.style.display = 'none';
            err.style.display = 'none';
            s.innerText = "⏳ Analizando...";

            try {
                const res = await fetch('/api/info?url=' + encodeURIComponent(url));
                const info = await res.json();
                if(info.success) {
                    document.getElementById('videoThumbnail').src = info.thumbnail;
                    document.getElementById('videoTitle').innerText = info.title;
                    p.style.display = 'block';
                    box.style.display = 'block';
                    s.innerText = "✅ Detectado";
                    
                    let timeLeft = 5;
                    dBtn.disabled = true;
                    dBtn.innerText = "ESPERA 5 seg...";
                    
                    const countdown = setInterval(() => {
                        timeLeft--;
                        document.getElementById('countdownText').innerText = `El botón se activará en ${timeLeft}...`;
                        if(timeLeft <= 0) {
                            clearInterval(countdown);
                            document.getElementById('countdownText').style.display = 'none';
                            dBtn.disabled = false;
                            dBtn.innerText = "DESCARGAR AHORA";
                        }
                    }, 1000);

                    dBtn.onclick = () => generateDownload(url, document.getElementById('formatInput').value);
                } else { s.innerText = ""; err.style.display = 'block'; }
            } catch (e) { s.innerText = "❌ Error."; err.style.display = 'block'; }
        }

        async function generateDownload(url, tipo) {
            const s = document.getElementById('status');
            const err = document.getElementById('errorMessage');
            s.innerText = "🚀 Generando descarga...";
            try {
                const res = await fetch(`/api/down?url=${encodeURIComponent(url)}&type=${tipo}`);
                const data = await res.json();
                if(data.url) {
                    // REDIRECCIÓN DIRECTA PARA FB/IG/TK/YT
                    // Esto evita el Error 403 por validación JS
                    window.open(data.url, '_blank');
                    s.innerText = "✅ Descarga abierta en pestaña nueva";
                } else { s.innerText = ""; err.style.display = 'block'; }
            } catch (e) { s.innerText = ""; err.style.display = 'block'; }
        }
    </script>
</body>
</html>
