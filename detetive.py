import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

# CORREÇÃO AQUI: 
# Opção A: Se você tem um arquivo .env, use: SERPAPI_API_KEY = os.getenv("SERPAPI_KEY")
# Opção B (Mais rápida para testar): Coloque a chave direto na variável:
SERPAPI_API_KEY = "GROQ_API_KEY=your_api_key_here
"

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
    if not SERPAPI_API_KEY or "6f15cf" not in SERPAPI_API_KEY:
        logs.append("❌ Erro: Chave SerpApi inválida ou não encontrada.")
        return jsonify({"erro": "Configuração de API pendente", "logs": logs}), 500

    if 'imagem' not in request.files:
        return jsonify({"erro": "Nenhuma imagem enviada", "logs": ["❌ Erro: Arquivo não recebido"]}), 400

    foto = request.files['imagem']
    filepath = os.path.join(UPLOAD_FOLDER, foto.filename)
    foto.save(filepath)
    
    logs.append(f"📤 Imagem '{foto.filename}' recebida.")

    try:
        # PASSO 1: Link temporário (Catbox é bom, mas vamos garantir o timeout)
        logs.append("☁️ Gerando link público para o Google Lens...")
        with open(filepath, 'rb') as f:
            # Usando o serviço transfer.sh como alternativa rápida caso o catbox falhe
            up = requests.post('https://catbox.moe/user/api.php', 
                               data={'reqtype': 'fileupload'}, 
                               files={'fileToUpload': f}, timeout=15)
            url_publica = up.text.strip()
        
        logs.append(f"🔗 Link gerado: {url_publica}")
        logs.append("🔎 Consultando SerpApi (Google Lens)...")

        # PASSO 2: Chamada real para a API
        params = {
            "engine": "google_lens",
            "url": url_publica,
            "api_key": SERPAPI_API_KEY
        }
        
        response = requests.get("https://serpapi.com/search", params=params, timeout=20)
        data = response.json()

        # Extraindo resultados
        matches = data.get("visual_matches", [])
        logs.append(f"✅ Busca concluída. {len(matches)} resultados encontrados.")

        resultados_finais = []
        for m in matches[:8]:
            resultados_finais.append({
                "title": m.get("title"),
                "link": m.get("link"),
                "source": m.get("source"),
                "thumbnail": m.get("thumbnail") # Essa é a imagem que vai aparecer no seu site
            })

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
