from flask import Flask, render_template, redirect, url_for, session, flash, request
import users_manage
import point_manage
import sqlite3
import random
from data_hora import obter_data_hora_br, formato_brasileiro
import logging
import os
from info import calcular_horas_salario
import admin

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')  # Carrega a chave secreta da variável de ambiente

# Configura logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

def obter_conexao_banco(db_path):
    return sqlite3.connect(db_path, check_same_thread=False)

def verifica_limite_marcacoes(user_id):
    hoje = formato_brasileiro()[:10]  # Extrai apenas a data 'DD/MM/YYYY'
    print(f"verifica_limite: {hoje}")

    try:
        with obter_conexao_banco("databases/point.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            # Ajuste para considerar apenas a data na comparação
            cursor.execute("""
                SELECT 
                    entrada, pausa, retorno, saida 
                FROM ponto 
                WHERE user_id = ? 
                AND SUBSTR(entrada, 1, 10) = ?
            """, (user_id, hoje))
            ponto = cursor.fetchone()

            if ponto:
                logging.info(f"Marcações retornadas para {hoje}: {ponto['entrada']}, {ponto['pausa']}, {ponto['retorno']}, {ponto['saida']}")
                todas_marcacoes = all(ponto[coluna] is not None for coluna in ['entrada', 'pausa', 'retorno', 'saida'])
                return todas_marcacoes
            else:
                logging.info("Nenhuma marcação encontrada para hoje.")
            return False

    except sqlite3.Error as e:
        logging.error(f"Erro ao verificar limite de marcações: {e}")
        return False


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        user_id = random.randint(10, 50000)
        is_admin = None

        try:
            users_manage.inserir(nome, email, senha, user_id, is_admin)
            flash('Usuário registrado com sucesso!')
            return redirect(url_for('login'))
        except Exception as e:
            logging.error(f"Erro ao registrar usuário: {e}")
            flash(f'Erro ao registrar usuário: {e}')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        try:
            with obter_conexao_banco('databases/users.db') as conn:
                conn.row_factory = sqlite3.Row
                user = conn.execute('SELECT * FROM users WHERE email = ? AND senha = ?', (email, senha)).fetchone()

            if user:
                session['user_id'] = user['id']
                session['username'] = user['nome']
                flash('Login realizado com sucesso!')
                return redirect(url_for('index'))
            else:
                flash('Email ou senha incorretos.')

        except sqlite3.Error as e:
            logging.error(f"Erro ao acessar o banco de dados: {e}")
            flash(f'Erro ao acessar o banco de dados: {e}')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Você foi desconectado.')
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
def administrar():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    # Verifique se o usuário é um administrador
    if not admin.is_admin(user_id):
        flash('Você não tem permissão para acessar esta página.')
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Lidar com operações de administração (adicionar, atualizar, deletar)
        operacao = request.form.get('operacao')
        if operacao == 'adicionar':
            # Lógica para adicionar um novo item
            admin.adicionar_item(request.form)
        elif operacao == 'atualizar':
            # Lógica para atualizar um item existente
            admin.atualizar_item(request.form)
        elif operacao == 'deletar':
            # Lógica para deletar um item existente
            admin.deletar_item(request.form.get('id'))

        flash(f'Operação {operacao} realizada com sucesso!')
        return redirect(url_for('admin'))

    # Recuperar dados para exibir na página de administração
    items = admin.recuperar_todos_itens()

    return render_template('admin.html', items=items)


@app.route('/conta')
def conta(user_id=None):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if user_id is None:
        user_id = session['user_id']

    try:
        with obter_conexao_banco('databases/users.db') as conn:
            user_row = conn.execute('SELECT nome FROM users WHERE id = ?', (user_id,)).fetchone()
            user = user_row[0] if user_row else 'Usuário não encontrado'

            # Calcula o salario
            horas_trabalhadas, salario = calcular_horas_salario(user_id)

        if user:
            return render_template('conta.html', user=user, horas_trabalhadas=horas_trabalhadas, salario=salario)
        else:
            flash('Usuário não encontrado.')
            logging.error("Usuario não encontrado.")
            return redirect(url_for('login'))

    except sqlite3.Error as e:
        logging.error(f"Erro ao acessar o banco de dados: {e}")
        flash(f'Erro ao acessar o banco de dados: {e}')
        return render_template('conta.html')

@app.route('/')
def index():
    if 'username' in session:
        user_id = session.get('user_id')
        point_data = point_manage.recuperar(user_id) or {
            'entrada': None,
            'pausa': None,
            'retorno': None,
            'saida': None
        }

        hoje = obter_data_hora_br()

        formatted_point_data = {
            key: (str(value)[:19] if value else 'Não registrado')  # Converte para string e corta para exibir apenas até os segundos
            for key, value in point_data.items()
        }

        all_registered_today = all(
            value and value[:10] == str(hoje)
            for value in (
                formatted_point_data.get('entrada'),
                formatted_point_data.get('pausa'),
                formatted_point_data.get('retorno'),
                formatted_point_data.get('saida')
            )
        )

        can_register = verificar_se_pode_registrar(user_id) and not all_registered_today

        return render_template(
            'index.html',
            username=session['username'],
            user_id=user_id,
            point_data=formatted_point_data,
            can_register=can_register,
            current_time=obter_data_hora_br()
        )

    return redirect(url_for('login'))

@app.route('/registrar_ponto', methods=['POST'])
def registrar_ponto():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session.get('user_id')

    if verifica_limite_marcacoes(user_id):
        flash('Você já atingiu o limite de marcações para hoje.')
        logging.info(f'Usuário {user_id} já atingiu o limite de marcações para hoje.')
        return redirect(url_for('index'))

    try:
        ponto_atual = point_manage.recuperar(user_id)

        if ponto_atual is None:
            point_manage.inserir(
                id=None,
                user_id=user_id,
                entrada=None,
                pausa=None,
                retorno=None,
                saida=None
            )
            ponto_atual = point_manage.recuperar(user_id)

        if not ponto_atual['entrada']:
            tipo_registro = 'entrada'
        elif not ponto_atual['pausa']:
            tipo_registro = 'pausa'
        elif not ponto_atual['retorno']:
            tipo_registro = 'retorno'
        elif not ponto_atual['saida']:
            tipo_registro = 'saida'
        else:
            flash('Todas as marcações para hoje já foram feitas.')
            return redirect(url_for('index'))

        data_hora_registro = formato_brasileiro()
        print(f"data e hora do registro: {data_hora_registro}")
        print(type(data_hora_registro))

        point_manage.atualizar(
            user_id=user_id,
            entrada=data_hora_registro if tipo_registro == 'entrada' else ponto_atual['entrada'],
            pausa=data_hora_registro if tipo_registro == 'pausa' else ponto_atual['pausa'],
            retorno=data_hora_registro if tipo_registro == 'retorno' else ponto_atual['retorno'],
            saida=data_hora_registro if tipo_registro == 'saida' else ponto_atual['saida']
        )

        flash(f'{tipo_registro.capitalize()} registrada com sucesso!')
        logging.info(f'{tipo_registro.capitalize()} registrada com sucesso!')
    except Exception as e:
        logging.error(f'Erro ao registrar ponto: {e}')

    return redirect(url_for('index'))


def verificar_se_pode_registrar(user_id):
    hoje = formato_brasileiro()[:10]  # Extrai apenas a data 'DD/MM/YYYY'
    print(f"verificar_se_pode_registrar - Data de hoje: {hoje}")

    conn = None
    try:
        conn = sqlite3.connect("databases/point.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                entrada, pausa, retorno, saida 
            FROM ponto 
            WHERE user_id = ? 
            AND SUBSTR(entrada, 1, 10) = ?
        """, (user_id, hoje))

        ponto = cursor.fetchone()

        if not ponto:
            logging.info("Nenhuma marcação encontrada para hoje. Pode registrar.")
            return True

        entrada = ponto['entrada']
        pausa = ponto['pausa']
        retorno = ponto['retorno']
        saida = ponto['saida']

        if entrada and pausa and retorno and saida:
            logging.info(f"Limite de marcações atingido para {user_id} no dia {hoje}.")
            return False

        logging.info("Ainda há marcações disponíveis para registrar.")
        return True

    except sqlite3.Error as e:
        logging.error(f"Erro ao verificar registro: {e}")
        return False

    finally:
        if conn:
            conn.close()


# Rota para enviar um relatório por e-mail
@app.route('/enviar_email', methods=['GET', 'POST'])
def enviar_email_route():
    render_template("email.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)