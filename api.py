# api.py
from flask import Flask, jsonify
from confluent_kafka import Producer, Consumer
import time
import uuid

# *** IMPORTANTE: Endereço interno do Kafka para o Docker ***
KAFKA_BROKER = "kafka:9092" 
TOPIC_NAME = "primeiro_topico"

app = Flask(__name__)

# Função de Produtor (simplificada)
def produce_message(message_number):
    conf = {'bootstrap.servers': KAFKA_BROKER}
    producer = Producer(conf)
    
    key = f"chave-{message_number}"
    value = f"Esta é a mensagem via API número {message_number}."
    
    def delivery_report(err, msg):
        if err is not None:
            print(f"Falha na entrega da mensagem: {err}")
    
    producer.produce(TOPIC_NAME, key=key.encode('utf-8'), value=value.encode('utf-8'), callback=delivery_report)
    producer.flush()
    return f"Mensagem {message_number} enviada"

@app.route('/produce', methods=['POST'])
def handle_produce():
    # Envia 5 mensagens de teste
    results = [produce_message(i) for i in range(1, 6)]
    return jsonify({"status": "Success", "messages_sent": results})

# Função de Consumidor (leitura e retorno)
@app.route('/consume', methods=['GET'])
def handle_consume():
    # Usa um ID de grupo único para ler mensagens novas
    consumer_id = str(uuid.uuid4())
    conf = {
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': f"api-consumer-{consumer_id}",
        'auto.offset.reset': 'latest' # Ler apenas o que for novo
    }
    consumer = Consumer(conf)
    consumer.subscribe([TOPIC_NAME])

    messages = []
    
    # Roda por 3 segundos para coletar mensagens recentes
    for _ in range(3): 
        msg = consumer.poll(1.0)
        if msg is not None and msg.error() is None:
            messages.append(msg.value().decode('utf-8'))
    
    consumer.close()
    return jsonify({"status": "Success", "messages_read": messages})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)