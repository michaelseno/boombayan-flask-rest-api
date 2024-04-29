import smtplib
from email_templates.verification_email import VerificationEmail

SMTP_SERVER = "smtp.gmail.com"
SENDER = "adboombayan@gmail.com"
PASSWORD = "tegnrjhijqjkinmt"


class Email:
    def __init__(self):
        self.connection = smtplib.SMTP_SSL(SMTP_SERVER)
        self.login()

    def login(self):
        self.connection.login(user=SENDER, password=PASSWORD)

    def send(self, recipients, name, url):
        template = VerificationEmail(sender=SENDER, receiver=recipients, url=url, name=name)
        self.connection.sendmail(
            from_addr=SENDER,
            to_addrs=recipients,
            msg=template.message.as_string()
        )
