import json
import pika
from messaging import get_connection, RpcClient

def on_request(ch, method, props, body):
    try:
        request = json.loads(body)
        action = request.get('action')
        response = {}

        rpc = RpcClient()

        if action == 'search_music':
            response = rpc.call('catalog_rpc', request)
        elif action == 'list_all':
            response = rpc.call('catalog_rpc', request)
        elif action == 'get_song_by_id':
            response = rpc.call('catalog_rpc', request)
        elif action == 'create_playlist':
            response = rpc.call('playlist_rpc', request)
        elif action == 'add_song_to_playlist':
            response = rpc.call('playlist_rpc', request)
        elif action == 'get_playlist':
            response = rpc.call('playlist_rpc', request)
        elif action == 'list_user_playlists':
            response = rpc.call('playlist_rpc', request)
        elif action == 'get_user_history':
            response = rpc.call('user_rpc', request)
        elif action == 'get_user_info':
            response = rpc.call('user_rpc', request)
        elif action == 'register_play':
            response = rpc.call('user_rpc', request)
        else:
            response = {'error': 'Ação desconhecida'}

    except json.JSONDecodeError:
        response = {'error': 'JSON inválido na requisição'}
    except Exception as e:
        response = {'error': f'Erro no gateway: {str(e)}'}

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

channel.queue_declare(queue='gateway_rpc')
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='gateway_rpc', on_message_callback=on_request)

print("🚪 Gateway aguardando requisições...")
channel.start_consuming()
