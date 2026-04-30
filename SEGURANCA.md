# 🔐 Guia de Segurança e Conformidade LGPD

## 📋 Implementações de Segurança Incluídas

### 1. **Validação de Upload**
```python
# Extensões permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}

# Limite de tamanho
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Nome seguro
filename = secure_filename(f"{int(time.time())}_{arquivo.filename}")
```

### 2. **Deleção Automática (LGPD)**
```python
def delete_file(filepath):
    """Deleta arquivo de forma segura"""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
    except Exception as e:
        print(f"Erro ao deletar: {e}")
    return False

# Chamado após análise
delete_file(filepath)
```

### 3. **Tratamento de Erros Seguro**
- Todos os endpoints possuem try/except
- Garante deleção mesmo em caso de erro
- Não expõe informações sensíveis

### 4. **Proteção de Dados**
- Base64 encoding para transmissão (imagens)
- API Key separada em variáveis
- Sem logs de informações sensíveis

---

## ⚖️ Conformidade LGPD

### Artigos Relevantes Implementados

| Artigo | Descrição | Implementação |
|--------|-----------|----------------|
| Art. 5 | Segurança | Validação e deleção |
| Art. 7 | Consentimento | Mensagem clara no rodapé |
| Art. 17 | Direito ao esquecimento | Deleção imediata |
| Art. 46 | Segurança técnica | Validação de entrada |

### Aviso de Privacidade Incluído

No rodapé do site:
> "Este site não armazena fotos. Todas as imagens são processadas temporariamente e deletadas imediatamente após análise, em conformidade com a LGPD."

---

## 🚨 Boas Práticas Implementadas

### ✅ Feito
1. Deleção de arquivos após processamento
2. Validação rigorosa de entrada
3. Nomes de arquivo seguros
4. Tratamento de exceções
5. Limite de tamanho de arquivo
6. Avisos de privacidade claros
7. Sem armazenamento em banco de dados

### 🔄 Para Aumentar Segurança (Opcional)

#### 1. **Usar HTTPS em Produção**
```python
# Em produção, usar SSL
# pip install pyopenssl
app.run(ssl_context='adhoc')
```

#### 2. **Adicionar CORS**
```python
from flask_cors import CORS
CORS(app)
```

#### 3. **Rate Limiting**
```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=lambda: 'user')

@app.route('/api/verificar-identidade', methods=['POST'])
@limiter.limit("5/minute")
def verificar_identidade():
    pass
```

#### 4. **Logging de Auditoria**
```python
import logging
logging.basicConfig(filename='audit.log', level=logging.INFO)

@app.route('/api/verificar-identidade', methods=['POST'])
def verificar_identidade():
    logging.info(f"Upload realizado em {time.time()}")
```

#### 5. **Compressão de Imagem Antes de Análise**
```python
from PIL import Image
from io import BytesIO

def compress_image(filepath, max_size=(800, 800)):
    img = Image.open(filepath)
    img.thumbnail(max_size)
    img.save(filepath)
```

---

## 🔑 Proteção de Chaves de API

### ❌ NUNCA Faça Isso
```python
# NÃO deixe a chave no código em produção
GROQ_API_KEY = "SUA_API_KEY_AQUI"
```

### ✅ Faça Assim
```python
# Use variáveis de ambiente
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
```

### Arquivo .env
```
GROQ_API_KEY=sua_chave_aqui
SERPAPI_API_KEY=sua_chave_aqui
```

### .gitignore
```
.env
uploads/
__pycache__/
*.pyc
.DS_Store
```

---

## 📊 Checklist de Segurança para Produção

- [ ] Chaves de API em variáveis de ambiente
- [ ] HTTPS habilitado
- [ ] Rate limiting ativo
- [ ] Logging de auditoria
- [ ] Backup de código
- [ ] Validação frontend + backend
- [ ] Testes de penetração
- [ ] Política de privacidade atualizada
- [ ] Termo de uso claro
- [ ] CORS configurado corretamente

---

## 🧪 Testar Segurança

### Teste 1: Validação de Arquivo
```bash
# Tentar upload de .exe (deve falhar)
curl -F "imagem=@malware.exe" http://localhost:5000/api/verificar-identidade
# Resultado esperado: "Tipo de arquivo não permitido"
```

### Teste 2: Arquivo Grande
```bash
# Tentar arquivo > 10MB (deve falhar)
# Resultado esperado: 413 Payload Too Large
```

### Teste 3: Deleção de Arquivo
```python
# Verificar pasta uploads após análise
# Resultado esperado: Vazia (arquivos deletados)
```

---

## 📝 Política de Privacidade (Modelo)

```
Política de Privacidade - Detetive de Identidade Digital

1. COLETA DE DADOS
   - Coletamos apenas imagens enviadas pelo usuário
   - As imagens são processadas temporariamente

2. ARMAZENAMENTO
   - NÃO armazenamos imagens no servidor
   - Arquivos são deletados imediatamente após análise

3. COMPARTILHAMENTO
   - Dados são enviados apenas para SerpApi e Groq
   - Consulte políticas desses serviços

4. DIREITOS DO USUÁRIO
   - Direito ao esquecimento: Implementado
   - Direito de acesso: Não aplicável (sem armazenamento)
   - Direito a correção: Contato direto

5. CONTATO
   - Para questões de privacidade: seu_email@email.com
   - Conformidade LGPD: sim
```

---

## 🔍 Monitoramento

### Logs Importantes
```python
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@app.route('/api/verificar-identidade', methods=['POST'])
def verificar_identidade():
    logger.info("Upload iniciado")
    # ... código ...
    logger.info("Upload concluído e deletado")
```

---

## 🚀 Deployment Seguro

### 1. **Usar Gunicorn em Produção**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 detetive:app
```

### 2. **Configurar Nginx (Reverse Proxy)**
```nginx
server {
    listen 443 ssl;
    server_name seu_dominio.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

### 3. **Docker (Opcional)**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=detetive.py
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "detetive:app"]
```

---

## 📞 Suporte à Segurança

Se encontrar vulnerabilidades:
1. NÃO publique no GitHub/redes públicas
2. Reporte de forma responsável
3. Aguarde patch antes de divulgar

---

**Segurança em primeiro lugar! 🔐**
