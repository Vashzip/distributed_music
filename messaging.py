import pika
import json
import uuid

RABBITMQ_HOST = 'localhost'


def get_connection():
    return pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )


def publish(queue, message):
    connection = get_connection()
    channel = connection.channel()

    channel.queue_declare(queue=queue)
    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=json.dumps(message)
    )

    connection.close()


class RpcClient:
    def __init__(self):
        self.connection = get_connection()
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            try:
                self.response = json.loads(body)
            except json.JSONDecodeError:
                self.response = {'error': 'Resposta inválida do servidor'}

    def call(self, queue, message, timeout=30):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=queue,
                properties=pika.BasicProperties(
                    reply_to=self.callback_queue,
                    correlation_id=self.corr_id
                ),
                body=json.dumps(message)
            )

            import time
            start_time = time.time()
            while self.response is None:
                self.connection.process_data_events(time_limit=1)
                if time.time() - start_time > timeout:
                    return {'error': 'Timeout na requisição'}

            return self.response
        except Exception as e:
            return {'error': f'Erro na comunicação RPC: {str(e)}'}

    def close(self):
        try:
            if self.connection and not self.connection.is_closed:
                self.connection.close()
        except Exception:
            pass
