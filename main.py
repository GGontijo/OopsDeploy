from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import os
import requests

app = FastAPI()

TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""

def notificar(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("Notificação enviada com sucesso!")
        else:
            print(f"Falha ao enviar notificação. Status code: {response.status_code}")
    except Exception as e:
        print(f"Erro ao enviar mensagem ao Telegram: {e}")

@app.post("/webhook")
async def webhook(request: Request):
    #return {"message": "Temporariamente inativo..."}, 200
    ip_remetente = request.headers.get('X-Forwarded-For', request.client.host)

    # Faz o git pull e reinicia o docker-compose
    os.system('cd /root/bot-video-downloader/ && git pull origin main')
    os.system('cd /root/bot-video-downloader/ && docker-compose up --build -d')

    # Notificar via Telegram
    mensagem = (
        f"Deploy realizado com sucesso!\n\n"
        f"IP do remetente: {ip_remetente}\n"
    )
    notificar(mensagem)
    return {"message": "Deploy realizado com sucesso!"}, 200

@app.post("/up")
async def up(request: Request):
    ip_remetente = request.headers.get('X-Forwarded-For', request.client.host)

    # Faz o git pull e reinicia o docker-compose
    os.system('cd /root/bot-video-downloader/ && docker-compose up -d')

    # Notificar via Telegram
    mensagem = (
        f"Failover realizado, Container subiu!\n\n"
        f"IP do remetente: {ip_remetente}\n"
    )
    notificar(mensagem)
    return {"message": "Failover realizado, Container subiu!"}, 200

@app.post("/down")
async def down(request: Request):
    ip_remetente = request.headers.get('X-Forwarded-For', request.client.host)

    # Faz o git pull e reinicia o docker-compose
    os.system('cd /root/bot-video-downloader/ && docker-compose down')

    # Notificar via Telegram
    mensagem = (
        f"Failover finalizado, Container foi desligado!\n\n"
        f"IP do remetente: {ip_remetente}\n"
    )
    notificar(mensagem)
    return {"message": "Failover finalizado, Container foi desligado!"}, 200
