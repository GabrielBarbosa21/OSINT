# 🔍 Detetive de Identidade Digital

Uma ferramenta OSINT (Open Source Intelligence) para verificação de identidade e detecção de fraudes com conformidade LGPD.

## ✨ O que faz?

1. **Upload de Imagem**: Você envia uma foto
2. **Google Lens Reverso**: Busca a imagem na web usando SerpApi
3. **Análise IA**: Groq verifica se todos os links encontrados pertencem à mesma pessoa
4. **Resultado**: Recebe análise de risco (BAIXO/MÉDIO/ALTO/CRÍTICO) com recomendações
5. **Privacidade**: Foto deletada automaticamente (LGPD)

---

## 🚀 Início Rápido

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

Ou instale manualmente:

```bash
pip install flask groq google-search-results werkzeug requests python-dotenv
```

### 2. Configurar Chaves de API

Edite `detetive.py` e adicione suas chaves:

```python
GROQ_API_KEY = "sua_chave_groq"        # https://console.groq.com/
SERPAPI_API_KEY = "sua_chave_serpapi"  # https://serpapi.com/
```

### 3. Executar o Servidor

```bash
python detetive.py
```

Acesse: **http://localhost:5000**

---

## 📋 Recursos Implementados

### Backend (detetive.py)
- ✅ Upload seguro com validação
- ✅ Integração SerpApi para Google Lens reverso
- ✅ Análise com IA Groq (llama-3.3-70b-versatile)
- ✅ Detecção de fake/golpe
- ✅ Deleção automática (LGPD)
- ✅ Tratamento de erros robusto

### Frontend (index.html)
- ✅ Dark Mode moderno
- ✅ Drag-and-drop de imagens
- ✅ Interface responsiva
- ✅ Spinner de carregamento
- ✅ Exibição de resultados formatados
- ✅ Nota de privacidade LGPD

---

## 🔒 Segurança & LGPD

- 🔐 Nomes de arquivo seguros (`secure_filename`)
- 🔐 Validação de tipos (PNG, JPG, JPEG, GIF, WEBP, BMP)
- 🔐 Limite de tamanho: 10MB
- 🔐 Deletação imediata de arquivos
- 🔐 Sem armazenamento permanente
- 🔐 Conformidade com LGPD

---

## 📁 Estrutura do Projeto

```
detetive_ofertas/
├── detetive.py              # Backend Flask
├── templates/
│   └── index.html           # Frontend
├── uploads/                 # Imagens temporárias (auto-criado)
├── requirements.txt         # Dependências
├── .env.example            # Exemplo de configuração
├── SETUP.md                # Guia detalhado
└── README.md               # Este arquivo
```

---

## 🎯 Como Usar

1. **Abra a aplicação**: http://localhost:5000
2. **Selecione uma imagem** (ou arraste)
3. **Clique em "Verificar Identidade"**
4. **Aguarde a análise** (30-60 segundos)
5. **Veja o relatório** com nível de risco

---

## 📊 Exemplo de Resultado

```
⚠️ RISCO: MÉDIO
🔍 ANÁLISE: A imagem encontrada em 3 fontes diferentes com nomes consistentes.
            Padrão indica conta potencialmente legítima, mas com presença em múltiplas plataformas.

🚩 BANDEIRAS VERMELHAS: 
   - Conta criada há menos de 6 meses
   - Múltiplas variações de perfil com mesma foto

✅ RECOMENDAÇÃO: Verificar credibilidade através de contatos diretos e confirmar identidade
```

---

## 🔧 Configuração Avançada

### Usar com .env

1. Crie arquivo `.env` baseado em `.env.example`
2. Preencha suas chaves
3. Modifique `detetive.py`:

```python
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
```

### Aumentar Limite de Upload

Em `detetive.py`:
```python
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
```

---

## 🛠️ Troubleshooting

| Problema | Solução |
|----------|---------|
| Módulo não encontrado | `pip install --upgrade [módulo]` |
| Erro 401 SerpApi | Verificar chave de API e créditos |
| Pasta uploads não criada | Criar manualmente ou reiniciar |
| Porta 5000 já em uso | Mudar em `app.run(port=5001)` |

---

## 📚 Documentação

- [SETUP.md](SETUP.md) - Guia completo de instalação
- [.env.example](.env.example) - Template de variáveis de ambiente

---

## 🤝 Contribuições

Este projeto é para uso educacional e de autoproteção.

**Lembre-se**: Use responsavelmente e respeite a privacidade das pessoas.

---

## ⚖️ Conformidade Legal

- ✅ LGPD (Lei Geral de Proteção de Dados - Brasil)
- ✅ Sem armazenamento permanente de dados
- ✅ Deletação imediata de arquivos
- ✅ Transparência sobre coleta de dados

---

**Desenvolvido com ❤️ para segurança digital**
