import sqlite3
from datetime import datetime
import logging
from collections import defaultdict


def calcular_horas_salario(user_id):
    try:
        # Conectando ao banco de dados
        conn = sqlite3.connect('databases/point.db')
        cursor = conn.cursor()

        # Recuperando dados de entrada e saída do banco de dados
        cursor.execute('''SELECT entrada, saida FROM ponto WHERE user_id = ?''', (user_id,))
        registros = cursor.fetchall()
        print(f"Registros: {registros}")

        # Dicionário para armazenar horas por dia
        horas_por_dia = defaultdict(float)

        for entrada, saida in registros:
            if entrada and saida:
                try:
                    # Convertendo strings de data para objetos datetime
                    entrada_hora = datetime.strptime(entrada, '%d/%m/%Y %H:%M:%S')
                    saida_hora = datetime.strptime(saida, '%d/%m/%Y %H:%M:%S')

                    # Calculando as horas trabalhadas no dia
                    horas_trabalhadas = (saida_hora - entrada_hora).total_seconds() / 3600  # Convertendo para horas

                    # Somando as horas ao dicionário, agrupando por data
                    dia = entrada_hora.date()  # Obtém a data sem hora
                    horas_por_dia[dia] += horas_trabalhadas

                except ValueError as e:
                    logging.error(f"Erro ao converter data/hora: {e}")

        # Calculando o total de horas e salário
        total_horas = sum(horas_por_dia.values())
        taxa_hora = 50.0  # Exemplo de taxa horária
        salario = total_horas * taxa_hora

        # Retornando as horas trabalhadas e o salário calculado
        return round(total_horas, 2), round(salario, 2)

    except sqlite3.Error as e:
        logging.error(f"Erro ao acessar o banco de dados: {e}")
        return 0, 0

    finally:
        # Garantindo que a conexão com o banco de dados seja fechada
        if conn:
            conn.close()