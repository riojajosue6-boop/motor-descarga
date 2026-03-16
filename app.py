from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import yt_dlp
import os
import tempfile

app = Flask(__name__)
CORS(app) # Esto permite que tu página web hable con este servidor

@app.route('/descargar', methods=['GET'])
def descargar():
    url = request.args.get('url')
    tipo = request.args.get('tipo') # 'mp4' o 'mp3'
    
    if not url:
        return jsonify({"error": "No se proporcionó URL"}), 400

    # Carpeta temporal para no llenar el disco del servidor
    tmpdir = tempfile.gettempdir()
    
    ydl_opts = {
        'outtmpl': f'{tmpdir}/%(title)s.%(ext)s',
        'quiet': True,
    }

    if tipo == 'mp3':
        ydl_status = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:
        # Mejor calidad de video (combinando video y audio)
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            archivo = ydl.prepare_filename(info)
            
            # Si fue MP3, el nombre cambia a .mp3
            if tipo == 'mp3':
                archivo = archivo.rsplit('.', 1)[0] + '.mp3'

            return send_file(archivo, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
