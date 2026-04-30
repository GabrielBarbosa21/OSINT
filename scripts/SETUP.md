# 🔍 Detetive de Identidade Digital - Guia de Instalação

## 📋 Requisitos Prévios

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Chaves de API: Groq e SerpApi

---

## 🚀 Instalação Passo a Passo

### 1. Instalar as Dependências

Execute os comandos abaixo NO terminal na pasta do projeto:

```bash
pip install flask groq google-search-results werkzeug requests python-dotenv
```

### Descrição das Bibliotecas:

- **Flask**: Framework web (já estava no seu projeto)
- **groq**: Cliente oficial da Groq para LLM (já estava no seu projeto)
- **google-search-results**: Integração com SerpApi para Google Lens
- **werkzeug**: Segurança em upload de arquivos (`secure_filename`)
- **requests**: (dependência automática do google-search-results)
- **python-dotenv**: Para gerenciar variáveis de ambiente (opcional, mas recomendado)

---

## 🔑 Configuração de APIs

### Obter Chave SerpApi

1. Acesse: **https://serpapi.com/**
2. Crie uma conta gratuita
3. Copie sua **API Key**
4. Abra o arquivo `detetive.py` e substitua:
   ```python
   SERPAPI_API_KEY = "SEU_SERPAPI_KEY_AQUI"  # Substitua aqui
   ```

### Verificar Chave Groq

A chave Groq já está configurada no código. Se precisar mudar:
1. Acesse: **https://console.groq.com/**
2. Copie sua **API Key**
3. Substitua no arquivo `detetive.py`:
   ```python
   GROQ_API_KEY = "sua_chave_aqui"
   ```

---

## 📁 Estrutura de Pastas

Após instalação, sua estrutura será:

```
detetive_ofertas/
├── detetive.py           # Backend Flask (renovado)
├── detetive2.py          # (arquivo antigo, pode deletar)
├── SETUP.md              # Este arquivo
├── templates/
│   └── index.html        # Frontend (renovado)
└── uploads/              # Pasta criada automaticamente
    └── (imagens temporárias aqui)
```

---

## ▶️ Executar o Servidor

1. Abra o terminal na pasta do projeto
2. Execute:
   ```bash
   python detetive.py
   ```

3. Você verá:
   ```
   * Running on http://127.0.0.1:5000
   ```

4. Abra o navegador em: **http://localhost:5000**

---

## 🛡️ Funcionalidades Implementadas

✅ **Upload Seguro**
- Validação de extensão (PNG, JPG, JPEG, GIF, WEBP, BMP)
- Nomes de arquivo seguros com `secure_filename`
- Limite de tamanho: 10MB
- Geração de timestamp para evitar conflitos

✅ **Google Lens Reversa**
- Busca visual com SerpApi
- Captura de títulos, links e fontes
- Extrai até 10 resultados

✅ **Análise IA com Groq**
- Modelo: `llama-3.3-70b-versatile`
- Verifica consistência de identidade
- Identifica padrões de fake/golpe
- Fornece recomendações de segurança

✅ **Conformidade LGPD**
- Arquivo deletado automaticamente após análise
- Nenhuma imagem armazenada permanentemente
- Timestamp em nome de arquivo (rastreabilidade)
- Mensagem clara no rodapé sobre privacidade

---

## 🧪 Testar a Aplicação

1. Upload uma imagem
2. Clique em "Verificar Identidade"
3. Aguarde a análise (30-60 segundos)
4. Veja o resultado com análise de risco

---

## ⚙️ Variáveis de Ambiente (Opcional)

Se preferir usar `.env`, crie o arquivo:

**.env**
```
GROQ_API_KEY=sua_chave_groq
SERPAPI_API_KEY=sua_chave_serpapi
FLASK_ENV=development
DEBUG=True
```

E modifique `detetive.py` para:
```python
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
```

---

## 🐛 Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'flask'"
```bash
pip install flask --upgrade
```

### Erro: "ModuleNotFoundError: No module named 'groq'"
```bash
pip install groq --upgrade
```

### Erro: "ModuleNotFoundError: No module named 'google_search_results'"
```bash
pip install google-search-results
```

### A pasta uploads não foi criada
- O código cria automaticamente. Se não criar, crie manualmente a pasta `uploads/` na raiz do projeto.

### Erro 401 da SerpApi
- Verifique se a chave de API foi inserida corretamente
- Confirme que tem créditos na conta SerpApi (plano gratuito tem limite)

---

## 📱 Acessibilidade

A aplicação é responsiva e funciona em:
- ✅ Desktop (Chrome, Firefox, Edge, Safari)
- ✅ Tablet
- ✅ Smartphone

---

## 🔒 Segurança

Implementações de segurança:
1. ✅ Validação de tipos de arquivo
2. ✅ `secure_filename` do Werkzeug
3. ✅ Limite de tamanho de upload (10MB)
4. ✅ Deleção automática de arquivos (LGPD)
5. ✅ Tratamento de exceções em todas as funções
6. ✅ CORS padrão do Flask (ative se necessário)

---

## 📞 Suporte

Se tiver problemas:
1. Verifique se Python está instalado: `python --version`
2. Verifique pip: `pip --version`
3. Reinstale dependências: `pip install --upgrade flask groq google-search-results`
4. Reinicie o servidor Flask

---

**Desenvolvido com ❤️ para verificação segura de identidades digitais.**
