import sqlite3
import logging

def obter_conexao_banco(db_path):
    return sqlite3.connect(db_path, check_same_thread=False)

def is_admin(user_id):
    # Verifica no banco de dados se o usuário tem privilégios de administrador
    try:
        with obter_conexao_banco('databases/users.db') as conn:
            cursor = conn.cursor()
            user = cursor.execute('SELECT is_admin FROM users WHERE id = ?', (user_id,)).fetchone()
            return user and user[0] == 1
    except sqlite3.Error as e:
        logging.error(f"Erro ao verificar privilégios de administrador: {e}")
        return False

def adicionar_item(form_data):
    # Implementar lógica para adicionar item
    pass

def atualizar_item(form_data):
    # Implementar lógica para atualizar item
    pass

def deletar_item(item_id):
    # Implementar lógica para deletar item
    pass

def recuperar_todos_itens():
    # Recupera todos os itens para exibir na página de administração
    try:
        with obter_conexao_banco('databases/point.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM ponto')
            itens = cursor.fetchall()
            cursor.close()  # Fechando o cursor explicitamente
            return itens
    except sqlite3.Error as e:
        logging.error(f"Erro ao recuperar itens: {e}")
        return []
