from bs4 import BeautifulSoup
import requests
import smtplib
import schedule
import time
from dotenv import load_dotenv
import os

# Load data from .env file
load_dotenv('.env')

# Email details from .env file
sender_email = os.getenv('SENDER_EMAIL')
email_password = os.getenv('EMAIL_PASSWORD')
receiver_email = os.getenv('RECEIVER_EMAIL')

# URL of the item
url = 'https://killcrew.co/collections/mens-bottoms/products/vented-mesh-script-shorts-green-gold?variant=41111394123874'

def check_stock():
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the availability element
    availabile_element = soup.find('div', class_='product-is-available')

    if availabile_element:
        in_stock_notif()
    else:
        out_of_stock_notif()


def out_of_stock_notif():
    subject = 'Item Out of Stock'
    message_body = 'The Green KillCrew shorts are still out of stock. I`ll check again later!\n\n\n-ThePyStockBot'
    send_email(subject, message_body)

def in_stock_notif():
    subject = 'Item Back in Stock!'
    message_body = f'The Green KillCrew shorts are back in stock! Check it out here before they`re gone: {url}\n\n\n-ThePyStockBot'
    send_email(subject, message_body)


def send_email(subject, message_body):
    # Create message
    message = f"Subject: {subject}\n\n{message_body}"

    # Connect to SMTP server
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, email_password)
        server.sendmail(sender_email, receiver_email, message)
        print('Notification sent!')


# Run the script 
check_stock()

# Run the script every 3 days
schedule.every(3).days.do(check_stock)

while True:
    schedule.run_pending()
    time.sleep(1)