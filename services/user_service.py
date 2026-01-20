import sys
import os
import json
import pika

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

from messaging import get_connection



def on_request(ch, method, props, body):
    response = {
        'user': 'João',
        'history': ['Bohemian Rhapsody', 'Highway to Hell']
    }

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(
            correlation_id=props.correlation_id
        ),
        body=json.dumps(response)
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)


connection = get_connection()
channel = connection.channel()

channel.queue_declare(queue='user_rpc')
channel.basic_consume(queue='user_rpc', on_message_callback=on_request)

print("👤 Serviço de usuários ativo...")
channel.start_consuming()
        