import pandas as pd
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()  # Load from .env

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_WHATSAPP_NUMBER = os.getenv("FROM_WHATSAPP_NUMBER")
TO_WHATSAPP_NUMBER = os.getenv("TO_WHATSAPP_NUMBER")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

df = pd.read_csv("std.csv")

message_body = "📚 *Assessment Marks Summary:*\n\n"
for _, row in df.iterrows():
    message_body += f"*{row['Subject']}* - {row['Assessment']}: {row['Obtained Marks']}\n"

message = client.messages.create(
    body=message_body,
    from_=FROM_WHATSAPP_NUMBER,
    to=TO_WHATSAPP_NUMBER
)
print("Message sent")
