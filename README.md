# 🏆 Copa do Mundo Tech - Alura Album

Este projeto é um **álbum virtual interativo de figurinhas** dedicado às grandes mentes e marcos da tecnologia (Pioneiros da Inteligência Artificial, Criadores da Linguagem Python, Arquitetos de Banco de Dados, Pioneiros dos Sistemas Operacionais e Celebridades Tech do Brasil).

O projeto conta com uma interface realista que simula a experiência física de folhear um álbum de figurinhas de papel, com efeitos visuais e sonoros integrados.

---

## 🚀 Objetivo do Projeto

O principal objetivo deste projeto é construir uma aplicação web interativa moderna e de alta fidelidade visual. A aplicação demonstra o uso de práticas recomendadas em desenvolvimento web, incluindo:
* Estruturação semântica em **HTML5**.
* Estilização avançada e controle de layouts fluidos com **CSS Vanilla**.
* Manipulação dinâmica do DOM, integração assíncrona com APIs e síntese sonora em tempo real com **JavaScript**.

---

## 📁 Estrutura de Arquivos e Funcionalidades

O projeto é estruturado em três arquivos fundamentais na pasta principal:

### 1. 📄 [index.html](i-arq-ia-alura-album-main/index.html)
* **Função**: Estruturação semântica do álbum e definição de todo o conteúdo estático.
* **O que faz**:
  * Define a capa do álbum, a contracapa e as páginas internas divididas por categorias de tecnologia.
  * Cria a marcação dos "slots" das figurinhas com numeração (ex: `#01`, `#02`) e biografias curtas.
  * Define os botões de navegação (anterior, próximo) e o controle de ativação de som.
  * Carrega a biblioteca externa `PageFlip` via CDN e os recursos de estilo e comportamento locais.

### 2. 🎨 [style.css](i-arq-ia-alura-album-main/style.css)
* **Função**: Estilização visual, layout responsivo e animações da interface.
* **O que faz**:
  * Define uma paleta de cores moderna usando variáveis CSS (com tons que variam de *blue universe* a *white snow*).
  * Renderiza o layout das páginas do álbum de forma centralizada e tridimensional.
  * Cria sombras gradientes realistas nas dobras de página (simulando a lombada física de um livro).
  * Implementa animações personalizadas, como o efeito de *glitch* nos títulos e controles de cursor (`grab` e `grabbing`) durante a interação de arrastar.

### 3. ⚡ [app.js](i-arq-ia-alura-album-main/app.js)
* **Função**: Comportamento interativo, consumo de API externa e efeitos sonoros gerados por síntese.
* **O que faz**:
  * **Integração com API**: Efetua chamadas assíncronas (`fetch`) para obter as figurinhas de um backend externo (rodando em `http://localhost:8000/figurinhas`). Se disponíveis, carrega e preenche dinamicamente as imagens nos slots do álbum.
  * **Configuração do PageFlip**: Inicializa o efeito de transição de páginas tridimensional da biblioteca `PageFlip`, configurando proporções de aspecto, suporte para toque em dispositivos móveis e limites de transição.
  * **Efeito Sonoro (Web Audio API)**: Cria um sintetizador virtual em tempo de execução que gera dinamicamente ruído branco filtrado e varredura de frequência para simular com precisão o som físico de folhas de papel virando.
  * **Controles de Navegação**: Escuta cliques nos botões de controle, teclas direcionais do teclado (setas para esquerda e direita) e gerencia o status do som (mutado/desmutado).

---

## 🛠️ Tecnologias e Recursos Utilizados

* **HTML5**: Marcação semântica e acessível.
* **CSS3 Vanilla**: Layouts baseados em Grid/Flexbox, animações de *glitch*, gradientes dinâmicos e controle de dobras de página.
* **JavaScript (ES6+)**: Consumo de API REST, controle assíncrono e eventos interativos.
* **Web Audio API**: Síntese sonora procedural do efeito de papel.
* **Biblioteca St.PageFlip**: Mecânica avançada para folheamento 3D.

link: https://projeto-album-de-figurinhas-alura-n.vercel.app/
