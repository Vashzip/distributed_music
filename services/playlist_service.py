import sys
import os
import json
import pika

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

from messaging import get_connection


def on_request(ch, method, props, body):
    request = json.loads(body)

    response = {
        'status': 'Playlist criada com sucesso'
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

channel.queue_declare(queue='playlist_rpc')
channel.basic_consume(queue='playlist_rpc', on_message_callback=on_request)

print("📂 Serviço de playlists ativo...")
channel.start_consuming()
