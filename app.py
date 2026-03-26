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
        h1 { color: var(--primary); text-transform: uppercase; }
        input { width: 100%; padding: 18px; border-radius: 15px; border: 2px solid #222; background: #1a1a1a; color: #fff; box-sizing: border-box; margin: 20px 0; }
        button { width: 100%; padding: 18px; background: var(--primary); color: #000; border: none; border-radius: 15px; font-weight: bold; cursor: pointer; }
        #timer-msg { display: none; margin-top: 20px; padding: 15px; border: 1px dashed var(--primary); border-radius: 15px; }
        .dl-box { background: #2ecc71; color: #000; padding: 20px; border-radius: 15px; margin-top: 20px; }
        .dl-btn { background: #000; color: #fff; padding: 12px 25px; text-decoration: none; border-radius: 10px; font-weight: bold; display: inline-block; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>TURBOLINK</h1>
        <input type="text" id="urlInput" placeholder="Pega el link aquí...">
        <button id="mainBtn" onclick="startProcess()">Arrancar Motor</button>
        <div id="timer-msg">🚀 Preparando descarga... <h2 id="countdown" style="color:var(--primary);">15</h2></div>
        <div id="status"></div>
    </div>

    <script>
        async function startProcess() {
            const url = document.getElementById('urlInput').value.trim();
            if(!url) return alert("Pega un link");
            const btn = document.getElementById('mainBtn');
            const timerMsg = document.getElementById('timer-msg');
            btn.disabled = true; timerMsg.style.display = "block";
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
            status.innerHTML = "⏳ Extrayendo...";
            try {
                const response = await fetch('/api/fetch?url=' + encodeURIComponent(url));
                const data = await response.json();
                if(data.success) {
                    // EL TRUCO: Usamos una función de JS para forzar al navegador a bajar el blob
                    status.innerHTML = `
                        <div class="dl-box">
                            <p style="margin:0; font-weight:bold;">✅ ¡Enlace Listo!</p>
                            <button onclick="forceDownload('${data.download_url}')" class="dl-btn">📥 DESCARGAR VIDEO</button>
                            <p style="font-size:10px; margin-top:10px;">Si no inicia, mantén presionado y dale a "Descargar vínculo".</p>
                        </div>`;
                } else { status.innerHTML = "❌ " + data.message; }
            } catch(e) { status.innerHTML = "❌ Error en el motor."; }
        }

        async function forceDownload(videoUrl) {
            const status = document.getElementById('status');
            status.innerHTML = "⏳ Iniciando descarga en tu dispositivo...";
            
            // Esto intenta descargar el video directamente desde el navegador del usuario
            // saltando el bloqueo de servidor.
            const link = document.createElement('a');
            link.href = videoUrl;
            link.setAttribute('download', 'TurboLink_Video.mp4');
            link.setAttribute('target', '_blank');
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/fetch')
def fetch_link():
    url = request.args.get('url')
    user_ip = request.remote_addr
    if user_ip not in user_stats: user_stats[user_ip] = {'yt': 0, 'social': 0}
    
    is_yt = "youtube.com" in url or "youtu.be" in url
    if is_yt and user_stats[user_ip]['yt'] >= 3: return jsonify({"success": False, "message": "Límite YT."})
    if not is_yt and user_stats[user_ip]['social'] >= 4: return jsonify({"success": False, "message": "Límite Redes."})

    headers = {"content-type": "application/json", "x-rapidapi-host": API_HOST, "x-rapidapi-key": API_KEY}
    try:
        r = requests.post(f"https://{API_HOST}/v1/social/autolink", json={"url": url}, headers=headers, timeout=15)
        res = r.json()
        video_url = res.get('url')
        if video_url:
            if is_yt: user_stats[user_ip]['yt'] += 1
            else: user_stats[user_ip]['social'] += 1
            return jsonify({"success": True, "download_url": video_url, "stats": user_stats[user_ip]})
        return jsonify({"success": False, "message": "No se encontró el video."})
    except: return jsonify({"success": False, "message": "Error API."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
