@echo off
REM Script de instalação para Windows
REM Execute este arquivo clicando duas vezes ou no terminal

echo.
echo ===== INSTALACAO: Detetive de Identidade Digital =====
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python não encontrado!
    echo Baixe e instale de: https://www.python.org/downloads/
    echo NÃO ESQUEÇA: Marque "Add Python to PATH" durante instalação
    pause
    exit /b 1
)

echo ✓ Python encontrado

REM Atualizar pip
echo.
echo [1/3] Atualizando pip...
python -m pip install --upgrade pip
if errorlevel 1 goto erro

REM Instalar dependências
echo.
echo [2/3] Instalando dependências...
pip install -r requirements.txt
if errorlevel 1 goto erro

REM Criar pasta uploads
echo.
echo [3/3] Criando pasta de uploads...
if not exist uploads (
    mkdir uploads
    echo ✓ Pasta uploads criada
) else (
    echo ✓ Pasta uploads já existe
)

echo.
echo ===== INSTALACAO CONCLUIDA COM SUCESSO! =====
echo.
echo PROXIMO PASSO:
echo 1. Abra o arquivo detetive.py em um editor de texto
echo 2. Encontre a linha: SERPAPI_API_KEY = "SEU_SERPAPI_KEY_AQUI"
echo 3. Substitua "SEU_SERPAPI_KEY_AQUI" pela sua chave do SerpApi
echo 4. Obtenha chave em: https://serpapi.com/
echo 5. Salve o arquivo
echo.
echo EXECUTAR O SERVIDOR:
echo 1. Abra terminal (cmd) nesta pasta
echo 2. Digite: python detetive.py
echo 3. Abra navegador em: http://localhost:5000
echo.
echo DOCUMENTACAO:
echo - README.md: Visão geral do projeto
echo - SETUP.md: Guia detalhado de instalação
echo - SEGURANCA.md: Boas práticas de segurança
echo.
pause
exit /b 0

:erro
echo.
echo ERRO na instalação!
echo Tente novamente manualmente:
echo   pip install flask groq google-search-results werkzeug requests python-dotenv
echo.
pause
exit /b 1
