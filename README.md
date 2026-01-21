# 🎵 Music Streaming Distribuído com RabbitMQ

Este projeto implementa um **sistema de streaming de música distribuído**, desenvolvido em **Python**, utilizando **RabbitMQ** como middleware de mensageria e o padrão **RPC (Request/Response)** para comunicação entre serviços.

O objetivo é **demonstrar na prática conceitos de Sistemas Distribuídos**, como desacoplamento, comunicação indireta, escalabilidade e independência entre serviços.

---

## 📌 Visão Geral da Arquitetura

O sistema é composto por:

* **Cliente**: interface via terminal
* **RabbitMQ**: broker de mensagens
* **Serviços independentes**:

  * Catalog Service (músicas)
  * Playlist Service (playlists)
  * User Service (usuários)

📡 Toda comunicação ocorre **exclusivamente via RabbitMQ**, sem chamadas diretas entre cliente e serviços.

---

## 🧩 Tecnologias Utilizadas

* Python 3
* RabbitMQ
* Biblioteca Pika (AMQP)
* Git / GitHub

---

## 🗂 Estrutura do Projeto

```
music-streaming-distribuido/
│
├── client.py
├── gateway.py (opcional)
├── messaging/
│   └── __init__.py
│   └── connection.py
│
├── services/
│   ├── catalog_service.py
│   ├── playlist_service.py
│   └── user_service.py
│
├── venv/
├── requirements.txt
└── README.md
```

---

## 🔌 RabbitMQ no Projeto

* Atua como **intermediário** entre cliente e serviços
* Cada serviço possui sua **fila própria**
* Garante comunicação **indireta e desacoplada**

Filas utilizadas:

* `catalog_queue`
* `playlist_queue`
* `user_queue`

---

## 🔁 Padrão RPC (Request / Response)

O projeto utiliza RPC sobre RabbitMQ:

1. Cliente envia uma requisição para a fila do serviço
2. Serviço processa a mensagem
3. Serviço responde usando:

   * `reply_to`
   * `correlation_id`
4. Cliente recebe a resposta correspondente

Esse padrão permite chamadas síncronas simuladas sobre mensageria.

---

## 🎶 Catalog Service

Responsável pelo **catálogo de músicas**.

### Características:

* Banco de dados **mockado em memória**
* Baseado em músicas populares do **Top Brasil**

### Funcionalidades:

* Listar todas as músicas
* Buscar por título, artista ou gênero

---

## 📀 Playlist Service

Responsável pelo gerenciamento de playlists.

### Funcionalidades:

* Criar playlists
* Associar músicas por ID
* Listar playlists existentes

Dados armazenados em memória (mock).

---

## 👤 User Service

Responsável pelo gerenciamento de usuários.

### Funcionalidades:

* Criar usuários
* Listar usuários

Serviço independente, sem dependência direta de outros serviços.

---

## 🖥 Cliente

* Interface via **terminal**
* Menu único para acesso a todos os serviços
* Não se comunica diretamente com serviços
* Envia requisições apenas via RabbitMQ

### Exemplo de Menu:

```
1 - Listar músicas
2 - Buscar música
3 - Criar playlist
4 - Ver playlists
5 - Criar usuário
6 - Listar usuários
0 - Sair
```

---

## ▶️ Como Executar o Projeto

### 1️⃣ Ativar o ambiente virtual

```bash
venv\Scripts\activate
```

### 2️⃣ Iniciar o RabbitMQ

Certifique-se de que o RabbitMQ está instalado e em execução.

### 3️⃣ Executar os serviços (em terminais separados)

```bash
python services/catalog_service.py
python services/playlist_service.py
python services/user_service.py
```

### 4️⃣ Executar o cliente

```bash
python client.py
```

---

## ✅ Benefícios da Arquitetura

* Baixo acoplamento
* Fácil manutenção
* Escalabilidade
* Comunicação indireta
* Simulação realista de sistemas distribuídos

---

## 🚀 Possíveis Evoluções

* Persistência em banco de dados
* Autenticação e autorização
* Interface gráfica
* APIs REST integradas
* Deploy com Docker

---

## 📚 Conclusão

Este projeto demonstra, de forma prática, a aplicação de conceitos fundamentais de **Sistemas Distribuídos**, utilizando mensageria com RabbitMQ e serviços independentes, sendo ideal para fins acadêmicos e aprendizado prático.

---

📌 *Projeto desenvolvido para fins educacionais.*
