from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# EL HTML que ya viste, pero con la ruta corregida
HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Motor de Descarga</title>
    <style>
        body { background: #0f0f0f; color: white; font-family: sans-serif; text-align: center; padding: 50px; }
        .card { background: #1a1a1a; padding: 30px; border-radius: 15px; display: inline-block; }
        input { padding: 10px; width: 300px; border-radius: 5px; border: none; }
        button { background: #cc0000; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin-top: 10px; font-weight: bold;}
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 Motor de Descarga</h1>
        <input type="text" id="v" placeholder="Link de YouTube">
        <br>
        <select id="t" style="margin: 10px; padding: 5px;">
            <option value="mp4">Video MP4</option>
            <option value="mp3">Audio MP3</option>
        </select>
        <br>
        <button onclick="doLoad()">DESCARGAR AHORA</button>
        <p id="s"></p>
    </div>
    <script>
        async function doLoad() {
            const val = document.getElementById('v').value;
            const tip = document.getElementById('t').value;
            const st = document.getElementById('s');
            if(!val) return;
            st.innerText = "⏳ Procesando...";
            try {
                // LLAMADA DIRECTA AL SERVIDOR
                const r = await fetch('/descargar?url=' + encodeURIComponent(val) + '&tipo=' + tip);
                const d = await r.json();
                if(d.download_url) {
                    st.innerText = "✅ ¡Listo!";
                    window.location.href = d.download_url;
                } else {
                    st.innerText = "❌ Error: " + (d.error || "No encontrado");
                }
            } catch(e) { st.innerText = "❌ Error de conexión"; }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/descargar')
def descargar():
    u = request.args.get('url')
    t = request.args.get('tipo', 'mp4')
    if not u: return jsonify({"error": "No URL"}), 400
    
    # Limpiar URL
    u = u.split('?si=')[0].split('&')[0]
    
    headers = {
        "x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585",
        "x-rapidapi-host": "auto-download-all-in-one.p.rapidapi.com"
    }
    
    try:
        res = requests.post("https://auto-download-all-in-one.p.rapidapi.com/v1/social/autolink", 
                           json={"url": u}, headers=headers, timeout=15)
        data = res.json()
        links = data.get("result", [])
        if links:
            link = links[0]['url']
            for l in links:
                if t == 'mp3' and (l.get('type') == 'audio' or 'mp3' in str(l.get('extension'))):
                    link = l['url']
                    break
            return jsonify({"download_url": link})
        return jsonify({"error": "No links found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
