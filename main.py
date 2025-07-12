import os
import requests
import telegram

HOST = os.getenv('HOST', 'https://hax.co.id')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')  # Telegram 6位登录验证码
TELE_TOKEN = os.getenv('TELE_TOKEN')
TELE_ID = os.getenv('TELE_ID')

session = requests.Session()

def send_telegram(message):
    bot = telegram.Bot(token=TELE_TOKEN)
    bot.send_message(chat_id=TELE_ID, text=message)

def login():
    url = f"{HOST}/api/login/telegram"
    data = {"username": USERNAME, "code": PASSWORD}
    resp = session.post(url, json=data)
    if resp.status_code != 200:
        send_telegram(f"登录失败，HTTP状态码 {resp.status_code}")
        return False
    result = resp.json()
    if result.get('success'):
        send_telegram("登录成功！")
        return True
    else:
        send_telegram(f"登录失败，返回数据: {result}")
        return False

def get_services():
    url = f"{HOST}/api/services"
    resp = session.get(url)
    if resp.status_code != 200:
        send_telegram(f"获取服务失败，HTTP状态码 {resp.status_code}")
        return None
    return resp.json()

def extend_service(svc_id):
    url = f"{HOST}/api/services/{svc_id}/extend"
    resp = session.post(url)
    if resp.status_code == 200:
        send_telegram(f"服务 {svc_id} 续期成功！")
        return True
    else:
        send_telegram(f"服务 {svc_id} 续期失败，HTTP状态码 {resp.status_code}")
        return False

def main():
    if not login():
        return
    services = get_services()
    if not services:
        return
    for svc in services.get('data', []):
        sid = svc.get('id')
        if sid:
            extend_service(sid)

if __name__ == "__main__":
    main()
