from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class VerificationEmail:
    def __init__(self, sender, receiver, url, name):
        self.message = ""
        self.generate_verification_email(sender, receiver, url, name)

    def generate_verification_email(self, sender_email, receiver_email, base_url, name):
        self.message = MIMEMultipart("alternative")
        self.message["Subject"] = "multipart test"
        self.message["From"] = sender_email
        self.message["To"] = receiver_email

        text = """\
        Hi {},
        This is your verification email after registration
        www.boombayan.com""".format(name)
        html = """\
        <html>
          <body>
            <p>Hi {},<br>
               Thank you for registering to Boombayan<br>
               <a href="{}">Click Here to Verify your account</a> 
            </p>
          </body>
        </html>
        """.format(name, base_url)
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        self.message.attach(part1)
        self.message.attach(part2)
