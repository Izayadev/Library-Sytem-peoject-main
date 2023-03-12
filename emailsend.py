from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path
import smtplib
msg = MIMEMultipart()
msg["from"] ="izayadev@gmail.com" #input("From : ")
msg["to"] = "izayadev@gmail.com"
msg["subject"]= "Hoho"

msg.attach(MIMEText("Body"))
msg.attach(Path("/Report about Clients (02 of 03).xlsx").read_bytes)
print(Path("/Report about Clients (02 of 03).xlsx").read_bytes)

with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
	smtp.ehlo()
	smtp.starttls()
	smtp.login("izayadev@gmail.com", "hevszdzqymptjudp")
	smtp.send_message(msg)
	print("Sent...")
