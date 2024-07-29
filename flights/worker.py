import pika
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import django
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Set up Django environment
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'indigo.settings')
django.setup()

from flights.models import User  # Import the User model

def send_email(to_email, subject, body):
    from_email = os.getenv('EMAIL_USER')
    password = os.getenv('EMAIL_PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

def callback(ch, method, properties, body):
    data = json.loads(body)
    print("data:", data)
    
    flight_details = data['flight_details']
    status = data['status']

    # Fetch all users
    users = User.objects.all()

    for user in users:
        user_email = user.email
        user_name = user.name

        subject = f"Flight Status Update: {status}"
        message = f"Dear {user_name},\n\nYour flight details are as follows:\n{flight_details}\n\nStatus: {status}"

        send_email(user_email, subject, message)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='notifications')

channel.basic_consume(queue='notifications', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
