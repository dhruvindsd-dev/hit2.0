import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# Email 
# login 
# server_quit
# send mail
# environment variables

class Email:
    def __init__(self):
        self.username = 'highlyinformativetext@gmail.com'
        self.password = 'Uchiha$877'
        self.server = None

    def login(self):
        self.server = smtplib.SMTP(host='smtp.gmail.com', port=587)
        self.server.ehlo()
        self.server.starttls() # ttls encryption 
        self.server.login(self.username, self.password)

    def send_mail(self,text,subject,from_email='HIT_2.0 <highlyinformativetext@gmail.com>',to_emails=None):# sends an email to the emails in the to_email_list..
        assert isinstance(to_emails, list)
        msg = MIMEMultipart('alternative')
        msg['From'] = from_email
        msg['To'] = ", ".join(to_emails)
        msg['Subject'] = subject
        txt_part = MIMEText(text, 'plain')
        msg.attach(txt_part)
        msg_str = msg.as_string()
        self.server.sendmail(from_email, to_emails, msg_str)

    def quit_server(self):
        self.server.quit()

    

