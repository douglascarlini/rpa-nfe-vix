from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import smtplib
import os

class Email:

    cfg = None
    msg = MIMEMultipart()

    def __init__(self, smtp, port, ssl=False):

        if ssl:
            self.cfg = smtplib.SMTP_SSL(smtp, port)
        else:
            self.cfg = smtplib._SSL(smtp, port)

    def login(self, user, pasw, tls=True):

        if tls: self.cfg.starttls()
        self.cfg.login(user, pasw)

    def add_file(self, path):

        file = os.path.basename(path)
        attachment = open(path, 'rb')
        obj = MIMEBase('application','octet-stream')
        obj.set_payload((attachment).read())
        encoders.encode_base64(obj)
        obj.add_header("Content-Disposition", "attachment; filename=" + file)
        self.msg.attach(obj)
        return self

    def send(self, subj, src, dst):

        self.msg['To'] = dst
        self.msg['From'] = src
        self.msg['Subject'] = subj
        msg = self.msg.as_string()
        self.cfg.sendmail(src, dst, msg)
        self.cfg.quit()