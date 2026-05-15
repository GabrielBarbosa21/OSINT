import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import base64

load_dotenv()

# AJUSTE VERCEL: Se não achar no .env local, ele pega as chaves secretas do painel do Vercel
SERPAPI_API_KEY = os.getenv("SERPAPI_KEY", "chave")
IMGBB_API_KEY = os.getenv("IMGBB_KEY", "chave")

prefixo_chave = SERPAPI_API_KEY[:6]

def buscar_yandex(url):
    """Busca imagens no SerpApi usando o mecanismo Yandex Images."""
    params = {
        "engine": "yandex_images",
        "url": url,
        "api_key": SERPAPI_API_KEY
    }
    try:
        response = requests.get("https://serpapi.com/search", params=params, timeout=20)
        response.raise_for_status()
        data = response.json()
        matches = data.get("image_results") or data.get("images_results") or []
        
        resultados = []
        for m in matches[:100]:
            resultados.append({
                "title": m.get("title"),
                "link": m.get("link"),
                "source": m.get("source"),
                "thumbnail": m.get("thumbnail")
            })
        return resultados
    except Exception:
        return [] # Se o Yandex falhar, o site não quebra e continua com o Google Lens

# Cria o aplicativo Flask
app = Flask(__name__)

# AJUSTE VERCEL: Na nuvem, a única pasta que permite salvar arquivos temporários é a /tmp
UPLOAD_FOLDER = '/tmp'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/verificar-identidade', methods=['POST'])
def verificar_identidade():
    logs = []
    
    if not SERPAPI_API_KEY or prefixo_chave not in SERPAPI_API_KEY:
        logs.append("❌ Erro: Chave SerpApi inválida ou não encontrada.")
        return jsonify({"erro": "Configuração de API pendente", "logs": logs}), 500

    if 'imagem' not in request.files:
        return jsonify({"erro": "Nenhuma imagem enviada", "logs": ["❌ Erro: Arquivo não recebido"]}), 400

    foto = request.files['imagem']
    filepath = os.path.join(UPLOAD_FOLDER, foto.filename)
    foto.save(filepath)
    
    logs.append(f"📤 Imagem '{foto.filename}' recebida.")

    try:
        logs.append("☁️ Gerando link público via ImgBB...")
        
        with open(filepath, 'rb') as f:
            img_data = f.read()
            payload = {
                "key": IMGBB_API_KEY,
                "image": base64.b64encode(img_data)
            }
            
            try:
                up = requests.post('https://api.imgbb.com/1/upload', data=payload, timeout=20)
                up.raise_for_status()
                json_data = up.json()
                url_publica = json_data['data']['url']
                logs.append(f"🔗 Link gerado: {url_publica}")
            except Exception as e:
                logs.append(f"❌ Erro no upload ImgBB: {str(e)}")
                return jsonify({"erro": "Falha no upload da imagem", "logs": logs}), 500

        logs.append("🔎 Consultando SerpApi (Google Lens) e Yandex...")

        # Chamada Google Lens
        params = {
            "engine": "google_lens",
            "url": url_publica,
            "api_key": SERPAPI_API_KEY
        }
        response = requests.get("https://serpapi.com/search", params=params, timeout=20)
        response.raise_for_status()
        data = response.json()
        matches = data.get("visual_matches", [])

        resultados_lens = []
        for m in matches[:100]:
            resultados_lens.append({
                "title": m.get("title"),
                "link": m.get("link"),
                "source": m.get("source"),
                "thumbnail": m.get("thumbnail")
            })

        resultados_yandex = buscar_yandex(url_publica)
        logs.append(f"✅ Busca Google Lens: {len(resultados_lens)} resultados; Yandex: {len(resultados_yandex)} resultados.")

        # Unifica e remove duplicados
        resultados_finais = []
        links_vistos = set()
        for item in resultados_lens + resultados_yandex:
            link = item.get("link")
            if not link or link in links_vistos:
                continue
            links_vistos.add(link)
            resultados_finais.append(item)

        # Limpeza LGPD
        if os.path.exists(filepath):
            os.remove(filepath)

        # CORREÇÃO DO ERRO JSON: Retornando o jsonify correto para o sucesso
        return jsonify({
            "sucesso": True,
            "risco": "MÉDIO" if len(resultados_finais) > 0 else "BAIXO",
            "analise": f"Foram encontrados {len(resultados_finais)} sites com imagens similares.",
            "detalhes": resultados_finais,
            "logs": logs
        })

    except Exception as e:
        if os.path.exists(filepath): os.remove(filepath)
        return jsonify({"erro": str(e), "logs": [f"💥 Erro: {str(e)}"]}), 500

# AJUSTE VERCEL: Necessário para a nuvem reconhecer o ponto de partida do Flask
app.debug = True
