import smtplib
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

msg = MIMEMultipart()

msg["from"] = input("From : ")
msg["to"] = input("Enter Email : ")
msg["subject"]= input("Subject : ")
msg.attach(MIMEText("Body"))

file = "aqua_profile.jpg"
with open(file, 'r') as f:
    atach = MIMEApplication(f.read(), Name=basename(file))
    atach['Content-Disposition'] = 'attachment; file="{}"'.format(basename(file))

msg.attach(atach)
from pathlib import Path

msg.attach(MIMEApplication(Path('aqua_profile.jpg').read_bytes))

with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
	smtp.ehlo()
	smtp.starttls()
	smtp.login("izayadev@gmail.com", "hevszdzqymptjudp")
	smtp.send_message(msg)
	print("Sent...")
	

