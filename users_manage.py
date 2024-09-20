import sqlite3

def tudo():
    conn = sqlite3.connect("databases/users.db")
    sql = "SELECT * FROM users"
    cursor = conn.execute(sql)
    for row in cursor:
        print(row)
    conn.close()
    print('---------------------')

def criar():
    conn = sqlite3.connect("databases/users.db")
    sql = """CREATE TABLE IF NOT EXISTS users (
              id INTEGER PRIMARY KEY, 
              nome TEXT, 
              email TEXT, 
              senha TEXT, 
              is_admin INTEGER DEFAULT 0
          )"""
    conn.execute(sql)
    print("Tabela criada com sucesso")
    conn.close()

def inserir(nome, email, senha, id, is_admin):
    conn = None
    try:
        conn = sqlite3.connect("databases/users.db")
        sql = "INSERT INTO users (id, nome, email, senha, is_admin) VALUES (?, ?, ?, ?, ?)"
        conn.execute(sql, (id, nome, email, senha, is_admin))
        conn.commit()
        print("Registro inserido com sucesso")
    except sqlite3.IntegrityError as e:
        print(f"Erro de integridade: {e}")
    except sqlite3.OperationalError as e:
        print(f"Erro operacional: {e}")
    except sqlite3.Error as e:
        print(f"Erro ao inserir dados: {e}")
    finally:
        if conn:
            conn.close()
            print("Conexão fechada")

def atualizar(id, nome, email, senha, is_admin):
    conn = None
    try:
        conn = sqlite3.connect("databases/users.db")
        sql = "UPDATE users SET nome = ?, email = ?, senha = ?, is_admin = ? WHERE id = ?"
        conn.execute(sql, (nome, email, senha, id, is_admin))
        conn.commit()
        print("Registro atualizado com sucesso")
    except sqlite3.IntegrityError as e:
        print(f"Erro de integridade: {e}")
    except sqlite3.OperationalError as e:
        print(f"Erro operacional: {e}")
    except sqlite3.Error as e:
        print(f"Erro ao atualizar dados: {e}")
    finally:
        if conn:
            conn.close()
            print("Conexão fechada")

def deletar(id):
    conn = None
    try:
        conn = sqlite3.connect("databases/users.db")
        sql = "DELETE FROM users WHERE id = ?"
        conn.execute(sql, (id,))
        conn.commit()
        print("Registro deletado com sucesso")
    except sqlite3.Error as e:
        print(f"Erro ao deletar dados: {e}")
    finally:
        if conn:
            conn.close()
            print("Conexão fechada")