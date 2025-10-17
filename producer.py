import time
from confluent_kafka import Producer

# Configuração do Broker Kafka (nosso container)
# Usamos 'localhost:9094' conforme configurado no docker-compose.yml
KAFKA_BROKER = "localhost:9094"
TOPIC_NAME = "primeiro_topico"

def delivery_report(err, msg):
    """Função de callback chamada após cada mensagem ser enviada."""
    if err is not None:
        print(f"Falha na entrega da mensagem: {err}")
    else:
        # Imprime o tópico, partição e offset onde a mensagem foi gravada
        print(f"Mensagem enviada com sucesso para o Tópico: '{msg.topic()}' [Partição: {msg.partition()}] @ Offset: {msg.offset()}")

def run_producer():
    """Inicia e executa o produtor Kafka."""
    # Configura o produtor
    conf = {
        'bootstrap.servers': KAFKA_BROKER,
        'client.id': 'python-producer'
    }
    producer = Producer(conf)

    print(f"Produtor iniciado. Enviando mensagens para o tópico: {TOPIC_NAME}")
    
    # Cria algumas mensagens
    for i in range(1, 11):
        key = f"chave-{i}"
        value = f"Esta é a mensagem número {i}."
        
        try:
            # Envio assíncrono: a mensagem é colocada em uma fila interna
            producer.produce(TOPIC_NAME, key=key, value=value.encode('utf-8'), callback=delivery_report)
            
            # Força o envio de mensagens periodicamente para não sobrecarregar a memória
            producer.poll(0)
            
        except Exception as e:
            print(f"Erro ao produzir mensagem: {e}")
        
        time.sleep(0.5)

    # Espera até que todas as mensagens pendentes na fila sejam enviadas
    producer.flush()
    print("Produção de mensagens concluída.")


if __name__ == '__main__':
    run_producer()