import requests
from bs4 import BeautifulSoup
import smtplib
import itertools
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config
import core_functions as cf
import http_requests
import timing

URL = ('https://www.optionsxpress.com.au/'
	   'OXNetTools/Chains/index.aspx?Chai'
	   'nType=3&SessionID=C73763A1C9E747C'
	   'DBDB18D0276D6B780')

def get_email_text(row_tup):
	if row_tup != None:
		if row_tup[8] > 0:
			h_or_l = 'higher'
		else:
			h_or_l = 'lower'

		body = ("Option is {0}% {1} than theoretical price.\n"
				"It is an {2} {3}.\n\n"
				"Strike Price: {4}\nLast Price: {5}\n"
				"Bid Price: {6}\nAsk Price: {7}\n"
				"Theoretical Value: {8}\n\nEXPIRES: {9}").format(str(abs(int(row_tup[8]))), h_or_l,
																   row_tup[5], row_tup[6], 
																   row_tup[0], row_tup[1],
																   row_tup[2], row_tup[3],
																   row_tup[4], str(row_tup[7])[:10])

	return body





def send_email(email_body):

	header = ("$ $ THIS IS AN ALERT FROM ALGOBOT IN"
		  "REFERENCE TO THE FOLLOWING SPY OPTION:")

	link = "{0}".format(URL)
	
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


class Results():
	def __init__(self, soup):
		self.soup = soup
		self.results = self.soup('tr', {'onmouseout': 'KillTimer();'})

	def itm(self, dist_from_moneyline):
		self.results = reversed(self.results)
		self.itms = [(x, 'itm') for x in self.results if x.find(class_='itm')]
		return self.itms[:dist_from_moneyline]

	def otm(self, dist_from_moneyline):
		self.otms = [(x, 'otm') for x in self.results if x.find(class_='otm')]
		return self.otms[:dist_from_moneyline]

	def itm_puts(self, dist_from_moneyline):
		self.itms = [(x, 'itm') for x in self.results if x.find(class_='itm')]
		return self.itms[:dist_from_moneyline]

	def otm_puts(self, dist_from_moneyline):
		self.results = reversed(self.results)
		self.otms = [(x, 'otm') for x in self.results if x.find(class_='otm')]
		return self.otms[:dist_from_moneyline]


def get_element(row, element_no):
	element = row.text.splitlines()[element_no]
	return float(element)


def get_tup(row):
	
	strike = get_element(row[0], 1)
	last = get_element(row[0], 2)
	bid = get_element(row[0], 3)
	ask = get_element(row[0], 4)
	theo = get_element(row[0], 5)
	call_or_put = row[1]

	return strike, last, bid, ask, theo, call_or_put

def get_above_threshold(tup, threshold):
	if tup[1] >= threshold:
		return tup
	else:
		pass

def find_percent_difference(tup):
	difference = float(tup[1]) - float(tup[4])
	try:
		percent_difference = difference / tup[4] * 100
	except ZeroDivisionError:
		percent_difference = 0
	return percent_difference


# def calls(exp_date):
# 	soup = http_requests.get_calls(URL, exp_date)
# 	result = Results(soup)
# 	loop(soup, result.otm_calls(3), 'call', exp_date)
# 	loop(soup, result.itm_calls(3), 'call', exp_date)

# def puts(exp_date):
# 	soup = http_requests.get_puts(URL, exp_date)
# 	result = Results(soup)
# 	loop(soup, result.otm_puts(3), 'put', exp_date)
# 	loop(soup, result.itm_puts(3), 'put', exp_date)

# def main():
# 	exp_dates = cf.get_dates()
# 	not_holiday = cf.market_holidays_2015(exp_dates)
# 	for exp_date in not_holiday:

# 		# calls(exp_date)
# 		puts(exp_date)

def prevent_dups(tup):
	results = str(tup[0]), tup[5], tup[6]
	results = str(results)
	with open('results1.txt', 'a+') as f:
		if not any(results == x.rstrip('\r\n') for x in f):
			f.write(results + '\n')
			return tup
		else:
			pass

def loop(soup, call_or_put, exp_date):
	email_body = ''
	if call_or_put == 'call':
		otms = Results(soup).otm(3)
		itms = Results(soup).itm(3)
	else:
		otms = Results(soup).otm_puts(3)
		itms = Results(soup).itm_puts(3)

	for x in itertools.chain(itms, otms):
		tup = get_tup(x)
		above_price_threshold = get_above_threshold(tup, .1)
		diff = find_percent_difference(tup)
		if not diff >= 50 or diff <= -50 and above_price_threshold:
			pass
		else:
			tup += (call_or_put, exp_date, diff)
			prevent_dups(tup)
			email_body += ('\n' + get_email_text(tup))
		
	if email_body:
		print "++++++++++BEGIN+++++++++"
		print email_body
	else:
		pass

def weeks(request, call_or_put):
	loop(http_requests.get_monthly(request), call_or_put, 'monthly')
	loop(http_requests.get_week_1(request), call_or_put, 'week 1')
	loop(http_requests.get_week_2(request), call_or_put, 'week 2')
	loop(http_requests.get_week_3(request), call_or_put, 'week 3')
	loop(http_requests.get_week_4(request), call_or_put, 'week 4')
	loop(http_requests.get_week_5(request), call_or_put, 'week 5')

def main():
	request = http_requests.Request(URL)
	"""Get calls"""
	weeks(request, 'call')
	"""Get puts"""
	request.get_put()
	weeks(request, 'put')
	request.driver.close()

main()