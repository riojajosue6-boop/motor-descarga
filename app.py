import os
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

API_KEY = "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585"
API_HOST = "auto-download-all-in-one.p.rapidapi.com"
user_stats = {} 

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TurboLink 🚀</title>
    <style>
        :root { --primary: #00f2ea; --bg: #0a0a0a; --card: #151515; }
        body { background: var(--bg); color: #fff; font-family: sans-serif; margin: 0; padding: 20px; text-align: center; }
        .container { max-width: 500px; margin: auto; background: var(--card); padding: 30px; border-radius: 25px; border: 1px solid #333; }
        h1 { color: var(--primary); text-transform: uppercase; text-shadow: 0 0 10px var(--primary); }
        input { width: 100%; padding: 18px; border-radius: 15px; border: 2px solid #222; background: #1a1a1a; color: #fff; box-sizing: border-box; margin: 20px 0; font-size: 16px; }
        button { width: 100%; padding: 18px; background: var(--primary); color: #000; border: none; border-radius: 15px; font-weight: bold; cursor: pointer; text-transform: uppercase; }
        #timer-msg { display: none; margin-top: 20px; padding: 15px; border: 1px dashed var(--primary); border-radius: 15px; background: rgba(0,242,234,0.05); }
        .dl-box { background: #2ecc71; color: #000; padding: 25px; border-radius: 20px; margin-top: 20px; }
        .dl-btn { background: #000; color: #fff; padding: 15px 30px; text-decoration: none; border-radius: 12px; font-weight: bold; display: block; margin-top: 15px; border: none; width: 100%; font-size: 16px; cursor: pointer; }
        .instruction { font-size: 13px; color: #333; margin-top: 15px; line-height: 1.4; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>TURBOLINK</h1>
        <p style="color:#666; font-size:12px;">DESCARGAS SEGURAS 🇧🇴</p>
        <input type="text" id="urlInput" placeholder="Pega el link aquí...">
        <button id="mainBtn" onclick="startProcess()">GENERAR DESCARGA</button>
        
        <div id="timer-msg">
            🚀 Procesando enlace...
            <h2 id="countdown" style="color:var(--primary); font-size: 40px; margin: 10px 0;">15</h2>
            <small>Espera un momento para activar el botón.</small>
        </div>

        <div id="status"></div>
    </div>

    <script>
        async function startProcess() {
            const url = document.getElementById('urlInput').value.trim();
            if(!url) return alert("Pega un link primero");
            const btn = document.getElementById('mainBtn');
            const timerMsg = document.getElementById('timer-msg');
            const status = document.getElementById('status');
            
            btn.disabled = true; status.innerHTML = ""; timerMsg.style.display = "block";
            
            let timeLeft = 15;
            let timer = setInterval(async () => {
                timeLeft--; document.getElementById('countdown').innerText = timeLeft;
                if(timeLeft <= 0) {
                    clearInterval(timer); timerMsg.style.display = "none";
                    await callAPI(url); btn.disabled = false;
                }
            }, 1000);
        }

        async function callAPI(url) {
            const status = document.getElementById('status');
            status.innerHTML = "⏳ Extrayendo video...";
            try {
                const response = await fetch('/api/fetch?url=' + encodeURIComponent(url));
                const data = await response.json();
                if(data.success) {
                    status.innerHTML = `
                        <div class="dl-box">
                            <p style="margin:0; font-size:18px; font-weight:bold;">✅ ¡ARCHIVO LISTO!</p>
                            
                            <a href="${data.download_url}" target="_blank" rel="noopener noreferrer" download="video.mp4" class="dl-btn">
                                📥 DESCARGAR VIDEO AHORA
                            </a>

                            <div class="instruction">
                                ⚠️ SI SE ABRE LA APP O EL VIDEO:<br>
                                1. Regresa a esta página.<br>
                                2. Mantén presionado el botón negro.<br>
                                3. Elige <b>"Descargar vínculo"</b>.
                            </div>
                        </div>`;
                } else { status.innerHTML = "<p style='color:red; margin-top:20px;'>❌ " + data.message + "</p>"; }
            } catch(e) { status.innerHTML = "<p style='color:red; margin-top:20px;'>❌ Error en el motor.</p>"; }
        }
    </script>
</body>
</html>
'''

@app.route('/api/fetch')
def fetch_link():
    url = request.args.get('url')
    headers = {"content-type": "application/json", "x-rapidapi-host": API_HOST, "x-rapidapi-key": API_KEY}
    try:
        r = requests.post(f"https://{API_HOST}/v1/social/autolink", json={"url": url}, headers=headers, timeout=15)
        res = r.json()
        video_url = res.get('url')
        if video_url:
            return jsonify({"success": True, "download_url": video_url})
        return jsonify({"success": False, "message": "No se encontró el video público."})
    except: return jsonify({"success": False, "message": "Error de conexión."})

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
