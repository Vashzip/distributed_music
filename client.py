import json
import time
from messaging import RpcClient

def print_response(action, response):
    print(f"\n{'='*50}")
    print(f"Ação: {action}")
    print(f"Resposta: {json.dumps(response, indent=2, ensure_ascii=False)}")
    print(f"{'='*50}\n")

def main():
    print("🎵 Cliente do Sistema de Streaming de Música")
    print("Conectando ao gateway...\n")
    
    rpc = RpcClient()
    
    try:
        print("1️⃣ Buscando músicas por 'Funk'...")
        response = rpc.call('gateway_rpc', {
            'action': 'search_music',
            'query': 'Funk'
        })
        print_response('search_music', response)
        
        print("2️⃣ Listando todas as músicas...")
        response = rpc.call('gateway_rpc', {
            'action': 'list_all'
        })
        print_response('list_all', response)
        
        print("3️⃣ Buscando música específica por ID...")
        response = rpc.call('gateway_rpc', {
            'action': 'get_song_by_id',
            'song_id': 1
        })
        print_response('get_song_by_id', response)
        
        print("4️⃣ Criando playlist para usuário...")
        response = rpc.call('gateway_rpc', {
            'action': 'create_playlist',
            'playlist_name': 'Minhas Favoritas',
            'user_id': 1
        })
        print_response('create_playlist', response)
        playlist_id = response.get('playlist_id')
        
        if playlist_id:
            print(f"5️⃣ Adicionando música à playlist {playlist_id}...")
            response = rpc.call('gateway_rpc', {
                'action': 'add_song_to_playlist',
                'playlist_id': playlist_id,
                'song_id': 1
            })
            print_response('add_song_to_playlist', response)
            
            print(f"6️⃣ Adicionando mais uma música à playlist {playlist_id}...")
            response = rpc.call('gateway_rpc', {
                'action': 'add_song_to_playlist',
                'playlist_id': playlist_id,
                'song_id': 2
            })
            print_response('add_song_to_playlist', response)
            
            print(f"7️⃣ Obtendo detalhes da playlist {playlist_id}...")
            response = rpc.call('gateway_rpc', {
                'action': 'get_playlist',
                'playlist_id': playlist_id
            })
            print_response('get_playlist', response)
        
        print("8️⃣ Listando playlists do usuário 1...")
        response = rpc.call('gateway_rpc', {
            'action': 'list_user_playlists',
            'user_id': 1
        })
        print_response('list_user_playlists', response)
        
        print("9️⃣ Obtendo histórico do usuário 1...")
        response = rpc.call('gateway_rpc', {
            'action': 'get_user_history',
            'user_id': 1
        })
        print_response('get_user_history', response)
        
        print("🔟 Obtendo informações do usuário 1...")
        response = rpc.call('gateway_rpc', {
            'action': 'get_user_info',
            'user_id': 1
        })
        print_response('get_user_info', response)
        
        print("1️⃣1️⃣ Registrando reprodução de música (comunicação síncrona via RPC)...")
        response = rpc.call('gateway_rpc', {
            'action': 'register_play',
            'user_id': 1,
            'song_title': 'Tá OK',
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        })
        print_response('register_play', response)
        
        print("1️⃣2️⃣ Obtendo histórico atualizado do usuário 1...")
        response = rpc.call('gateway_rpc', {
            'action': 'get_user_history',
            'user_id': 1
        })
        print_response('get_user_history', response)
        
        print("✅ Todas as operações concluídas com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
    finally:
        rpc.close()

if __name__ == "__main__":
    main()
