import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os

def send_email(text):
    EMAIL_USER = os.environ["EMAIL_USER"]
    EMAIL_PASS = os.environ["EMAIL_PASS"]

    # <<< Указываешь реальные адреса тут (пример) >>>
    recipients = [
        "KZJ78@yandex.ru",
        "alex77st@mail.ru" 
    ]
    # <<< Конец списка адресатов >>>

    msg = MIMEText(text, "plain", "utf-8")
    msg["Subject"] = "Цены на золото (585, 750, 999)"
    msg["From"] = EMAIL_USER
    msg["To"] = ", ".join(recipients)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)
    server.sendmail(EMAIL_USER, recipients, msg.as_string())
    server.quit()


def handler(request):
    try:
        url = "https://m-lombard.kz/"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        # Ищем элементы с ценами (возможно .main-cost и .small-cost)
        prices_raw = soup.select(".main-cost, .small-cost")
        prices = [p.get_text(strip=True) for p in prices_raw]

        price_585 = prices[0] if len(prices) > 0 else "Нет данных"
        price_750 = prices[1] if len(prices) > 1 else "Нет данных"
        price_999 = prices[2] if len(prices) > 2 else "Нет данных"

        text = (
            "Текущие цены на золото:\n"
            f"585 проба: {price_585}\n"
            f"750 проба: {price_750}\n"
            f"999 проба: {price_999}\n"
        )

        send_email(text)

        # Vercel ожидает возвращаемое значение; возвращаем JSON-подобную строку
        return {
            "status": 200,
            "body": text
        }

    except Exception as e:
        return {
            "status": 500,
            "body": f"Error: {str(e)}"
        }
