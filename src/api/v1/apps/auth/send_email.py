from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from db import mail

def send_mail(email, json_data):
    serializer = URLSafeTimedSerializer('kjfjk1kj2kjkj32jkjksj2j1kjk1jwewkjfjsfkjbk2jkjkj')
    activation_token = serializer.dumps(email, salt='activate')
    activation_link = f'http://127.0.0.1:5000/activate/{activation_token}'
    msg = Message(
        'Account Verification',
        sender='er.voramihir@gmail.com',
        recipients=['er.voramihir@gmail.com']
    )
    msg.body = f'Hello {json_data.get("first_name")}, please click the link for verification {activation_link}'
    mail.send(msg)