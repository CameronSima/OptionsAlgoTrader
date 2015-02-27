import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config

def get_email_body(inputs, exp_date):
	if inputs != None:

		for x, y in inputs.iteritems():
			if x > 0:
				h_or_l = 'higher'
			else:
				h_or_l = 'lower'

			perc = [i for i in str(x) if i.isdigit()]
			perc_string = ''
			for x in perc[:2]:
				perc_string += x

			header = ("$ $ $ $ $ $ $ $ $ $ $ $ \n**TESTING**\n"
					  "$ $ $ $ $ $ $ $ $ $ $ $ \n\n")

			body = ("Option expiring on {4} with price {0} "
					"and theoretical price {1} is {2}% {3} "
					"than theoretical value.\n\n").format(str(y[0]),
													   str(y[1]),
													   perc_string,
													   h_or_l,
													   exp_date[:-2])

			link = "{0}".format(config.settings['URL'])

			return header, body, link


def send_email(email_body):
	header, body, link = email_body
	ADDRESS = config.sender['ADDRESS']
	s = smtplib.SMTP('smtp.gmail.com',587)
	s.starttls()
	s.ehlo
	try:
		s.login(config.sender['ADDRESS'], config.sender['PASSWORD'])
	except:
		print "SMTP AUTHENTICATION ERROR"
	msg = MIMEMultipart()

	if config.settings['TEXT_MESSAGING'] == True:
		"""
		send only the important stuff to
		keep the text msg short.
		"""
		msg.attach(MIMEText(body))
		s.sendmail(config.sender['ADDRESS'], 
				   config.receiver['PHONE_NUMBER'] + 
				   config.receiver['GATEWAY'], msg.as_string())

	else:
		msg['Subject'] = '**$$$_SPY OPTIONS ALERT_$$$**'
		msg.attach(MIMEText(header + body + link))
		s.sendmail(config.sender['ADDRESS'], 
				   config.receiver['ADDRESS'], msg.as_string())

	s.close()