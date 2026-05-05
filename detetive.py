import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import base64

load_dotenv()

# CORREÇÃO AQUI: 
# Opção A: Se você tem um arquivo .env, use: SERPAPI_API_KEY = os.getenv("SERPAPI_KEY")
# Opção B (Mais rápida para testar): Coloque a chave direto na variável:
SERPAPI_API_KEY = "SUA_CHAVE"  # Substitua pela sua chave real
prefixo_chave = SERPAPI_API_KEY[:6]


def buscar_yandex(url):
    """Busca imagens no SerpApi usando o mecanismo Yandex Images."""
    params = {
        "engine": "yandex_images",
        "url": url,
        "api_key": SERPAPI_API_KEY
    }
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


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/verificar-identidade', methods=['POST'])
def verificar_identidade():
    logs = []
    
    # Validação da chave
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


# ... dentro da sua função ...

        # PASSO 1: Link público via ImgBB
        logs.append("☁️ Gerando link público via ImgBB...")
        
        with open(filepath, 'rb') as f:
            # Lendo a imagem e convertendo para base64
            img_data = f.read()
            
            payload = {
                "key": "SUA_CHAVE", # Substitua pela sua chave do ImgBB
                "image": base64.b64encode(img_data)
            }
            
            try:
                up = requests.post('https://api.imgbb.com/1/upload', data=payload, timeout=20)
                up.raise_for_status() # Garante que o request funcionou
                
                json_data = up.json()
                url_publica = json_data['data']['url']
                
                logs.append(f"🔗 Link gerado: {url_publica}")
                
            except Exception as e:
                logs.append(f"❌ Erro no upload: {str(e)}")
                # Aqui você pode tratar o erro ou retornar
                return "Erro ao processar imagem"

        logs.append("🔎 Consultando SerpApi (Google Lens) e Yandex...")

        # PASSO 2: Chamada para a SerpApi Google Lens
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
        for m in matches[:1000]:  # Limitando a 100 resultados para evitar sobrecarga
            resultados_lens.append({
                "title": m.get("title"),
                "link": m.get("link"),
                "source": m.get("source"),
                "thumbnail": m.get("thumbnail")
            })

        resultados_yandex = buscar_yandex(url_publica)
        logs.append(f"✅ Busca Google Lens: {len(resultados_lens)} resultados; Yandex: {len(resultados_yandex)} resultados.")

        # Combina resultados e remove links duplicados
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

        return jsonify({
            "sucesso": True,
            "risco": "MÉDIO" if len(matches) > 0 else "BAIXO",
            "analise": f"Foram encontrados {len(matches)} sites com imagens similares.",
            "detalhes": resultados_finais,
            "logs": logs
        })

    except Exception as e:
        return jsonify({"erro": str(e), "logs": [f"💥 Erro: {str(e)}"]}), 500
if __name__ == '__main__':
    app.run(debug=True)
