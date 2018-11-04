from email.mime.text import MIMEText

import smtplib
import yaml
import os

yaml_config_file_path = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), 'maxigbot.yml')

bot_config = yaml.load(open(yaml_config_file_path))

if len(bot_config) > 0:
    print(">> Configuration file loaded.\n")

mail_config = bot_config['maxigbot']['send-mail']

smtp_ssl_host = mail_config['smtp_ssl_host']
smtp_ssl_port = mail_config['smtp_ssl_port']
username = mail_config['username']
password = mail_config['password']
sender = mail_config['sender']
targets = mail_config['target-address']

msg = MIMEText('Hello World....123')
msg['Subject'] = 'Hello World 123 from Earth!'
msg['From'] = sender
msg['To'] = ', '.join(targets)

server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
server.login(username, password)
server.sendmail(sender, targets, msg.as_string())
server.quit()
print("Done!")
