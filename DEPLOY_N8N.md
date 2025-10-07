# Deploy MCP Server para uso com n8n (Railway)

## Problema: n8n hosteado não acessa localhost

Se seu n8n está hosteado na Railway (ou outra plataforma cloud), ele **não consegue** acessar `http://localhost:8000` do seu computador local, pois estão em redes diferentes.

## Solução: Deploy do MCP Server na Railway

### Passo 1: Preparar o Repositório

O repositório já está configurado com `railway.toml` apontando para `Dockerfile.n8n` (com SSE transport).

### Passo 2: Deploy na Railway

1. **Acesse** [railway.app](https://railway.app)

2. **Crie novo projeto**:
   - Click em "New Project"
   - Selecione "Deploy from GitHub repo"
   - Escolha este repositório

3. **Configure (se necessário)**:
   - Railway detecta automaticamente o `railway.toml`
   - Variável `PORT` é setada automaticamente
   - Adicione variáveis opcionais se precisar (proxy, response limit, etc.)

4. **Aguarde o deploy**:
   - Railway vai buildar usando `Dockerfile.n8n`
   - Após deploy, você receberá uma URL pública

### Passo 3: Obter a URL

Após deploy completo, Railway fornecerá uma URL como:
```
https://seu-projeto-production.up.railway.app
```

**IMPORTANTE**: Para SSE, você usa a URL diretamente **sem** `/sse` no final.

### Passo 4: Configurar no n8n

No seu n8n hosteado na Railway:

1. **Adicione** o node "MCP Client Tool"

2. **Configure**:
   - **SSE Endpoint**: `https://seu-projeto-production.up.railway.app`
   - **Authentication**: `None`
   - **Tools**: `All`

3. **Teste** a conexão:
   - Se configurado corretamente, você verá as ferramentas:
     - `get_transcript`
     - `get_video_info`

## Opção Alternativa: Expor Localhost com ngrok

Se preferir não fazer deploy na Railway, pode expor seu servidor local:

### 1. Instalar ngrok
```bash
brew install ngrok
# ou baixe em: https://ngrok.com/download
```

### 2. Autenticar (crie conta grátis em ngrok.com)
```bash
ngrok authtoken SEU_TOKEN_AQUI
```

### 3. Expor a porta 8000
```bash
ngrok http 8000
```

### 4. Usar a URL do ngrok no n8n
```
SSE Endpoint: https://abc123.ngrok.io
```

**Desvantagens do ngrok**:
- ❌ URL muda toda vez que reinicia ngrok (plano grátis)
- ❌ Seu computador precisa estar ligado
- ❌ Pode ter limitações de bandwidth

## Verificação

Para testar se o servidor está acessível:

```bash
# Teste local
curl http://localhost:8000

# Teste na Railway (substitua pela sua URL)
curl https://seu-projeto-production.up.railway.app
```

## Troubleshooting

### "Connection refused" ou "Cannot connect"
- ✅ Verifique se o servidor está rodando na Railway
- ✅ Verifique os logs do deploy na Railway
- ✅ Confirme que usou `Dockerfile.n8n` (SSE transport)

### "No tools found"
- ✅ Verifique se a URL está correta (sem `/sse` no final)
- ✅ Teste a URL diretamente no browser
- ✅ Verifique se o servidor está usando porta correta (Railway seta automaticamente)

### n8n não aceita a URL
- ✅ Use HTTPS na Railway (não HTTP)
- ✅ Não adicione `/sse`, `/health` ou outros paths
- ✅ Use apenas a URL base fornecida pela Railway
