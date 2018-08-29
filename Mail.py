from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class MailSender(object):

    """
    Create a e-mail sender using the SMTPlib

    Attributes:
        attachment (STRING): Path of the file to be attached
        body (STRING): The Email body/message
        From (STRING): Sender's email
        senderPassword (STRING): Sender's email password
        smtpServer (STRING): SMTP Server (smtp.server.com:port)
        subject (STRING): The subject of the email
        To (STRING): recipient of the email
    """

    def __init__(self, From, senderPassword, To,
                 smtpServer, attachment, subject, body):
        self.From = From
        self.senderPassword = senderPassword
        self.To = To
        self.smtpServer = smtpServer
        self.attachment = attachment
        self.subject = subject
        self.body = body

    def send_email(self):
        msg = MIMEMultipart()
        msg['To'] = self.To
        msg['From'] = self.From
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.body, 'plain'))

        with open(self.attachment, 'rb') as file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((file).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            "attachment; filename= %s" % file.name)
            msg.attach(part)

        with SMTP(self.smtpServer) as server:
            server.starttls()
            server.login(self.From, self.senderPassword)
            server.sendmail(self.From, self.To, msg.as_string())
            server.quit()
        return
