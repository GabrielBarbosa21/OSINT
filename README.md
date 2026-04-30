# Detetive de Identidade Digital v1.0

## Visão Geral

O **Detetive de Identidade Digital** é uma ferramenta avançada de OSINT (Open Source Intelligence) desenvolvida para auxiliar na verificação de identidades digitais e no combate a fraudes online. Utilizando técnicas de inteligência de fontes abertas, o sistema analisa imagens de perfil para identificar possíveis usos fraudulentos em plataformas sociais, contribuindo para a proteção de usuários e organizações contra ameaças digitais.

A versão 1.0 oferece uma interface web intuitiva que permite o upload de imagens, processamento automatizado via APIs especializadas e apresentação de resultados com evidências visuais, mantendo total conformidade com regulamentações de privacidade.

## Arquitetura do Sistema

O sistema foi projetado com uma arquitetura modular e escalável, seguindo princípios de engenharia de software moderna:

```
Frontend (HTML/CSS/JS) → Backend Flask → Servidor Temporário → APIs Externas → Resposta Processada
```

### Componentes Principais:

- **Frontend**: Interface responsiva desenvolvida com HTML5, CSS3 moderno e JavaScript vanilla, proporcionando experiência de usuário fluida com animações e interações dinâmicas.

- **Backend Flask**: Servidor web Python utilizando o framework Flask para gerenciar requisições HTTP, processamento de formulários e coordenação de APIs externas.

- **Servidor Temporário**: Sistema de armazenamento temporário para processamento de imagens, com limpeza automática após análise.

- **APIs Externas**: Integração com serviços de busca visual (SerpApi) e processamento de linguagem natural (Groq) para análise inteligente de resultados.

- **Processamento de Resposta**: Análise estruturada dos dados retornados, categorização por domínio e apresentação organizada.

## Segurança e Privacidade

A segurança e privacidade dos dados são prioridades fundamentais do sistema:

- **Conformidade LGPD**: O projeto foi desenvolvido seguindo rigorosamente as normas da Lei Geral de Proteção de Dados (LGPD), garantindo transparência no tratamento de informações pessoais.

- **Limpeza Automática**: Todos os arquivos temporários são automaticamente removidos do servidor imediatamente após o processamento, não mantendo cópias ou backups.

- **Sem Armazenamento Persistente**: O sistema não armazena dados sensíveis, imagens ou metadados em bancos de dados ou sistemas de arquivo permanentes.

- **Processamento Temporário**: As imagens são processadas apenas durante a sessão de análise e descartadas automaticamente.

- **Transparência**: O usuário é informado sobre todas as operações realizadas e tem controle total sobre os dados enviados.

## Tecnologias Utilizadas

- **Backend**: Python 3.x com Flask framework
- **Frontend**: HTML5, CSS3 (design moderno com gradientes e animações), JavaScript vanilla
- **APIs Externas**:
  - SerpApi (Google Lens API) para busca visual reversa
  - Groq API para processamento de linguagem natural e análise inteligente
- **Infraestrutura**: Servidor web com suporte a uploads temporários e limpeza automática

## Guia de Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Ambiente virtual (recomendado)
- Conexão com internet para acesso às APIs

### Passo a Passo

1. **Clone o repositório**:
   ```bash
   git clone <url-do-repositorio>
   cd detetive-identidade-digital
   ```

2. **Crie um ambiente virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**:
   - Copie o arquivo `.env.example` para `.env`
   - Edite o arquivo `.env` com suas chaves de API:
     ```
     SERPAPI_KEY=sua-chave-serpapi-aqui
     GROQ_API_KEY=sua-chave-groq-aqui
     ```
   - **Importante**: Nunca commite o arquivo `.env` real no repositório

5. **Execute o servidor**:
   ```bash
   python detetive.py
   ```

6. **Acesse a aplicação**:
   - Abra o navegador em `http://localhost:5000`
   - Faça upload de uma imagem para iniciar a análise

### Verificação da Instalação

Após iniciar o servidor, você deve ver:
- Interface web responsiva carregando corretamente
- Capacidade de fazer upload de imagens
- Processamento automático com barra de progresso
- Resultados organizados em grade com filtros

## Funcionalidades v1.0

- ✅ Upload seguro de imagens
- ✅ Busca visual reversa automatizada
- ✅ Análise inteligente com IA
- ✅ Interface responsiva com animações
- ✅ Filtros por domínio (Instagram, LinkedIn, Outros)
- ✅ Modal de visualização ampliada
- ✅ Sistema de paginação expansível
- ✅ Logs detalhados do processamento
- ✅ Conformidade LGPD com limpeza automática

## O que Esperar da v1.1 (Roadmap)

A próxima versão trará melhorias significativas na profundidade da análise:

- **Busca Aprofundada**: Implementação de algoritmos de busca recursiva para descobrir conexões indiretas e perfis relacionados.

- **Relatórios em PDF**: Geração automática de relatórios estruturados em formato PDF, incluindo:
  - Análise detalhada dos resultados
  - Timeline de descobertas
  - Recomendações de ação
  - Metadados técnicos preservados

- **Dashboard Analítico**: Interface aprimorada com métricas de confiança e visualizações de rede de conexões.

- **Integração com Múltiplas Fontes**: Expansão para outras plataformas além do Google Lens.

- **API REST**: Exposição de endpoints para integração com outros sistemas.

## Contribuição

Este projeto foi desenvolvido como uma demonstração de engenharia de software aplicada à cibersegurança. Para sugestões ou colaborações, entre em contato através dos canais apropriados.

## Licença

Este projeto é distribuído sob licença proprietária. Consulte os termos de uso para mais informações.

---

**Desenvolvido com foco em engenharia de software e responsabilidade ética no tratamento de dados.**