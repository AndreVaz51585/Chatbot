# Chatbot for EvoLab

API FastAPI do chatbot/RAG do EvoLab, preparada para correr localmente ou em Docker.

## Arrancar com Docker Compose

1. Copiar o ficheiro de ambiente:

   ```bash
   cp .env.example .env
   ```

2. Em deploy, editar `.env` e trocar `CORS_ALLOW_ORIGINS` pelo URL do frontend.

   Exemplo:

   ```env
   CORS_ALLOW_ORIGINS=http://34.123.45.67,https://evolab.example.com
   ```

3. Construir e arrancar os containers:

   ```bash
   docker compose up --build
   ```

O Compose arranca:

- `chatbot`: API FastAPI disponível em `http://localhost:8000`.

O modelo responsável por responder é o Gemini, configurado por `GEMINI_MODEL`. Para usar `gemini-2.0-flash-lite`, é obrigatório definir `GOOGLE_API_KEY` no ficheiro `.env`.

Na VM, se a porta `8000` estiver aberta na firewall, o widget pode ser carregado pelo frontend com:

```html
<script src="http://IP_DA_VM:8000/static/embed.js"></script>
```

O `embed.js` calcula automaticamente o URL base da API a partir do próprio `script src`. Se for preciso forçar outro endereço, definir antes:

```html
<script>
  window.EVOLAB_CHATBOT_API_URL = "http://IP_DA_VM:8000";
</script>
<script src="http://IP_DA_VM:8000/static/embed.js"></script>
```

## Variáveis principais

- `CHATBOT_PORT`: porta exposta pela API, por defeito `8000`.
- `GOOGLE_API_KEY`: chave da Gemini API.
- `GEMINI_MODEL`: modelo Gemini usado pelo RAG, por defeito `gemini-2.0-flash-lite`.
- `GEMINI_TEMPERATURE`: temperatura das respostas, por defeito `0.2`.
- `CORS_ALLOW_ORIGINS`: lista separada por vírgulas com os origins autorizados a chamar a API.
- `EMBEDDING_MODEL_NAME`: modelo de embeddings usado no RAG, por defeito `models/gemini-embedding-001`.
- `CHROMA_COLLECTION_NAME`: coleção Chroma onde ficam guardados os vetores desse modelo.
