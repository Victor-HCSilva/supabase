from .supabase_client import supabase
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def get_users(request: HttpRequest):
    response = supabase.table('users').select("*").execute()
    return JsonResponse(response.data, safe=False)


@csrf_exempt#sem csrf token
def add_user_api(request: HttpRequest):
    # 1. Garantir que a requisição é do tipo POST
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido. Use POST.'}, status=405)

    try:
        data = json.loads(request.body)

        if 'name' not in data or 'password' not in data:
            return JsonResponse({'error': 'Campos "name" e "password" são obrigatórios.'}, status=400)

        response = supabase.table('users').insert(data).execute()

        return JsonResponse(response.data, safe=False, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido no corpo da requisição.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt#sem csrf token
def delete_user(request: HttpRequest):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Método não permitido. Use DELETE.'}, status=405)

    try:
        data = json.loads(request.body)

        conditions = not 'id' in data or not 'name' in data

        if conditions:
            return JsonResponse({'error': 'Campo id obrigatório.'}, status=400)

        response = supabase.table('users').delete()\
            .eq('name', data['name'])\
            .eq('id',data['id'] )\
            .execute()

        return JsonResponse(response.data, safe=False, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido no corpo da requisição.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def update_user_api(request: HttpRequest, user_id: int): # O ID correto vem daqui
    if request.method != 'PATCH':
        return JsonResponse({'error': 'Método não permitido. Use PATCH para atualizações.'}, status=405)

    try:
        update_data = json.loads(request.body)

        if not update_data:
            return JsonResponse({'error': 'Corpo da requisição não pode ser vazio.'}, status=400)

        # --- CORREÇÃO E MELHORIA DE SEGURANÇA ---
        # É uma boa prática remover o campo 'id' do corpo da requisição,
        # para garantir que ninguém tente alterar o ID do usuário, que deve ser imutável.
        # O método .pop() remove a chave e retorna o valor (que não usaremos),
        # o segundo argumento 'None' evita um erro caso o 'id' não esteja no JSON.
        update_data.pop('id', None)

        # --- CORREÇÃO DA LÓGICA ---
        # Use o 'user_id' que veio da URL para encontrar o registro.
        response = supabase.table('users').update(update_data).eq('id', user_id).execute()

        # Verificar se o usuário foi encontrado e atualizado
        if not response.data:
            # --- CORREÇÃO DA MENSAGEM DE ERRO ---
            # Use a variável 'user_id' na mensagem.
            return JsonResponse({'error': f'Usuário com id {user_id} não encontrado.'}, status=404)

        # Retornar os dados atualizados como confirmação
        return JsonResponse(response.data, safe=False, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido no corpo da requisição.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
