const messagesContainer = document.getElementById('chatbot-messages');
const inputField = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const chatbotContainer = document.getElementById('chatbot-container');
const toggleBtn = document.getElementById('chatbot-toggle-btn');
const closeBtn = document.getElementById('chatbot-close-btn');

let chatHistory = []; // Para armazenar o histórico e enviar no RAG

// Fechar / Abrir o chatbot
toggleBtn.addEventListener('click', () => {
    chatbotContainer.classList.toggle('hidden');
    if (!chatbotContainer.classList.contains('hidden')) {
        inputField.focus();
    }
});

// Botao fechar da barra do topo
closeBtn.addEventListener('click', () => {
    chatbotContainer.classList.add('hidden');
});

function appendMessage(sender, text) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender);
    msgDiv.innerText = text;
    messagesContainer.appendChild(msgDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

async function sendMessage() {
    const text = inputField.value.trim();
    if (!text) return;

    // Coloca a mensagem do utilizador no UI
    appendMessage('user', text);
    inputField.value = '';

    // Preparar para enviar à API
    const loadingDiv = document.createElement('div');
    loadingDiv.classList.add('message', 'bot');
    loadingDiv.innerHTML = '<i class="fas fa-ellipsis-h fa-fade"></i>';
    messagesContainer.appendChild(loadingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    try {
        const response = await fetch('/api/chat', {
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
        
        // Remove a pensar
        messagesContainer.removeChild(loadingDiv);
        
        // Adiciona a resposta
        appendMessage('bot', data.reply);

        // Guardar o contexto para a próxima pergunta
        chatHistory.push({ role: 'user', content: text });
        chatHistory.push({ role: 'bot', content: data.reply });

    } catch (error) {
        messagesContainer.removeChild(loadingDiv);
        appendMessage('bot', 'Desculpe, ocorreu um erro de conexão.');
        console.error("Erro na API:", error);
    }
}

sendBtn.addEventListener('click', sendMessage);
inputField.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

