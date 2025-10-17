# 🚀 POC Kafka KRaft (Node Único) com API Python (Flask)

Este projeto é uma Prova de Conceito (POC) que demonstra uma arquitetura básica de streaming de dados utilizando:
1.  **Apache Kafka (KRaft mode)** como broker de mensagens.
2.  **Kafka UI** para monitoramento e visualização de tópicos.
3.  **API Python (Flask)** para simular um Produtor e um Consumidor.

O ambiente completo é orquestrado via Docker Compose, facilitando o início rápido.

## ⚙️ Arquitetura da Stack

| Serviço | Imagem | Porta Exposta | Função |
| :--- | :--- | :--- | :--- |
| `kafka-broker` | `confluentinc/cp-kafka:7.6.0` | 9094 | Broker e Controller (KRaft, nó único) |
| `kafka-ui` | `provectuslabs/kafka-ui:latest` | 8080 | Interface de Monitoramento Web |
| `python-api-poc`| (Build) | 5000 | API para Produção/Consumo de Teste |

**Configuração Crítica (KRaft):**
* **Cluster ID:** `Y-t_TjR9Q3GFuYt28wDq8A`
* **Tópico de Teste:** `primeiro_topico`

## 🏁 Como Iniciar

### Pré-requisitos
* Docker e Docker Compose V2 (ou `docker-compose` legado) instalados.

### Passos de Inicialização

1.  **Clonar o Repositório:**
    ```bash
    git clone [https://www.dio.me/articles/enviando-seu-projeto-para-o-github](https://www.dio.me/articles/enviando-seu-projeto-para-o-github)
    cd [pasta do projeto]
    ```

2.  **Construir e Iniciar a Stack:**
    Use o `--build` para garantir que o contêiner Python use seu `api.py` mais recente.
    ```bash
    docker compose up -d --build
    ```

3.  **Verificar o Status:**
    Confirme se todos os contêineres estão rodando (Status `Up`):
    ```bash
    docker compose ps
    ```
    Para acompanhar os logs em tempo real (recomendado durante o teste):
    ```bash
    docker compose logs -f
    ```

## 🧪 Testando o Fluxo de Mensagens

Use o arquivo `poc_tests.http` (requer a extensão **Rest Client** do VS Code) para executar os testes em sequência:

### 1. Acessar as Interfaces
* **Kafka UI:** Abra [http://localhost:8080](http://localhost:8080)
* **API Python:** Acesse [http://localhost:5000](http://localhost:5000)

### 2. Fluxo Produtor/Consumidor

| Teste | Método | Endpoint | Objetivo |
| :--- | :--- | :--- | :--- |
| **PRODUCE** | `POST` | `/produce` | Envia 5 mensagens para `primeiro_topico`. |
| **CONSUME** | `GET` | `/consume` | Lê todas as mensagens (auto.offset.reset: earliest) do `primeiro_topico`. |

**Resultado Esperado:**
* Ambas as chamadas devem retornar `HTTP 200 OK`.
* O *endpoint* `/consume` deve retornar um array `messages_read` contendo 5 mensagens.
* O Kafka UI deve exibir 5 mensagens no `primeiro_topico`.

## 🛑 Limpeza (Remoção da Stack)

Para remover todos os contêineres, redes e o volume de dados do Kafka:

```bash
docker compose down -v
```