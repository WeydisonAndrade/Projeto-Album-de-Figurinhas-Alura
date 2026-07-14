// ===================================================
// CONFIGURAÇÃO DA API
// A constante API_BASE_URL armazena o endereço do backend local.
// Quando o frontend é servido pelo backend (ex: FastAPI), as URLs
// podem ser relativas ou apontar para o endereço localhost.
// ===================================================
const API_BASE_URL = "http://localhost:8000";

// ===================================================
// FUNÇÃO: preencherFigurinhas()
// Busca as figurinhas no backend, faz o mapeamento por ID,
// e injeta dinamicamente as imagens nos slots HTML vazios correspondentes.
// ===================================================
async function preencherFigurinhas() {
    try {
        // 1. Faz uma requisição assíncrona GET para buscar as figurinhas
        const response = await fetch(`${API_BASE_URL}/figurinhas`);

        if (!response.ok) {
            throw new Error(`Erro na API: ${response.status} ${response.statusText}`);
        }

        // 2. Converte a resposta recebida em um array JSON
        const figurinhas = await response.json();

        // 3. Cria um mapa (Map) de chave/valor (ID -> Dados da figurinha) para lookup O(1) rápido
        //    Formato do map: 1 -> { id: 1, nome: "Alan Turing", imagem_url: "/imgs/01-alan-turing.jpg" }
        const porId = new Map(figurinhas.map(f => [f.id, f]));

        // 4. Seleciona todos os slots de figurinha vazios do DOM (.sticker-slot)
        const slots = document.querySelectorAll(".sticker-slot");

        // 5. Itera sobre cada slot encontrado
        for (const slot of slots) {
            const slotNumeroEl = slot.querySelector(".slot-number");
            if (!slotNumeroEl) continue;

            // Extrai o número ID do texto (exemplo: "#01" -> limpa o "#" -> converte em inteiro -> 1)
            const id = parseInt(slotNumeroEl.textContent.replace("#", ""), 10);

            // Se o mapa de figurinhas não contém este ID, ignora e pula para o próximo
            if (!porId.has(id)) continue;

            // Recupera as informações da figurinha no mapa
            const figurinha = porId.get(id);

            // Cria um novo elemento de imagem para colar no slot
            const img = document.createElement("img");
            img.src = `${API_BASE_URL}${figurinha.imagem_url}`;
            img.alt = figurinha.nome;
            img.className = "sticker-img";

            // Se a imagem carregar com sucesso, adiciona classe que aplica o estilo "colado"
            img.onload = () => slot.classList.add("slot-preenchido");
            img.onerror = () => console.warn(`Imagem não encontrada: ${figurinha.nome}`);

            // Insere o elemento da imagem como o primeiro filho do slot
            slot.insertBefore(img, slot.firstChild);
        }

        console.log(`✅ ${figurinhas.length} figurinhas carregadas da API!`);

    } catch (erro) {
        console.warn("⚠️  Não foi possível conectar à API do backend:", erro.message);
        console.info("ℹ️  Inicie o servidor: cd backend/dia-3 && uvicorn main:app --reload");
    }
}

// ===================================================
// EVENTO: DOMContentLoaded
// Inicializa o álbum (PageFlip), configura o controle de arraste das páginas,
// sintetizador de som (Web Audio API) e interações do teclado.
// ===================================================
document.addEventListener("DOMContentLoaded", () => {
    // Referências a elementos DOM chave da página
    const bookElement = document.getElementById("book");
    const btnPrev = document.getElementById("btn-prev");
    const btnNext = document.getElementById("btn-next");
    const soundToggle = document.getElementById("sound-toggle");
    const iconOn = soundToggle.querySelector(".sound-icon-on");
    const iconOff = soundToggle.querySelector(".sound-icon-off");

    let isMuted = false;
    let pageFlip = null;

    // ---------------------------------------------------
    // 1. INICIALIZAÇÃO DA BIBLIOTECA ST.PAGEFLIP
    // ---------------------------------------------------
    try {
        pageFlip = new St.PageFlip(bookElement, {
            width: 550,              // Largura base de cada página
            height: 800,             // Altura base de cada página
            size: "stretch",         // Se ajusta dinamicamente ao container mantendo proporções
            minWidth: 315,
            maxWidth: 1000,
            minHeight: 420,
            maxHeight: 1350,
            drawShadow: true,        // Habilita renderização de sombras realistas
            maxShadowOpacity: 0.4,   // Intensidade da sombra de dobra
            showCover: true,         // Permite que a primeira página atue como capa (abertura simples)
            mobileScrollSupport: true,
            useMouseEvents: false,   // Desativa gestos padrão do StPageFlip para evitar disparos acidentais
            showPageCorners: false,  // Oculta cantos dobrados interativos no hover do mouse
            disableFlipByClick: true,// Desativa virar página apenas clicando nela
            flippingTime: 800        // Duração da animação de virada (800ms)
        });

        // Lê e carrega as páginas a partir da marcação HTML contendo classe '.page'
        pageFlip.loadFromHTML(document.querySelectorAll(".page"));

        // ---------------------------------------------------
        // CONTROLE DE ARRASTE PERSONALIZADO (Drag and Drop State)
        // Permite folhear as páginas arrastando o mouse ou deslizando o dedo (touch)
        // ---------------------------------------------------
        let activeDragPage = null; // Armazena a página atualmente sob o início do clique
        let isClicking = false;     // Identifica se o botão do mouse ou tela está pressionada
        let startX = 0;            // Posição horizontal inicial do clique/touch
        let startY = 0;            // Posição vertical inicial do clique/touch
        let dragStarted = false;   // Indica se o arraste superou a distância limite (threshold)

        // Escuta os eventos mouse/touch em cada página para iniciar intenção de folhear
        document.querySelectorAll(".page").forEach((page, index) => {
            page.addEventListener("mousedown", (e) => {
                // Impede arraste se clicar em links ou botões
                if (e.target.closest("button") || e.target.closest("a")) return;
                isClicking = true;
                startX = e.clientX;
                startY = e.clientY;
                dragStarted = false;
                activeDragPage = { page, index };
            });

            page.addEventListener("touchstart", (e) => {
                if (e.target.closest("button") || e.target.closest("a")) return;
                const touch = e.touches[0];
                isClicking = true;
                startX = touch.clientX;
                startY = touch.clientY;
                dragStarted = false;
                activeDragPage = { page, index };
            });
        });

        // Processa o movimento e inicia a física do PageFlip somente após ultrapassar o threshold (10px)
        const handleMove = (clientX, clientY, isTouch = false) => {
            if (!isClicking || !activeDragPage) return;
            
            const deltaX = clientX - startX;
            const deltaY = clientY - startY;
            const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
            
            const bookRect = bookElement.getBoundingClientRect();

            // Só ativa o flip se mover mais de 10px (previne disparar em cliques normais)
            if (distance > 10 && !dragStarted) {
                dragStarted = true;
                let cornerX, cornerY;
                
                // Determina canto vertical de arraste (topo vs base) relativo à viewport
                const centerY = bookRect.top + bookRect.height / 2;
                if (startY < centerY) {
                    cornerY = 0; // Agarra pelo canto superior
                } else {
                    cornerY = bookRect.height; // Agarra pelo canto inferior
                }

                // Determina canto horizontal (páginas pares são do lado direito, ímpares esquerdo)
                if (activeDragPage.index % 2 === 0) {
                    cornerX = bookRect.width; // Agarra do canto direito
                } else {
                    cornerX = 0; // Agarra do canto esquerdo
                }
                
                document.body.classList.add("dragging");
                pageFlip.startUserTouch({ x: cornerX, y: cornerY });
            }
            
            // Se o arraste foi iniciado, atualiza a dobra conforme a posição atual do ponteiro
            if (dragStarted) {
                const relX = clientX - bookRect.left;
                const relY = clientY - bookRect.top;
                pageFlip.userMove({ x: relX, y: relY }, isTouch);
            }
        };

        // Finaliza o arraste soltando a página, completando ou cancelando a virada de página
        const handleRelease = (clientX, clientY, isTouch = false) => {
            if (dragStarted) {
                const bookRect = bookElement.getBoundingClientRect();
                const relX = clientX - bookRect.left;
                const relY = clientY - bookRect.top;
                pageFlip.userStop({ x: relX, y: relY }, isTouch);
            }
            isClicking = false;
            dragStarted = false;
            activeDragPage = null;
            document.body.classList.remove("dragging");
        };

        // Eventos globais na janela para captura e liberação do arraste
        window.addEventListener("mousemove", (e) => {
            handleMove(e.clientX, e.clientY, false);
        });

        window.addEventListener("touchmove", (e) => {
            if (e.touches.length > 0) {
                const touch = e.touches[0];
                handleMove(touch.clientX, touch.clientY, true);
            }
        });

        window.addEventListener("mouseup", (e) => {
            handleRelease(e.clientX, e.clientY, false);
        });

        window.addEventListener("touchend", (e) => {
            const touch = e.changedTouches[0] || e.touches[0];
            if (touch) {
                handleRelease(touch.clientX, touch.clientY, true);
            } else {
                handleRelease(startX, startY, true);
            }
        });

        // Mostra o livro (oculto por padrão no carregamento CSS) após a inicialização perfeita
        bookElement.style.display = "block";

        // Chama a função assíncrona para buscar e preencher as figurinhas via API (não bloqueia a UI)
        preencherFigurinhas();

    } catch (error) {
        console.error("Erro ao inicializar a biblioteca PageFlip:", error);
    }

    // ---------------------------------------------------
    // 2. GERADOR E SINTETIZADOR DE EFEITO SONORO (Web Audio API)
    //    Gera som de folheamento de papel de forma sintética (ruído procedural)
    // ---------------------------------------------------
    function playPaperTurnSound() {
        if (isMuted) return;

        try {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (!AudioContext) return;

            const audioCtx = new AudioContext();
            const duration = 0.45; // Duração em segundos do som
            const sampleRate = audioCtx.sampleRate;
            const bufferSize = sampleRate * duration;
            const buffer = audioCtx.createBuffer(1, bufferSize, sampleRate);
            const data = buffer.getChannelData(0);

            // 2a. Síntese de Ruído Branco com Envelope de Volume Personalizado
            for (let i = 0; i < bufferSize; i++) {
                const progress = i / bufferSize;
                
                // Gera amostra de ruído aleatório entre -1 e 1
                const noise = Math.random() * 2 - 1;

                // Envelope de volume: rampa de subida rápida (primeiros 30%) e decaimento suave (70% restantes)
                let envelope = 0;
                if (progress < 0.3) {
                    envelope = progress / 0.3; // Rampa de ataque rápido
                } else {
                    envelope = (1 - progress) / 0.7; // Decaimento linear suave
                }

                // Simula estalidos pequenos (fricção física) inserindo picos de forma aleatória e rara
                const paperCrackle = Math.random() > 0.985 ? (Math.random() * 2 - 1) * 0.35 : 0;

                // Aplica a mesclagem e atenua o ganho global
                data[i] = (noise * 0.65 + paperCrackle) * envelope * 0.12;
            }

            // Cria o nó de origem do buffer contendo nosso som de ruído
            const noiseNode = audioCtx.createBufferSource();
            noiseNode.buffer = buffer;

            // 2b. Filtro Passa-Banda (Bandpass)
            // Isola uma faixa de frequências específica para simular o som do papel de forma natural
            const bandpassFilter = audioCtx.createBiquadFilter();
            bandpassFilter.type = "bandpass";
            bandpassFilter.Q.value = 2.0;

            // Varredura de Frequência Exponencial (Sweep):
            // Começa em 1500Hz e decai até 350Hz (efeito acústico de folha se afastando)
            bandpassFilter.frequency.setValueAtTime(1500, audioCtx.currentTime);
            bandpassFilter.frequency.exponentialRampToValueAtTime(350, audioCtx.currentTime + duration);

            // 2c. Filtro Passa-Baixo (Lowpass)
            // Corta agudos ásperos ou digitais indesejados acima de 3.8KHz
            const lowpassFilter = audioCtx.createBiquadFilter();
            lowpassFilter.type = "lowpass";
            lowpassFilter.frequency.setValueAtTime(3800, audioCtx.currentTime);

            // 2d. Conecta o grafo de processamento e toca o áudio:
            // Nó Fonte (Ruído) -> Filtro Passa-Banda -> Filtro Passa-Baixo -> Saída Final (Caixas de som)
            noiseNode.connect(bandpassFilter);
            bandpassFilter.connect(lowpassFilter);
            lowpassFilter.connect(audioCtx.destination);

            noiseNode.start();
        } catch (e) {
            console.warn("Falha ao tocar som de virada de página:", e);
        }
    }

    // ---------------------------------------------------
    // 3. CONTROLE DOS ESTADOS DE MUTE E VOLUME
    // ---------------------------------------------------
    soundToggle.addEventListener("click", () => {
        isMuted = !isMuted;
        if (isMuted) {
            iconOn.classList.add("hidden");
            iconOff.classList.remove("hidden");
        } else {
            iconOn.classList.remove("hidden");
            iconOff.classList.add("hidden");
        }
    });

    // ---------------------------------------------------
    // 4. CONTROLES E EVENTOS DE NAVEGAÇÃO DE PÁGINA
    // ---------------------------------------------------
    if (pageFlip) {
        // Dispara o som de papel sintetizado quando o estado do livro mudar para "flipping" (virando)
        pageFlip.on("changeState", (e) => {
            if (e.data === "flipping") {
                playPaperTurnSound();
            }
        });

        // Monitora as viradas de páginas para ocultar ou exibir botões laterais
        pageFlip.on("flip", (e) => {
            const currentPage = e.data;
            const totalPages = pageFlip.getPageCount();

            // Oculta botão esquerdo se estiver na capa (Pág 0)
            if (currentPage === 0) {
                btnPrev.classList.add("hidden");
            } else {
                btnPrev.classList.remove("hidden");
            }

            // Oculta botão direito se estiver na última página (Contracapa)
            if (currentPage === totalPages - 1) {
                btnNext.classList.add("hidden");
            } else {
                btnNext.classList.remove("hidden");
            }
        });

        // Eventos de clique nas setas flutuantes
        btnPrev.addEventListener("click", () => {
            pageFlip.flipPrev();
        });

        btnNext.addEventListener("click", () => {
            pageFlip.flipNext();
        });

        // Eventos de digitação no teclado (Setas Direcionais) para virar páginas
        document.addEventListener("keydown", (e) => {
            if (e.key === "ArrowLeft") {
                pageFlip.flipPrev();
            } else if (e.key === "ArrowRight") {
                pageFlip.flipNext();
            }
        });

        // Inicializa com botão esquerdo oculto pois começamos na Capa (Pág 0)
        btnPrev.classList.add("hidden");
    }
});
