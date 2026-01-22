import sys
import os
import json
import pika

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

from messaging import get_connection



# ===== BANCO MOCKADO (TOP BRASIL) =====
MUSIC_DB = [
    {"id": 1, "title": "Tá OK", "artist": "DENNIS & Kevin O Chris", "genre": "Funk"},
    {"id": 2, "title": "Ela Não Anda Só", "artist": "MC Ryan SP", "genre": "Funk"},
    {"id": 3, "title": "Leão", "artist": "Marília Mendonça", "genre": "Sertanejo"},
    {"id": 4, "title": "Malvadão 3", "artist": "Xamã", "genre": "Rap"},
    {"id": 5, "title": "Poesia Acústica #13", "artist": "Pineapple Storm", "genre": "Rap"},
    {"id": 6, "title": "Zona de Perigo", "artist": "Léo Santana", "genre": "Axé"},
    {"id": 7, "title": "Nosso Quadro", "artist": "Ana Castela", "genre": "Sertanejo"},
    {"id": 8, "title": "Haja Colírio", "artist": "Guilherme & Benuto", "genre": "Sertanejo"},
    {"id": 9, "title": "Eu Gosto Assim", "artist": "Gustavo Mioto & Mari Fernandez", "genre": "Sertanejo"},
    {"id": 10, "title": "Me Porto Bonito", "artist": "Bad Bunny & Chencho Corleone", "genre": "Pop Latino"},
]

QUEUE = "catalog_rpc"

def on_request(ch, method, props, body):
    try:
        request = json.loads(body)
        action = request.get("action")

        if action == "search_music":
            query = request.get("query", "")
            if not query:
                response = {"error": "query é obrigatório"}
            else:
                query = str(query).lower()
                result = [
                    m for m in MUSIC_DB
                    if query in m["title"].lower()
                    or query in m["artist"].lower()
                    or (m["genre"] and query in m["genre"].lower())
                ]
                response = {"result": result}

        elif action == "list_all":
            response = {"result": MUSIC_DB}

        elif action == "get_song_by_id":
            song_id = request.get("song_id")
            if not song_id:
                response = {"error": "song_id é obrigatório"}
            else:
                song = next((m for m in MUSIC_DB if m["id"] == song_id), None)
                if song:
                    response = {"result": song}
                else:
                    response = {"error": "Música não encontrada"}

        else:
            response = {"error": "Ação inválida"}

    except json.JSONDecodeError:
        response = {"error": "JSON inválido"}
    except Exception as e:
        response = {"error": f"Erro interno: {str(e)}"}

    ch.basic_publish(
        exchange="",
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

    channel.queue_declare(queue=QUEUE)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE, on_message_callback=on_request)

    print("🎵 Catalog Service (Top BR) rodando...")
    channel.start_consuming()

if __name__ == "__main__":
    main()
