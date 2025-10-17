from confluent_kafka import Consumer, KafkaException, KafkaError
import sys

# Configuração do Broker Kafka (nosso container)
KAFKA_BROKER = "localhost:9094"
TOPIC_NAME = "primeiro_topico"
# Grupo de consumidores (identifica quem está lendo)
CONSUMER_GROUP_ID = "python-consumer-group-poc"

def run_consumer():
    """Inicia e executa o consumidor Kafka."""
    
    # Configura o consumidor
    conf = {
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': CONSUMER_GROUP_ID,
        # Define a posição inicial de leitura:
        # 'earliest' lê desde o início (vai ler as 10 mensagens enviadas)
        # 'latest' leria apenas mensagens novas
        'auto.offset.reset': 'earliest' 
    }

    consumer = Consumer(conf)
    
    try:
        # Se inscreve no tópico
        consumer.subscribe([TOPIC_NAME])

        print(f"Consumidor iniciado. Lendo do tópico: {TOPIC_NAME} (Group ID: {CONSUMER_GROUP_ID})")
        
        while True:
            # Pega 1 mensagem, esperando no máximo 1 segundo
            msg = consumer.poll(timeout=1.0)
            
            if msg is None:
                continue
            
            if msg.error():
                # Erros de conexão ou internos
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # Fim de partição, não é um erro fatal
                    sys.stderr.write(f'%% {msg.topic()} [{msg.partition()}] atingiu o fim da partição no offset {msg.offset()}\n')
                elif msg.error():
                    # Erro fatal
                    raise KafkaException(msg.error())
            else:
                # Mensagem OK!
                # Decodifica o valor e a chave
                key = msg.key().decode('utf-8') if msg.key() else None
                value = msg.value().decode('utf-8')
                
                print(f"Lido: Chave='{key}', Valor='{value}' | Offset: {msg.offset()}")

    except Exception as e:
        print(f"Erro no consumidor: {e}")
        
    finally:
        # Fecha e commita o último offset lido
        print("\nFechando consumidor...")
        consumer.close()

if __name__ == '__main__':
    run_consumer()