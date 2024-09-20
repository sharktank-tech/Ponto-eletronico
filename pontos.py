import sqlite3
from datetime import datetime

conn = sqlite3.connect("databases/point.db")

def criar():
  sql = """
    CREATE TABLE IF NOT EXISTS ponto (
        id INTEGER,
        user_id INTEGER,
        entrada TEXT,
        pausa TEXT,
        retorno TEXT,
        saida TEXT,
        PRIMARY KEY (id)
  )
  """
  conn.execute(sql)
  conn.commit()  # Salva as alterações no banco de dados
  conn.close()
  print("\nTabela criada com sucesso\n")

def tudo():
  sql = "SELECT * FROM ponto"
  cursor = conn.execute(sql)
  for row in cursor:
    if row == None:
        print('\n----------| empy |-----------\n')
    else:    
      print(row)
  conn.close()

def atualizar(user_id, entrada, pausa, retorno, saida):
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



def inserir(id, user_id, entrada, pausa, retorno, saida):
    try:
        with sqlite3.connect("databases/point.db") as conn:
            sql = """
            INSERT INTO ponto (id, user_id, entrada, pausa, retorno, saida)
            VALUES (?, ?, ?, ?, ?, ?) 
            """
            # Converte para o formato ISO 8601 se as variáveis forem datetime
            entrada_iso = entrada.isoformat() if hasattr(entrada, 'isoformat') else entrada
            pausa_iso = pausa.isoformat() if hasattr(pausa, 'isoformat') else pausa
            retorno_iso = retorno.isoformat() if hasattr(retorno, 'isoformat') else retorno
            saida_iso = saida.isoformat() if hasattr(saida, 'isoformat') else saida

            conn.execute(sql, (id, user_id, entrada_iso, pausa_iso, retorno_iso, saida_iso))
            conn.commit()
            print("Registro inserido com sucesso")
            return True

    except sqlite3.Error as e:
        print(f"Erro ao inserir dados: {e}")
        return False



def deletar(id):
    conn = None
    try:
        conn = sqlite3.connect("databases/point.db")
        sql = "DELETE  FROM ponto WHERE id = ?"
        conn.execute(sql, (id,))
        conn.commit()
        print(f"Registro {id} deletado com sucesso")
    except sqlite3.Error as e:
        print(f"Erro ao deletar dados: {e}")
    finally:
        if conn:
            conn.close()
            print("Conexão fechada")
    


print("1 - criar" + "\n" + "2 - tudo" + "\n" + "3 - atualizar" + "\n" + "4 - Inserir" + "\n" + "5 - deletar")
entrada = input('Entrada: ')

# Criar usuário
if entrada == "1":
    criar()

# Selecionar usuário
if entrada == "2":
    tudo()

# Atualizar usuário
if entrada == "3":
    user_id = input('user_id: ')
    entrada = input('entrada: ')
    pausa = input('pausa: ')
    retorno = input('retorno: ')
    saida = input('saida: ')
    atualizar(user_id, entrada, pausa, retorno, saida)

# Inserir usuário
if entrada == "4":
    id = input('id: ')
    user_id = input('user_id: ')
    entrada = input('entrada: ')
    pausa = input('pausa: ')
    retorno = input('retorno: ')
    saida = input('saida: ')
    inserir(id, user_id, entrada, pausa, retorno, saida)

# Deletar usuário
elif entrada == "5":
    id = input("ID: ")
    deletar(id)