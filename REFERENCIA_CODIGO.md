# 🔍 Referência Rápida de Código

## Backend (detetive.py) - Funções Principais

### 1. **Upload e Validação**
```python
@app.route('/api/verificar-identidade', methods=['POST'])
def verificar_identidade():
    # Validar arquivo
    # Salvar com nome seguro
    # Processar com SerpApi
    # Analisar com Groq
    # Deletar arquivo
    # Retornar resultado
```

### 2. **Busca Reversa com SerpApi**
```python
def search_image_with_serpapi(image_path):
    image_base64 = image_to_base64(image_path)
    params = {
        "api_key": SERPAPI_API_KEY,
        "engine": "google_lens",
        "image": image_base64
    }
    # Retorna visual_matches com links, títulos e fontes
```

### 3. **Análise com Groq**
```python
def analyze_with_groq(visual_matches):
    # Formata dados dos matches
    # Envia prompt para Groq
    # Retorna análise com:
    #   - Risco (BAIXO/MÉDIO/ALTO/CRÍTICO)
    #   - Análise de identidade
    #   - Bandeiras vermelhas
    #   - Recomendações
```

### 4. **Deleção (LGPD)**
```python
def delete_file(filepath):
    # Remove arquivo após análise
    # Conformidade LGPD
    # Garante privacidade do usuário
```

---

## Frontend (index.html) - Seções

### 1. **HTML Structure**
```html
<form id="formUpload" enctype="multipart/form-data">
    <!-- Input de arquivo com drag-drop -->
    <!-- Botão de verificação -->
</form>

<div class="resultado">
    <!-- Exibe análise formatada -->
</div>

<div class="erro">
    <!-- Exibe mensagens de erro -->
</div>
```

### 2. **CSS Destacado**
- Dark Mode: `linear-gradient(135deg, #0a0e27 0%, #16213e 100%)`
- Cor primária: `#00d4ff` (ciano)
- Animações suaves (fadeIn, spin, slideIn)
- Responsivo para mobile/tablet

### 3. **JavaScript - Principais Funções**
```javascript
// Drag and drop
// Validação de arquivo
// AJAX POST para /api/verificar-identidade
// Exibição de resultados
// Tratamento de erros
```

---

## Fluxo de Dados

```
FRONTEND (index.html)
│
├─> User seleciona imagem (drag/drop ou input)
│
├─> Clica "Verificar Identidade"
│
├─> JavaScript: fetch('/api/verificar-identidade', FormData)
│
└─> Envia arquivo para:

BACKEND (detetive.py)
│
├─> Valida arquivo (tipo, tamanho)
│
├─> Salva temporariamente em uploads/
│
├─> Converte para Base64
│
├─> Envia para SerpApi
│   └─> Recebe visual_matches (links, títulos)
│
├─> Envia para Groq LLM
│   └─> Recebe análise formatada
│
├─> Deleta arquivo (LGPD)
│
└─> Retorna JSON com resultado

FRONTEND (index.html)
│
└─> JavaScript: Exibe resultado na página
```

---

## Endpoints da API

### POST /api/verificar-identidade

**Request:**
```
Content-Type: multipart/form-data
Body:
  - imagem: [arquivo]
```

**Response Sucesso (200):**
```json
{
  "sucesso": true,
  "analise": "⚠️ RISCO: ALTO\n🔍 ANÁLISE: ...",
  "resultados_encontrados": 8,
  "detalhes": [
    {
      "title": "Título",
      "link": "https://...",
      "source": "Instagram",
      "snippet": ""
    }
  ]
}
```

**Response Erro (400/500):**
```json
{
  "erro": "Mensagem de erro descritiva"
}
```

---

## Variáveis Importantes

### Configuração
```python
UPLOAD_FOLDER = 'uploads'              # Pasta de uploads
ALLOWED_EXTENSIONS = {...}              # Tipos permitidos
MAX_FILE_SIZE = 10 * 1024 * 1024       # Limite 10MB
GROQ_API_KEY = "..."                    # Chave Groq
SERPAPI_API_KEY = "..."                 # Chave SerpApi
```

### Models
```python
model="llama-3.3-70b-versatile"  # Modelo Groq usado
engine="google_lens"              # Motor SerpApi usado
```

---

## Funções Auxiliares

| Função | Propósito |
|--------|-----------|
| `allowed_file()` | Valida extensão de arquivo |
| `delete_file()` | Deleta arquivo (LGPD) |
| `image_to_base64()` | Converte imagem para Base64 |
| `search_image_with_serpapi()` | Busca reversa com Google Lens |
| `analyze_with_groq()` | Análise IA de identidade |

---

## Configurações Flask

```python
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
app.run(debug=True)  # debug=False em produção
```

---

## Prompt do Groq

O prompt enviado para Groq analisa:

1. **Coesão de Identidade**: Mesma pessoa em todos os links?
2. **Inconsistências**: Nomes diferentes? Contextos diferentes?
3. **Padrões Suspeitos**: Muitas contas recentes? Muitas variações?
4. **Resultado**: RISCO + ANÁLISE + BANDEIRAS + RECOMENDAÇÃO

---

## Erros Comuns e Tratamento

| Erro | Tratamento |
|------|-----------|
| Arquivo não enviado | 400 Bad Request + mensagem |
| Tipo não permitido | 400 Bad Request + sugestão |
| SerpApi falha | Retorna análise vazia com aviso |
| Groq falha | Retorna erro descritivo |
| Deleção falha | Log + continua (não interrompe) |

---

## Segurança Implementada

✅ `secure_filename()` - Previne path traversal
✅ Validação de tipo - Apenas imagens
✅ Limite de tamanho - Previne DoS
✅ Base64 encoding - Transmissão segura
✅ Deleção automática - Conformidade LGPD
✅ Try/except - Falhas controladas

---

## Performance

- **Upload**: < 1 segundo
- **SerpApi**: 10-30 segundos
- **Groq Análise**: 5-15 segundos
- **Deleção**: < 1 segundo
- **Total**: ~30-60 segundos

---

## Requisitos de Produção

Para colocar em produção:

1. `debug=False` no Flask
2. `HTTPS` habilitado
3. Usar Gunicorn/uWSGI
4. Variáveis em `.env`
5. Nginx como reverse proxy
6. Rate limiting
7. Logging de auditoria

---

## Checklist de Testes

- [ ] Upload funciona (arquivo salvo)
- [ ] Validação rejeita arquivo errado
- [ ] SerpApi retorna resultados
- [ ] Groq retorna análise
- [ ] Arquivo é deletado
- [ ] Frontend mostra resultado
- [ ] Erros são tratados
- [ ] Responde em tempo razoável

---

*Referência rápida para desenvolvimento e manutenção* 📚
