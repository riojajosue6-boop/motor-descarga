import os
import requests
from flask import Flask, request, jsonify, render_template_string, Response, stream_with_context

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
    <title>TurboLink 🚀 | Ahorro Activo</title>
    <style>
        :root { --primary: #00f2ea; --bg: #0a0a0a; --card: #151515; }
        body { background: var(--bg); color: #fff; font-family: sans-serif; margin: 0; padding: 20px; text-align: center; }
        .container { max-width: 500px; margin: auto; background: var(--card); padding: 30px; border-radius: 25px; border: 1px solid #333; }
        input { width: 100%; padding: 18px; border-radius: 15px; border: 2px solid #222; background: #1a1a1a; color: #fff; box-sizing: border-box; margin: 20px 0; }
        #mainBtn { width: 100%; padding: 18px; background: var(--primary); color: #000; border: none; border-radius: 15px; font-weight: bold; cursor: pointer; }
        #timer-msg { display: none; margin-top: 20px; padding: 15px; border: 1px dashed var(--primary); border-radius: 15px; }
        .dl-box { background: #2ecc71; color: #000; padding: 25px; border-radius: 20px; margin-top: 20px; }
        .dl-btn { background: #000; color: #fff; padding: 15px 30px; text-decoration: none; border-radius: 12px; font-weight: bold; display: block; margin-top: 15px; }
        .alert-box { background: #f39c12; color: #000; padding: 15px; border-radius: 15px; margin-top: 15px; font-size: 13px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>TURBOLINK</h1>
        <p style="color:var(--primary); font-size:12px;">PROTECCIÓN DE DATOS NIVEL PRO 🛡️</p>
        <input type="text" id="urlInput" placeholder="Pega el link aquí...">
        <button id="mainBtn" onclick="startProcess()">GENERAR VIDEO</button>
        <div id="timer-msg">🚀 Preparando motor... <h2 id="countdown" style="color:var(--primary);">15</h2></div>
        <div id="status"></div>
    </div>

    <script>
        async function startProcess() {
            const url = document.getElementById('urlInput').value.trim();
            if(!url) return alert("Pega un link");
            const btn = document.getElementById('mainBtn');
            btn.disabled = true; document.getElementById('timer-msg').style.display = "block";
            let timeLeft = 15;
            let timer = setInterval(async () => {
                timeLeft--; document.getElementById('countdown').innerText = timeLeft;
                if(timeLeft <= 0) {
                    clearInterval(timer); document.getElementById('timer-msg').style.display = "none";
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
                    let btnHtml = "";
                    if(data.method === "tunnel") {
                        // MODO TIKTOK: Usa el 1GB pero asegura descarga
                        btnHtml = `<a href="/api/download?video_url=${encodeURIComponent(data.download_url)}" class="dl-btn">📥 GUARDAR TIKTOK</a>`;
                    } else {
                        // MODO YT/FB: NO usa tu 1GB (Ahorro total)
                        btnHtml = `
                            <a href="${data.download_url}" target="_blank" class="dl-btn">📥 DESCARGAR VIDEO</a>
                            <div class="alert-box">
                                ⚠️ ATENCIÓN:<br>Si se abre la app, regresa aquí, mantén presionado el botón negro y elige "Descargar vínculo".
                            </div>`;
                    }
                    status.innerHTML = `<div class="dl-box"><b>✅ ¡LISTO!</b>${btnHtml}</div>`;
                } else { status.innerHTML = "❌ " + data.message; }
            } catch(e) { status.innerHTML = "❌ Error."; }
        }
    </script>
</body>
</html>
'''

@app.route('/api/fetch')
def fetch_link():
    url = request.args.get('url')
    headers = {"content-type": "application/json", "x-rapidapi-host": API_HOST, "x-rapidapi-key": API_KEY}
    is_tiktok = "tiktok.com" in url
    try:
        r = requests.post(f"https://{API_HOST}/v1/social/autolink", json={"url": url}, headers=headers, timeout=15)
        res = r.json()
        video_url = res.get('url')
        if video_url:
            return jsonify({"success": True, "download_url": video_url, "method": "tunnel" if is_tiktok else "redirect"})
        return jsonify({"success": False, "message": "No encontrado."})
    except: return jsonify({"success": False, "message": "Error API."})

@app.route('/api/download')
def download_video():
    # Este túnel solo se activa para TikTok, protegiendo tu Giga
    video_url = request.args.get('video_url')
    req = requests.get(video_url, headers={'User-Agent': 'Mozilla/5.0'}, stream=True, timeout=30)
    def generate():
        for chunk in req.iter_content(chunk_size=1024*1024): yield chunk
    response = Response(stream_with_context(generate()), content_type='video/mp4')
    response.headers['Content-Disposition'] = 'attachment; filename="TurboLink_TikTok.mp4"'
    return response

@app.route('/')
def home(): return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
