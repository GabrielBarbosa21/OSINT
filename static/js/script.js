// Elements
const formUpload = document.getElementById('formUpload');
const inputImagem = document.getElementById('imagem');
const fileLabel = document.getElementById('fileLabel');
const fileName = document.getElementById('fileName');
const btnVerificar = document.getElementById('btnVerificar');

const progressContainer = document.getElementById('progressContainer');
const progressFill = document.getElementById('progressFill');
const progressSteps = document.getElementById('progressSteps');
const logContainer = document.getElementById('logContainer');
const logContent = document.getElementById('logContent');

const resultado = document.getElementById('resultado');
const veredito = document.getElementById('veredito');
const veredutoIcon = document.getElementById('veredutoIcon');
const veredutoTitle = document.getElementById('veredutoTitle');
const veredutoContent = document.getElementById('veredutoContent');
const riscoBadge = document.getElementById('riscoBadge');
const imagesContainer = document.getElementById('imagesContainer');
const imagesGrid = document.getElementById('imagesGrid');

const erro = document.getElementById('erro');
const textoErro = document.getElementById('textoErro');

// Modal elements
const imageModal = document.getElementById('imageModal');
const modalClose = document.getElementById('modalClose');
const modalImage = document.getElementById('modalImage');
const modalTitle = document.getElementById('modalTitle');
const modalSource = document.getElementById('modalSource');
const modalLink = document.getElementById('modalLink');

// Filter elements
const filterBtns = document.querySelectorAll('.filter-btn');
const loadMoreContainer = document.getElementById('loadMoreContainer');
const loadMoreBtn = document.getElementById('loadMoreBtn');

// State
let currentStep = 0;
const totalSteps = 4;
let allImages = [];
let displayedImages = [];
let currentFilter = 'all';
let imagesPerPage = 10;

// Drag and drop
fileLabel.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileLabel.classList.add('drag-over');
});

fileLabel.addEventListener('dragleave', () => {
    fileLabel.classList.remove('drag-over');
});

fileLabel.addEventListener('drop', (e) => {
    e.preventDefault();
    fileLabel.classList.remove('drag-over');
    inputImagem.files = e.dataTransfer.files;
    atualizarNomeArquivo();
});

inputImagem.addEventListener('change', atualizarNomeArquivo);

function atualizarNomeArquivo() {
    if (inputImagem.files.length > 0) {
        fileName.textContent = `✓ ${inputImagem.files[0].name}`;
        fileName.classList.add('active');
    } else {
        fileName.textContent = '';
        fileName.classList.remove('active');
    }
}

// Progress functions
function updateProgress(step, percentage) {
    currentStep = step;
    progressFill.style.width = percentage + '%';

    const steps = progressSteps.querySelectorAll('.progress-step');
    steps.forEach((s, idx) => {
        s.classList.remove('active', 'done');
        if (idx + 1 < step) {
            s.classList.add('done');
        } else if (idx + 1 === step) {
            s.classList.add('active');
        }
    });
}

// Log functions
function formatTimestamp(value) {
    const date = value ? new Date(value) : new Date();
    if (isNaN(date.getTime())) {
        return new Date().toLocaleTimeString('pt-BR', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    }

    return date.toLocaleTimeString('pt-BR', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

function addLog(stage, message) {
    const entry = document.createElement('div');
    entry.className = `log-entry ${stage}`;
    entry.textContent = message || 'Mensagem não informada';
    logContent.appendChild(entry);
    logContent.scrollTop = logContent.scrollHeight;
}

function displayLogs(logs) {
    logContent.innerHTML = '';
    if (!Array.isArray(logs)) {
        addLog('erro', `[${formatTimestamp()}] Dados de log inválidos`);
        return;
    }

    logs.forEach((log) => {
        let stage = 'info';
        let message = '';
        let timestamp = '';

        if (typeof log === 'string') {
            message = log;
        } else if (log && typeof log === 'object') {
            stage = log.stage || log.type || 'info';
            message = log.message || log.msg || log.text || JSON.stringify(log);
            timestamp = formatTimestamp(log.timestamp || log.time || log.created_at);
        }

        if (!timestamp) {
            timestamp = formatTimestamp();
        }

        addLog(stage, `[${timestamp}] ${message}`);
    });
}

// Risk color function
function getRiscoBadgeClass(risco) {
    const nivel = risco.toLowerCase();
    if (nivel.includes('baixo')) return 'baixo';
    if (nivel.includes('médio')) return 'medio';
    if (nivel.includes('alto') && !nivel.includes('crítico')) return 'alto';
    if (nivel.includes('crítico')) return 'critico';
    return 'medio';
}

function getRiscoIcon(risco) {
    const nivel = risco.toLowerCase();
    if (nivel.includes('baixo')) return '✅';
    if (nivel.includes('crítico')) return '🚨';
    if (nivel.includes('alto')) return '⚠️';
    return '❓';
}

// Display results
function exibirResultados(data) {
    const riscoClass = getRiscoBadgeClass(data.risco || 'Desconhecido');
    const riscoIcon = getRiscoIcon(data.risco || 'Desconhecido');

    veredutoIcon.textContent = riscoIcon;
    veredutoTitle.textContent = 'Veredito Final';
    veredutoContent.textContent = data.analise || 'Nenhuma análise disponível.';
    riscoBadge.textContent = data.risco || 'Desconhecido';
    riscoBadge.className = `risco-badge ${riscoClass}`;

    if (data.detalhes && data.detalhes.length > 0) {
        allImages = data.detalhes;
        currentFilter = 'all';
        displayedImages = [];
        imagesContainer.style.display = 'block';
        renderImages();
    }

    resultado.classList.add('active');
}

// Submit form
formUpload.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!inputImagem.files.length) {
        mostrarErro('Selecione uma imagem antes de verificar.');
        return;
    }

    resultado.classList.remove('active');
    erro.classList.remove('active');

    progressContainer.classList.add('active');
    logContainer.classList.add('active');
    fileLabel.classList.add('scanning');
    btnVerificar.disabled = true;

    updateProgress(1, 25);
    addLog('upload', '📤 Iniciando upload da imagem...');

    const formData = new FormData();
    formData.append('imagem', inputImagem.files[0]);

    try {
        const response = await fetch('/api/verificar-identidade', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.logs) {
            displayLogs(data.logs);
            updateProgress(4, 100);
        }

        if (response.ok && data.sucesso) {
            exibirResultados(data);
            updateProgress(4, 100);
        } else {
            mostrarErro(data.erro || 'Erro ao processar imagem');
        }
    } catch (err) {
        mostrarErro('Erro de conexão: ' + err.message);
    } finally {
        fileLabel.classList.remove('scanning');
        btnVerificar.disabled = false;
    }
});

function mostrarErro(mensagem) {
    textoErro.textContent = mensagem;
    erro.classList.add('active');
    progressContainer.classList.remove('active');
    logContainer.classList.remove('active');
    fileLabel.classList.remove('scanning');
}

// Filter functions
function getImageDomain(source) {
    if (!source) return 'outros';
    const lowerSource = source.toLowerCase();
    if (lowerSource.includes('instagram')) return 'instagram';
    if (lowerSource.includes('linkedin')) return 'linkedin';
    return 'outros';
}

function filterImages(filter) {
    currentFilter = filter;
    displayedImages = [];
    renderImages();
}

function renderImages() {
    const filteredImages = currentFilter === 'all' 
        ? allImages 
        : allImages.filter(img => getImageDomain(img.source) === currentFilter);
    
    const imagesToShow = filteredImages.slice(0, displayedImages.length + imagesPerPage);
    displayedImages = imagesToShow;
    
    imagesGrid.innerHTML = '';
    
    imagesToShow.forEach((img, idx) => {
        const card = document.createElement('div');
        card.className = 'image-card';
        
        let thumbnailHTML = '';
        if (img.thumbnail) {
            thumbnailHTML = `<img src="${img.thumbnail}" alt="Thumbnail ${idx + 1}">`;
        } else {
            thumbnailHTML = '<div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: #2d3561; color: #666;">🖼️</div>';
        }

        card.innerHTML = `
            <div class="image-thumbnail">${thumbnailHTML}</div>
            <div class="image-info">
                <div class="image-title" title="${img.title}">${img.title ? img.title.substring(0, 20) : 'Sem título'}</div>
                <div class="image-source" title="${img.source}">📍 ${img.source || 'Sem fonte'}</div>
                <a href="${img.link || '#'}" target="_blank" class="image-link" title="${img.link || ''}">🔗 Ver</a>
            </div>
        `;
        
        // Add staggered animation
        card.style.animationDelay = `${idx * 0.1}s`;
        card.classList.add('stagger');
        
        // Add click event for modal
        card.addEventListener('click', () => openModal(img));
        
        imagesGrid.appendChild(card);
    });
    
    // Show/hide load more button
    const hasMore = displayedImages.length < filteredImages.length;
    loadMoreContainer.style.display = hasMore ? 'block' : 'none';
}

function loadMoreImages() {
    const filteredImages = currentFilter === 'all' 
        ? allImages 
        : allImages.filter(img => getImageDomain(img.source) === currentFilter);
    
    const remaining = filteredImages.length - displayedImages.length;
    const toLoad = Math.min(remaining, imagesPerPage);
    
    for (let i = 0; i < toLoad; i++) {
        displayedImages.push(filteredImages[displayedImages.length]);
    }
    
    renderImages();
}

// Modal functions
function openModal(img) {
    modalImage.src = img.thumbnail || '';
    modalTitle.textContent = img.title || 'Sem título';
    modalSource.textContent = `Fonte: ${img.source || 'Desconhecida'}`;
    modalLink.href = img.link || '#';
    imageModal.classList.add('active');
}

function closeModal() {
    imageModal.classList.remove('active');
}

// Event listeners
filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        filterImages(btn.dataset.filter);
    });
});

loadMoreBtn.addEventListener('click', loadMoreImages);

modalClose.addEventListener('click', closeModal);

imageModal.addEventListener('click', (e) => {
    if (e.target === imageModal) {
        closeModal();
    }
});

// Close modal on escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && imageModal.classList.contains('active')) {
        closeModal();
    }
});
