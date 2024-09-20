import sqlite3
from datetime import datetime, time

def format_time_for_sql(time_obj):
    """Converte datetime.time para uma string no formato 'HH:MM:SS'."""
    return time_obj.strftime('%H:%M:%S') if isinstance(time_obj, time) else None

def parse_datetime(dt_str):
    """Converte string de data e hora para datetime, removendo milissegundos se presentes."""
    if isinstance(dt_str, str) and dt_str:
        try:
            return datetime.fromisoformat(dt_str)
        except ValueError:
            print(f"Erro ao converter {dt_str} para datetime.")
            return None
    return None

def inserir(id, user_id, entrada, pausa, retorno, saida):
    try:
        with sqlite3.connect("databases/point.db") as conn:
            sql = """
            INSERT INTO ponto (id, user_id, entrada, pausa, retorno, saida)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            conn.execute(sql, (id, user_id, entrada, pausa, retorno, saida))
            conn.commit()
            print("Registro inserido com sucesso")
            return True
    except sqlite3.Error as e:
        print(f"Erro ao inserir dados: {e}")
        return False

def atualizar(user_id, entrada=None, pausa=None, retorno=None, saida=None):
    try:
        with sqlite3.connect("databases/point.db") as conn:
            sql = """
            UPDATE ponto
            SET entrada = COALESCE(?, entrada),
                pausa = COALESCE(?, pausa),
                retorno = COALESCE(?, retorno),
                saida = COALESCE(?, saida)
            WHERE user_id = ?
            """
            conn.execute(sql, (entrada, pausa, retorno, saida, user_id))
            conn.commit()
            print("Registro atualizado com sucesso")
            return True
    except sqlite3.Error as e:
        print(f"Erro ao atualizar dados: {e}")
        return False

def recuperar(user_id):
    try:
        with sqlite3.connect("databases/point.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ponto WHERE user_id = ?", (user_id,))
            ponto = cursor.fetchone()
            if ponto:
                return {
                    'id': ponto['id'],
                    'user_id': ponto['user_id'],
                    'entrada': ponto['entrada'],
                    'pausa': ponto['pausa'],
                    'retorno': ponto['retorno'],
                    'saida': ponto['saida']
                }
            return None
    except sqlite3.Error as e:
        print(f"Erro ao recuperar dados: {e}")
        return None