from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.message import EmailMessage
import base64
from dotenv import load_dotenv, dotenv_values
from datetime import datetime
import os
import mimetypes

def send_email(filePath):
    FULL_PATH_TO_PROJECT = "your_path"
    try:
        date_time = datetime.now()
        load_dotenv(dotenv_path=FULL_PATH_TO_PROJECT+"/.env")


        EMAIL = os.getenv("EMAIL")
        # Load saved credentials
        creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/gmail.send'])

        service = build('gmail', 'v1', credentials=creds)

        # Compose message
        message = EmailMessage()
        message['to'] = EMAIL
        message['from'] = EMAIL
        message['subject'] = 'Daily Crypto Report'
        message.set_content(
            "Hello!\n"
            "Your daily crypto report is ready!\n"
            "Check the attached file for more details\n\n"
            "Kind regards\n"
            "VZ's CryptoBot 🫰"
            )

        mime_type,_ = mimetypes.guess_type(filePath)
        mime_main, mime_sub = mime_type.split("/")

        with open(filePath, "rb") as f:
            file_data = f.read()
            file_name = f.name.split("/")[-1]

        message.add_attachment(file_data,maintype=mime_main, subtype=mime_sub,filename=file_name)

        # Encode and send
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        body = {'raw': raw}

        service.users().messages().send(userId='me', body=body).execute()
    except Exception as e:
        # Log any potential errors into errors.log
        with open(FULL_PATH_TO_PROJECT+"/errors.log","a")as f:
            f.write(f"[{date_time.strftime('%d.%m.%Y %H:%M:%S')}] smtp.py error: {e}")
