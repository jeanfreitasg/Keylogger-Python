from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MailSender(object):
    """Create a e-mail sender using the SMTPlib"""

    def __init__(self, sender, senderPassword, receiver,
                 smtpServer, attachment, subject, body):
        self.sender = sender
        self.senderPassword = senderPassword
        self.receiver = receiver
        self.smtpServer = smtpServer
        self.attachment = attachment
        self.subject = subject
        self.body = body

    def send_email():
        msg = MIMEMultipart()
        msg['To'] = self.receiver
        msg['From'] = self.sender
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.body))

        with open(self.attachment, 'rb') as file:
            msg.attach(MIMEText(file.read))

        with SMTP(self.smtpServer) as server:
            server.starttls()
            server.login(self.sender, self.password)
            server.sendmail(self.sender, self.receiver, msg.as_string())
            server.quit()
