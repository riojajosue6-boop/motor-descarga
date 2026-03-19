import os
import requests
import re
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# --- PLANTILLA HTML/CSS/JS TODO-EN-UNO (DISEÑO PREMIUM) ---
HTML_PREMIUM = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Descargador Pro | Bolivia</title>
    <style>
        :root { --red: #ff0000; --dark: #0a0a0a; --gray: #1a1a1a; --text: #eee; }
        body { background: var(--dark); color: var(--text); font-family: 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 0; text-align: center; }
        
        /* Nav & Footer */
        nav { background: #000; padding: 15px; border-bottom: 1px solid #333; }
        nav a { color: #888; margin: 0 15px; text-decoration: none; font-size: 14px; cursor: pointer; }
        nav a:hover { color: var(--red); }
        footer { padding: 40px; color: #444; font-size: 12px; border-top: 1px solid #222; margin-top: 40px; }

        /* Contenedor Principal */
        .main-card { background: var(--gray); padding: 40px; border-radius: 25px; display: inline-block; border: 1px solid #333; max-width: 550px; width: 90%; margin: 20px auto; box-shadow: 0 20px 60px rgba(0,0,0,0.8); }
        h1 { color: var(--red); margin: 0 0 10px 0; font-size: 36px; text-transform: uppercase; letter-spacing: 1px; }
        .subtitle { color: #888; margin-bottom: 30px; font-size: 16px; }

        /* Input y Selector */
        .input-group { position: relative; margin-bottom: 20px; }
        input { width: 100%; padding: 18px; border-radius: 12px; border: 1px solid #333; background: #222; color: #fff; font-size: 16px; box-sizing: border-box; outline: none; transition: 0.3s; }
        input:focus { border-color: var(--red); box-shadow: 0 0 10px rgba(255,0,0,0.3); }
        
        .options { display: flex; gap: 10px; margin-bottom: 25px; justify-content: center; }
        select { padding: 15px; border-radius: 10px; background: #222; color: white; border: 1px solid #444; flex: 1; cursor: pointer; font-size: 15px; }

        /* Botón Principal */
        #btnAction { width: 100%; padding: 18px; background: var(--red); color: white; border: none; border-radius: 12px; font-weight: bold; font-size: 18px; cursor: pointer; transition: 0.3s; text-transform: uppercase; }
        #btnAction:hover { background: #cc0000; transform: translateY(-2px); }
        #btnAction:disabled { background: #444; cursor: not-allowed; transform: none; }

        /* Sección de Previsulización (Thumbnail) */
        #previewSection { display: none; margin-top: 30px; padding-top: 30px; border-top: 1px solid #333; text-align: left; }
        #videoThumbnail { width: 100%; border-radius: 15px; border: 1px solid #444; margin-bottom: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.5); }
        #videoTitle { font-weight: bold; color: #fff; margin-bottom: 5px; font-size: 16px; }
        #videoSource { color: #666; font-size: 14px; text-transform: uppercase; margin-bottom: 15px; }
        
        #finalDownloadBtn { width: 100%; padding: 15px; background: #00aa00; color: white; border: none; border-radius: 10px; font-weight: bold; font-size: 16px; cursor: pointer; text-decoration: none; display: inline-block; text-align: center; box-sizing: border-box; }
        #finalDownloadBtn:hover { background: #008800; }

        /* Estado y Carga */
        #status { margin-top: 25px; font-weight: bold; min-height: 24px; font-size: 15px; }
        .loader { border: 4px solid #333; border-top: 4px solid var(--red); border-radius: 50%; width: 30px; height: 30px; animation: spin 1s linear infinite; display: inline-block; vertical-align: middle; margin-right: 10px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform
