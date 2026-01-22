import sys
import os
import json
import pika

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

from messaging import get_connection, publish

PLAYLISTS = {}
playlist_counter = 1

def on_request(ch, method, props, body):
    try:
        request = json.loads(body)
        action = request.get("action")
        response = {}

        if action == "create_playlist":
            playlist_name = request.get("playlist_name")
            user_id = request.get("user_id")
            
            if not playlist_name or not user_id:
                response = {"error": "playlist_name e user_id são obrigatórios"}
            else:
                global playlist_counter
                playlist_id = playlist_counter
                playlist_counter += 1
                
                PLAYLISTS[playlist_id] = {
                    "id": playlist_id,
                    "name": playlist_name,
                    "user_id": user_id,
                    "songs": []
                }
                response = {"status": "Playlist criada com sucesso", "playlist_id": playlist_id}

        elif action == "add_song_to_playlist":
            playlist_id = request.get("playlist_id")
            song_id = request.get("song_id")
            
            if not playlist_id or not song_id:
                response = {"error": "playlist_id e song_id são obrigatórios"}
            elif playlist_id not in PLAYLISTS:
                response = {"error": "Playlist não encontrada"}
            else:
                if song_id not in PLAYLISTS[playlist_id]["songs"]:
                    PLAYLISTS[playlist_id]["songs"].append(song_id)
                    response = {"status": "Música adicionada à playlist com sucesso"}
                else:
                    response = {"status": "Música já está na playlist"}

        elif action == "get_playlist":
            playlist_id = request.get("playlist_id")
            
            if not playlist_id:
                response = {"error": "playlist_id é obrigatório"}
            elif playlist_id not in PLAYLISTS:
                response = {"error": "Playlist não encontrada"}
            else:
                response = {"result": PLAYLISTS[playlist_id]}

        elif action == "list_user_playlists":
            user_id = request.get("user_id")
            
            if not user_id:
                response = {"error": "user_id é obrigatório"}
            else:
                user_playlists = [p for p in PLAYLISTS.values() if p["user_id"] == user_id]
                response = {"result": user_playlists}

        else:
            response = {"error": "Ação inválida"}

    except json.JSONDecodeError:
        response = {"error": "JSON inválido"}
    except Exception as e:
        response = {"error": f"Erro interno: {str(e)}"}

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(
            correlation_id=props.correlation_id
        ),
        body=json.dumps(response)
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = get_connection()
    channel = connection.channel()

    channel.queue_declare(queue='playlist_rpc')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='playlist_rpc', on_message_callback=on_request)

    print("📂 Serviço de playlists ativo...")
    channel.start_consuming()

if __name__ == "__main__":
    main()
