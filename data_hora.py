from datetime import datetime
import pytz

# Define o fuso horário de Brasília
fuso_horario_br = pytz.timezone('America/Sao_Paulo')

# Função para obter a data e hora atuais no fuso horário de Brasília
def obter_data_hora_br():
    return datetime.now(fuso_horario_br)

# Formata a data e hora no padrão brasileiro com o fuso horário
def formato_brasileiro():
    return obter_data_hora_br().strftime('%d/%m/%Y %H:%M:%S')

def data():
    return obter_data_hora_br().strftime('%d/%m/%Y')

def hora():
    return obter_data_hora_br().strftime('%H:%M:%S')
