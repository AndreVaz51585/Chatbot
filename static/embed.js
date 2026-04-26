
// IEFE - Immediately Invoked Function Expression
// garante que o script é completamente isolado e que não interfere com outras variáveis ou bibliotecas do site onde é embutido.

(function() {

    // URL base da API (onde o FastAPI está a correr).
    // temos de alterar quando for para produção, ou seja, quando o widget for embutido em sites externos, e onde o localhost não será acessível. Para isso, podemos usar uma variável de ambiente ou configuração que aponte para o URL correto da API.
    const BASE_URL = "http://localhost:8000";

    // Injetar o CSS do widget
    const style = document.createElement('link');
    style.rel = 'stylesheet';
    style.href = `${BASE_URL}/static/style.css`;
    document.head.appendChild(style);
    
    // Injetar FontAwesome para os ícones
    const fontAws = document.createElement('link');
    fontAws.rel = 'stylesheet';
    fontAws.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css';
    document.head.appendChild(fontAws);

    // Criar a estrutura HTML do Widget e injetar no <body>
    const widgetContainer = document.createElement('div');
    widgetContainer.id = 'EvoLab-widget';
    widgetContainer.innerHTML = `
        <button id="chatbot-toggle-btn">
            <i class="fas fa-comment-dots"></i>
        </button>

        <div id="chatbot-container" class="hidden">
            <div id="chatbot-header">
                <div class="header-info">
                    <i class="fas fa-robot"></i>
                    <h3>Assistente EvoLab</h3>
                </div>
                <button id="chatbot-close-btn"><i class="fas fa-times"></i></button>
            </div>
            <div id="chatbot-messages">
                <div class="message bot">Olá! Sou o assistente virtual do EvoLab, como posso ajuda-lo hoje?</div>
            </div>
            <div id="chatbot-input-area">
                <input type="text" id="chat-input" placeholder="Escreva a sua dúvida..." autocomplete="off">
                <button id="send-btn"><i class="fas fa-paper-plane"></i></button>
            </div>
        </div>
    `;
    document.body.appendChild(widgetContainer);

    // Adicionar a lógica de interação (Event Listeners)
    const messagesContainer = document.getElementById('chatbot-messages');
    const inputField = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const chatbotContainerElement = document.getElementById('chatbot-container');
    const toggleBtn = document.getElementById('chatbot-toggle-btn');
    const closeBtn = document.getElementById('chatbot-close-btn');


    // histórico local do chat, que enviamos diretamente à nossa API
    let chatHistory = [];

    toggleBtn.addEventListener('click', () => {
        chatbotContainerElement.classList.toggle('hidden');
        if (!chatbotContainerElement.classList.contains('hidden')) {
            inputField.focus();
        }
    });

    closeBtn.addEventListener('click', () => {
        chatbotContainerElement.classList.add('hidden');
    });

    function appendMessage(sender, text) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', sender);
        msgDiv.innerText = text;
        messagesContainer.appendChild(msgDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // Função para enviar mensagem à API
    async function sendMessage() {
        const text = inputField.value.trim();
        if (!text) return;

        appendMessage('user', text);
        inputField.value = '';

        const loadingDiv = document.createElement('div');
        loadingDiv.classList.add('message', 'bot');
        loadingDiv.innerHTML = '<i class="fas fa-ellipsis-h fa-fade"></i>';
        messagesContainer.appendChild(loadingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        try {
            const response = await fetch(`${BASE_URL}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    question: text,
                    history: chatHistory
                })
            });

            const data = await response.json();
            
            messagesContainer.removeChild(loadingDiv);
            appendMessage('bot', data.reply);

            chatHistory.push({ role: 'user', content: text });
            chatHistory.push({ role: 'bot', content: data.reply });

        } catch (error) {
            messagesContainer.removeChild(loadingDiv);
            appendMessage('bot', 'Desculpe, ocorreu um erro de conexão.');
            console.error("Erro na API Chatbot:", error);
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

})();
