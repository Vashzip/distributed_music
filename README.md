# Sistema Distribuído de Streaming de Música

Sistema distribuído inspirado em plataformas de streaming de música (Spotify, Deezer), implementado como projeto final da disciplina de Sistemas Distribuídos. O sistema demonstra comunicação interprocessos, invocação remota (RPC), comunicação indireta e assíncrona via RabbitMQ.

## 📋 Arquitetura do Sistema

O sistema é composto pelos seguintes componentes:

### 1. **Cliente** (`client.py`)
Envia requisições ao gateway, simulando interações de usuários com a plataforma (busca de músicas, criação de playlists, consulta de histórico).

### 2. **Gateway** (`gateway.py`)
Middleware que atua como ponto único de entrada do sistema. Recebe requisições do cliente e coordena a comunicação com os serviços distribuídos através de RPC.

### 3. **Serviços Distribuídos** (`services/`)
Cada serviço executa em processo separado e implementa funcionalidades específicas:

- **Catalog Service** (`catalog_service.py`): Gerencia o catálogo de músicas, permitindo busca e listagem.
- **Playlist Service** (`playlist_service.py`): Gerencia playlists de usuários, permitindo criação, adição de músicas e consulta.
- **User Service** (`user_service.py`): Gerencia usuários e histórico de reprodução, além de publicar eventos assíncronos.

### 4. **Módulo de Mensagens** (`messaging.py`)
Fornece abstrações para comunicação via RabbitMQ:
- Funções para publicação de mensagens assíncronas
- Cliente RPC para invocação remota síncrona

### 5. **Broker de Mensagens** (RabbitMQ)
Responsável pela comunicação indireta e assíncrona entre os componentes.

## 🏗️ Padrões de Comunicação

O sistema demonstra dois tipos de comunicação:

### Comunicação Síncrona (RPC)
- Cliente → Gateway → Serviços: Requisições que necessitam resposta imediata
- Usado para: busca de músicas, criação de playlists, consulta de histórico

### Comunicação Assíncrona (Pub/Sub)
- Eventos publicados sem esperar resposta imediata
- Usado para: registro de eventos de reprodução (filas de eventos)

## 🚀 Requisitos

- Python 3.10+
- RabbitMQ Server
- Ambiente virtual Python (venv recomendado)

## 📦 Instalação

### 1. Instalar RabbitMQ

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install rabbitmq-server
```

**Fedora:**
```bash
sudo dnf install rabbitmq-server
```

**macOS:**
```bash
brew install rabbitmq
```

**Após instalar, inicie o serviço:**
```bash
# Linux (systemd)
sudo systemctl start rabbitmq-server

# macOS
brew services start rabbitmq
```

### 2. Configurar Ambiente Virtual

```bash
# Navegar para o diretório do projeto
cd /home/vash/distributed_music

# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

## ▶️ Execução

O sistema precisa de **5 terminais separados** rodando simultaneamente. Cada componente deve estar em execução antes do próximo.

### ⚠️ Ordem de Inicialização

1. **RabbitMQ** (deve estar rodando)
2. **Catalog Service**
3. **Playlist Service**
4. **User Service**
5. **Gateway**
6. **Cliente** (executa as operações e encerra)

### Passo 1: Verificar RabbitMQ

**Verificar se está rodando:**
```bash
sudo systemctl status rabbitmq-server
# ou
rabbitmqctl status
```

**Se não estiver rodando, apenas INICIE o serviço:**
```bash
# Linux
sudo systemctl start rabbitmq-server

# macOS
brew services start rabbitmq
```

**Nota:** Se você ainda não instalou o RabbitMQ, volte à seção de [Instalação](#-instalação) acima.

### Passo 2: Iniciar os Serviços

Abra **4 terminais separados** e execute cada serviço na ordem especificada:

**Terminal 1 - Catalog Service:**
```bash
cd /home/vash/distributed_music
source venv/bin/activate
python services/catalog_service.py
```
**Saída esperada:** `🎵 Catalog Service (Top BR) rodando...`

**Terminal 2 - Playlist Service:**
```bash
cd /home/vash/distributed_music
source venv/bin/activate
python services/playlist_service.py
```
**Saída esperada:** `📂 Serviço de playlists ativo...`

**Terminal 3 - User Service:**
```bash
cd /home/vash/distributed_music
source venv/bin/activate
python services/user_service.py
```
**Saída esperada:** `👤 Serviço de usuários ativo...`

**Terminal 4 - Gateway:**
```bash
cd /home/vash/distributed_music
source venv/bin/activate
python gateway.py
```
**Saída esperada:** `🚪 Gateway aguardando requisições...`

### Passo 3: Executar o Cliente

**Terminal 5 - Cliente:**
```bash
cd /home/vash/distributed_music
source venv/bin/activate
python client.py
```

O cliente executará automaticamente todas as operações:
- Busca de músicas
- Listagem de catálogo
- Criação de playlists
- Adição de músicas às playlists
- Consulta de histórico
- Registro de reproduções

### 🛑 Encerrando o Sistema

Para encerrar o sistema, pressione `Ctrl+C` em cada terminal na ordem inversa:
1. Cliente (se ainda estiver rodando)
2. Gateway
3. User Service
4. Playlist Service
5. Catalog Service

### 🔍 Verificando se está funcionando

**Verificar filas no RabbitMQ:**
```bash
rabbitmqctl list_queues
```

Você deve ver as seguintes filas quando os serviços estiverem rodando:
- `gateway_rpc`
- `catalog_rpc`
- `playlist_rpc`
- `user_rpc`
- `play_history_events` (quando houver eventos)

## ⚠️ Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'pika'"

**Solução:** Certifique-se de que o ambiente virtual está ativado e instale as dependências:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Erro: "Connection refused" ou "Cannot connect to RabbitMQ"

**Solução:** Inicie o RabbitMQ:
```bash
sudo systemctl start rabbitmq-server
# ou
sudo systemctl restart rabbitmq-server
```

### Erro: "Queue not found" ou timeout

**Solução:** Certifique-se de que todos os serviços estão rodando na ordem correta:
1. Catalog Service
2. Playlist Service  
3. User Service
4. Gateway
5. Cliente

### Os serviços não respondem

**Solução:** Verifique se o RabbitMQ está rodando e se todas as conexões estão ativas:
```bash
rabbitmqctl list_connections
```

## 📝 Funcionalidades Implementadas

### Catalog Service
- `search_music`: Busca músicas por título, artista ou gênero
- `list_all`: Lista todas as músicas do catálogo
- `get_song_by_id`: Obtém detalhes de uma música específica

### Playlist Service
- `create_playlist`: Cria uma nova playlist para um usuário
- `add_song_to_playlist`: Adiciona uma música a uma playlist
- `get_playlist`: Obtém detalhes de uma playlist
- `list_user_playlists`: Lista todas as playlists de um usuário

### User Service
- `get_user_history`: Obtém histórico de reprodução de um usuário
- `get_user_info`: Obtém informações de um usuário
- `register_play`: Registra uma reprodução de música (também publica evento assíncrono)

## 🔄 Fluxo de Execução

```
Cliente → Gateway (RPC) → Serviço Específico → Gateway → Cliente
                         ↓
                    Evento Assíncrono (RabbitMQ)
```

### Exemplo: Busca de Música
1. Cliente envia requisição RPC ao Gateway
2. Gateway identifica ação `search_music` e encaminha ao Catalog Service
3. Catalog Service processa a busca e retorna resultados
4. Gateway retorna resposta ao Cliente
5. Cliente exibe resultados

### Exemplo: Registro de Reprodução
1. Cliente envia requisição RPC ao Gateway
2. Gateway encaminha ao User Service
3. User Service registra a reprodução
4. User Service publica evento assíncrono na fila `play_history_events`
5. Gateway retorna confirmação ao Cliente

## 📊 Estrutura de Mensagens

### Requisições RPC
```json
{
  "action": "search_music",
  "query": "Funk"
}
```

### Respostas
```json
{
  "result": [
    {
      "id": 1,
      "title": "Tá OK",
      "artist": "DENNIS & Kevin O Chris",
      "genre": "Funk"
    }
  ]
}
```

### Eventos Assíncronos
```json
{
  "user_id": 1,
  "song_title": "Tá OK",
  "type": "song_played"
}
```

## 🧪 Exemplos de Uso

### Buscar Música
```python
from messaging import RpcClient

rpc = RpcClient()
response = rpc.call('gateway_rpc', {
    'action': 'search_music',
    'query': 'Sertanejo'
})
print(response)
```

### Criar Playlist
```python
response = rpc.call('gateway_rpc', {
    'action': 'create_playlist',
    'playlist_name': 'Minhas Favoritas',
    'user_id': 1
})
playlist_id = response.get('playlist_id')
```

### Publicar Evento Assíncrono
```python
from messaging import publish

publish('play_history_events', {
    'user_id': 1,
    'song_title': 'Tá OK',
    'type': 'song_played'
})
```

## 📁 Estrutura do Projeto

```
distributed_music/
├── client.py                 # Cliente do sistema
├── gateway.py                # Gateway/Middleware
├── messaging.py              # Módulo de comunicação
├── requirements.txt          # Dependências Python
├── .gitignore               # Arquivos ignorados pelo Git
├── README.md                # Este arquivo
└── services/
    ├── catalog_service.py   # Serviço de catálogo
    ├── playlist_service.py  # Serviço de playlists
    └── user_service.py      # Serviço de usuários
```

## 🔍 Conceitos de Sistemas Distribuídos Demonstrados

1. **Comunicação Interprocessos**: Componentes comunicam-se via RabbitMQ
2. **Invocação Remota (RPC)**: Comunicação síncrona cliente-servidor
3. **Comunicação Indireta**: Via broker de mensagens (RabbitMQ)
4. **Comunicação Assíncrona**: Eventos publicados sem bloqueio
5. **Middleware (Gateway)**: Ponto único de entrada e coordenação
6. **Serviços Distribuídos**: Processos separados com responsabilidades específicas

## ⚠️ Notas Importantes

- **Ordem é importante**: Os serviços devem ser iniciados na ordem especificada
- **Mantenha todos os terminais abertos**: Cada serviço precisa estar rodando simultaneamente
- **Dados em memória**: Os dados são armazenados em memória e serão perdidos ao reiniciar os serviços
- **Timeout**: O sistema tem timeout padrão de 30 segundos para requisições RPC
- **Tratamento de erros**: Tratamento de erros básico está implementado

## 👥 Autores

Projeto desenvolvido para a disciplina de Sistemas Distribuídos - 2025-2

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais.
