import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MailSender:
    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        sender_email: str,
        smtp_username: str,
        smtp_password: str,
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email: str = sender_email
        self.smtp_username: str = smtp_username
        self.smtp_password: str = smtp_password

    def connect(self):
        if hasattr(self, "server") and self.server.helo()[0] == 250:
            return

        self.server = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10)
        self.server.starttls()
        self.server.login(self.smtp_username, self.smtp_password)

    def send_email(
        self,
        receiver_email: str,
        subject: str,
        text_body: str,
        html_body: str = None,
    ):
        msg = MIMEMultipart("alternative")
        msg["From"] = self.sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject

        msg.attach(MIMEText(text_body, "plain"))
        if html_body:
            msg.attach(MIMEText(html_body, "html"))
        text = msg.as_string()

        self.connect()
        self.server.sendmail(self.sender_email, receiver_email, text)
