#!/bin/bash
# Script de instalação rápida para Linux/Mac
# Para Windows, execute os comandos pip manualmente

echo "🔍 Instalando Detetive de Identidade Digital..."
echo ""

# Atualizar pip
echo "📦 Atualizando pip..."
pip install --upgrade pip

# Instalar dependências
echo "📦 Instalando dependências..."
pip install -r requirements.txt

# Criar pasta uploads
echo "📁 Criando pasta de uploads..."
mkdir -p uploads

echo ""
echo "✅ Instalação concluída!"
echo ""
echo "🚀 Próximos passos:"
echo "1. Edite o arquivo detetive.py e substitua SERPAPI_API_KEY"
echo "2. Execute: python detetive.py"
echo "3. Acesse: http://localhost:5000"
echo ""
echo "📖 Para mais informações, veja:"
echo "   - README.md (visão geral)"
echo "   - SETUP.md (instalação detalhada)"
echo "   - SEGURANCA.md (boas práticas de segurança)"
