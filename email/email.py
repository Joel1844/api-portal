from logging import raiseExceptions
from posixpath import split
import smtplib
import ssl
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def mailer_notifications(mail_settings: dict = {

    "receiver": ["receiver@example.com"],
    "subject": "Nuevo caso reportado",
    "text": "Mensaje de el correo"
}):

    msg = EmailMessage()
    msg = MIMEMultipart('alternative')

    html = mail_settings["text"]
    part2 = MIMEText(html, 'html')
    msg.attach(part2)
    context = ssl.create_default_context()

    msg["Subject"] = mail_settings["subject"]
    msg["From"] = mail_settings["mail_sender"]
    msg["To"] = ",".join(mail_settings["receiver"])


    # with smtplib.SMTP("defensordelpueblo.do", port=587) as smtp:
    #     smtp.connect("defensordelpueblo.do", port=587)
    #     smtp.starttls(context=context)
    #     smtp.login("titulares@defensordelpueblo.do", "O[$R(idG;clR")
    #     smtp.send_message(msg)
    #     smtp.quit()

    
    with smtplib.SMTP("mail.smtp2go.com", port=587) as smtp:
        smtp.connect("mail.smtp2go.com", port=587)
        smtp.starttls(context=context)
        smtp.login("dwh", "WU3feHUCoHFiS245")
        smtp.send_message(msg)
        smtp.quit()
