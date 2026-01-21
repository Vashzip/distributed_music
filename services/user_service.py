import sys
import os
import json
import pika

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

from messaging import get_connection, publish

USERS = {
    1: {"id": 1, "name": "João", "history": []},
    2: {"id": 2, "name": "Maria", "history": []},
    3: {"id": 3, "name": "Pedro", "history": []}
}

def on_request(ch, method, props, body):
    try:
        request = json.loads(body)
        action = request.get("action")
        response = {}

        if action == "get_user_history":
            user_id = request.get("user_id")
            
            if not user_id:
                response = {"error": "user_id é obrigatório"}
            elif user_id not in USERS:
                response = {"error": "Usuário não encontrado"}
            else:
                response = {"result": USERS[user_id]["history"]}

        elif action == "get_user_info":
            user_id = request.get("user_id")
            
            if not user_id:
                response = {"error": "user_id é obrigatório"}
            elif user_id not in USERS:
                response = {"error": "Usuário não encontrado"}
            else:
                response = {"result": USERS[user_id]}

        elif action == "register_play":
            user_id = request.get("user_id")
            song_title = request.get("song_title")
            
            if not user_id or not song_title:
                response = {"error": "user_id e song_title são obrigatórios"}
            elif user_id not in USERS:
                response = {"error": "Usuário não encontrado"}
            else:
                play_entry = {
                    "song": song_title,
                    "timestamp": request.get("timestamp", "")
                }
                USERS[user_id]["history"].append(play_entry)
                
                if len(USERS[user_id]["history"]) > 50:
                    USERS[user_id]["history"].pop(0)
                
                response = {"status": "Reprodução registrada com sucesso"}
                
                publish("play_history_events", {
                    "user_id": user_id,
                    "song_title": song_title,
                    "type": "song_played"
                })

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


connection = get_connection()
channel = connection.channel()

channel.queue_declare(queue='user_rpc')
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='user_rpc', on_message_callback=on_request)

print("👤 Serviço de usuários ativo...")
channel.start_consuming()
