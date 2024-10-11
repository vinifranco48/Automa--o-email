import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime, timedelta
import pytz
import sys

# Configuração para desabilitar o buffering da saída
sys.stdout.reconfigure(line_buffering=True)

print("Script iniciado")

# Configurações de e-mail
sender_email = os.environ.get('SENDER_EMAIL', 'viniabreu48@gmail.com')
sender_password = os.environ.get('SENDER_PASSWORD', 'nzbxlalkxvbkbmyo')
form_link = "https://docs.google.com/forms/d/e/1FAIpQLSe_O5UtAmylzedWZwxUwpn18AByCj9h9zzj1csEGgDUXwWLzw/viewform"

print(f"Configurações de e-mail: sender_email={sender_email}, senha={'*' * len(sender_password) if sender_password else 'Não definida'}")

# Lista de destinatários e dias para envio
recipients = {
    "viniabreu48@gmail.com": "Thursday"
}

print(f"Destinatários configurados: {recipients}")

# Configuração do fuso horário do Brasil
brazil_tz = pytz.timezone('America/Sao_Paulo')

# Horário de envio
SEND_TIME = "17:35"

def send_email(recipient):
    now = datetime.now(brazil_tz)
    print(f"Função send_email chamada em {now.strftime('%Y-%m-%d %H:%M:%S')} para {recipient}")
    
    if now.strftime('%A') != 'Thursday':
        print(f"Hoje não é quinta-feira. E-mail não será enviado.")
        return
    
    print(f"Tentando enviar e-mail para {recipient}")
    subject = "Link do Formulário"
    body = f"Olá! Aqui está o link para o formulário: {form_link}"
    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)
        print(f"E-mail enviado com sucesso para {recipient}")
    except Exception as e:
        print(f"Erro ao enviar e-mail para {recipient}: {str(e)}")

def schedule_emails():
    for email, day in recipients.items():
        schedule.every().thursday.at(SEND_TIME).do(send_email, recipient=email).tag('email_task')
    print(f"E-mails agendados para {SEND_TIME}")
    print(f"Próximas tarefas agendadas: {schedule.get_jobs()}")

def check_and_run_tasks():
    now = datetime.now(brazil_tz)
    if now.strftime('%A') == 'Thursday':
        current_time = now.strftime('%H:%M')
        if current_time >= SEND_TIME:
            print(f"Horário atual ({current_time}) >= horário de envio ({SEND_TIME}). Verificando tarefas.")
            for job in schedule.get_jobs('email_task'):
                if job.should_run:
                    print(f"Executando tarefa: {job}")
                    job.run()
                else:
                    print(f"Tarefa não deve ser executada: {job}")
    schedule.run_pending()

def run_pending():
    last_minute = -1
    while True:
        now = datetime.now(brazil_tz)
        if now.minute != last_minute:
            print(f"Verificação de tarefas pendentes em {now.strftime('%Y-%m-%d %H:%M:%S')} (Dia da semana: {now.strftime('%A')})")
            last_minute = now.minute
        check_and_run_tasks()
        time.sleep(1)  

if __name__ == "__main__":
    schedule_emails()
    now = datetime.now(brazil_tz)
    print(f"Agendamento iniciado. Horário atual no Brasil: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    if now.strftime('%A') == 'Thursday' and now.strftime('%H:%M') >= SEND_TIME:
        print("Horário de envio já passou. Tentando enviar e-mail imediatamente.")
        for email in recipients:
            send_email(email)
    print("Pressione Ctrl+C para sair.")
    run_pending()