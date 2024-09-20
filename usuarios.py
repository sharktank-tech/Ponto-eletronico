import sqlite3

from admin import is_admin

conn = sqlite3.connect("databases/users.db")

def criar():
    sql = """CREATE TABLE IF NOT EXISTS users (
              id INTEGER PRIMARY KEY, 
              nome TEXT, 
              email TEXT, 
              senha TEXT, 
              is_admin INTEGER DEFAULT 0
          )"""
    conn.execute(sql)
    conn.commit()  # Salva as alterações no banco de dados
    conn.close()
    print("\nTabela criada com sucesso\n")

def tudo():
  sql = "SELECT * FROM users"
  cursor = conn.execute(sql)
  for row in cursor:
    if row == None:
        print('\n----------| empy |-----------\n')
    else:
      print(row)
  cursor.close()


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


print("1 - criar" + "\n" + "2 - tudo" + "\n" + "3 - inserir" + "\n" + "4 - deletar")
entrada = input('Entrada: ')

# Criar novo usuario
if entrada == "1":
  criar()

# Selecionar tudo
if entrada == "2":
  tudo()

# Inserir usuario
if entrada == "3":
  nome = input('Nome: ')
  email = input('Email: ')
  senha = input('Senha: ')
  id = input('ID: ')
  is_admin = input('Admin (1=S/0=N): ')
  inserir(nome, email, senha, id, is_admin)

# Deletar usuario
if entrada == "4":
    id = input("ID: ")
    deletar(id)