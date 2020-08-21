import smtplib # lan of the email
from email.message import EmailMessage
from string import Template
from pathlib import Path

def send_email_to(email_receiver, content):
	email = EmailMessage()
	email['from'] = 'Daniel Benet'
	email['to'] = email_receiver
	email['subject'] = 'Top 5 hacker news (automation programm)'

	email.set_content(content)

	with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
	    smtp.ehlo()
	    smtp.starttls()
	    smtp.login('ladyworst0@gmail.com', 'pertutti1')
	    smtp.send_message(email)
	    print('All good boss!')