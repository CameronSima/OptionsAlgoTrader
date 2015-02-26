import requests
from bs4 import BeautifulSoup
import numpy
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date 
from dateutil.relativedelta import relativedelta, calendar

import config

if config.settings['DEBUG'] == True:
	import timing

# URL = ('https://www.optionsxpress.com.au/OXNetTools',
# 	  '/Chains/index.aspx?SessionID=&Symbol=SPY&Ran',
# 	  'ge=4&lstMarket=0&ChainType=&AdjNonStdOptions',
# 	  '=OFF&lstMonths=&FromVB6=True')


# def get_request(url):
	# """
	# This may be useful in the future as a simple
	# way to access monthly contracts.
	# """
# 	r = requests.get(URL)
# 	soup = BeautifulSoup(r.text)
# 	return soup

def get_dates():
	"""
	lstMonths parameter is in the form of 
	'12/2/15;0', 0 indicating a monthly contract,
	and 1 indicating a monthly (3rd weekly contract)
	"""

	"""week1 = this friday"""
	week1 = date.today() + relativedelta(weekday=calendar.FRIDAY)
	week2 = week1 + relativedelta(weeks=+1)
	week3 = week1 + relativedelta(weeks=+2)
	week4 = week1 + relativedelta(weeks=+4)
	week5 = week1 + relativedelta(weeks=+5)
	week6 = week1 + relativedelta(weeks=+3)

	return ((str(week1) + ';' + '0'), 
		   (str(week2) + ';' + '0'),
		   (str(week3) + ';' + '0'),
		   (str(week4) + ';' + '0'),
		   (str(week5) + ';' + '0'),
		   (str(week6) + ';' + '1'))

def get_request(url, exp_date):
	data = {
	    '__VIEWSTATE': ('dDwtMjgzNDc5MzI0OztsPGN'
	                   'oa0Fkak5vblN0ZE9wdGlvbn'
	                   'M7Y2hQcmljZXJFbmFibGVEa'
	                   'XZpZGVuZHM7cmFkaW9Qcmlj'
	                   'ZXJDYWxsUHV0QztyYWRpb1B'
	                   'yaWNlckNhbGxQdXRQO2Noa1'
	                   'JvbGxPdmVyczs+Pi6ZHd/3Y'
	                   'fvEgTRO5zXzTzEOqOTU'),

	    '__VIEWSTATEGENERATOR': 'B2404176',

	    'hidDisableSiteStats': '0',
	    'txtTestDriveH':'false',
	    'txtSymbol':'SPY',
	    'hdnSymPassBack':'false',
	    'hdnSymEnabled':'true',
	    'hdnPushpinEnabled':'1',
	    'hdnAccount':'0',
	    'hdnIsT3':'0',
	    'lstMarket':'0',
	    'lstRange':'4',
	    'lstChainType':'3',
	    'lstMonths': exp_date,
	    'txtPricerVol':'12.24',
	    'txtPricerStockPrice':'211.21',
	    'txtPricerTimeToMaturity':'11',
	    'txtPricerInterest':'1.00',
	    'txtPricerDividendDate':'12/19/2014',
	    'txtPricerDividend':'1.13',
	    'lstPricerDivFreq':'91',
	    'radioPricerCallPut':'Calls',
	    'hidChainsExist':'Exists',
	    'hidIsDetached':'0',
	    'txtStrike':'0',
	    'txtDisableRowOvers':'Enable',
	    'txtDisplayXSpreads':'0',
	    'txtPricerCheckCalls':'1',
	    'txtLoadedSymbol':'SPY',
	    'txtLoadedRange':'4',
	    'txtLoadedChainType':'3',
	    'txtLoadedExpiration':'3/20/2015;0',
	    'txtUnderlyingQt':('SPY|211.209|211.14'
	                      '|211.16|0|5|TRUE|21'
	                      '1.21|210.48|7415270'
	                      '3|-0.03000000000000'
	                      '11|2/23/2015 5:02:22'
	                      ' PM|211.209|211.14|21'
	                      '1.16|211.21|210.48|-0.03'),

	    'txtStreamDelay':'1000',
	    'txtStreamOptionQuotes':'1',
	    'txtSortDir':'0',
	    'txtSessionID':'C73763A1C9E747CDBDB18D0276D6B780',
	    'txtIsMini':'0',

	}

	response = requests.post(url, data=data)
	soup = BeautifulSoup(response.text)
	return soup

url = ('https://www.optionsxpress.com.au/'
		   'OXNetTools/Chains/index.aspx?Chai'
		   'nType=3&SessionID=C73763A1C9E747C'
		   'DBDB18D0276D6B780')

def get_puts(url, exp_date):

	"""
	All the code so far determines data for 
	calls only. This submits the request
	to obtain puts information.
	"""
	args = {
		'symbol': "SPY", 
		'range': "4", 
		'exp': "3/20/2015;1", 
		'currentimpvol': "12.25", 
		'stockpricedisplay': "211.81"
		}

	data = {
		'args': args,
		'callput': "P",
		'currentimpvol': "12.25",
		'daystillexp': "37",
		'exp': exp_date,
		'includediv': "false",
		'interestrate': "1.00",
		'isdetached': "0",
		'lstPricerDivFreq': "91",
		range: "4",
		'sessionid': "C73763A1C9E747CDBDB18D0276D6B780",
		'stockpricedisplay': "211.81",
		'symbol': "SPY",
		'txtPricerDividend': "1.13",
		'txtPricerDividendDate': "12/19/2014"
	}

	response = requests.post(url, data=data)
	soup = BeautifulSoup(response.text)
	return soup

def get_otm_elements(soup, cols, offset, result_range):
	"""
	A list of out of the money elements. Specific element
	is chosen with offset number, and result-size
	is chosen with result_range.
	"""
	results = [x for x in soup('td', {'class': 'otm'})]
	# print "results"
	# print results
	nums = [x for x in range(result_range) if x%cols==offset]
	return [results[x].text for x in nums if x <= len(results)]


def get_itm_elements(soup, cols, offset, result_range1, result_range2):
	"""
	A list of in the money elements. Specific element
	is chosen with offset number, and result-size
	is chosen with result_range.
	"""
	results = [x for x in soup('td', {'class': 'itm'})]
	nums = [x for x in range(result_range1, result_range2) if x%cols==offset]
	itm_puts = [results[x].text for x in nums if x <= len(results)]
	return [x for x in reversed(itm_puts)]


def get_current_strike_price(soup):
	"""
	Finds the curent strike price, needed
	to find the money line.
	"""
	datarow = soup.find('tr', {'class': 'datarow'})
	tds = datarow.findAll('td')
	current_price = tds[1].text
	return current_price

def get_strikes_list(soup):
	"""Finds strike prices."""
	strikes_list = [(x.text).rstrip() for x in soup('a', {'class': 'strikes'})]
	strikes_list = sorted(set(strikes_list))
	return strikes_list

def get_last_ten(strikes_list, current_price, otm_puts):
	up_to_moneyline = [x for x in strikes_list if x <= current_price]
	moneyline_tups = zip(up_to_moneyline, otm_puts[:len(up_to_moneyline)])
	rev = [x for x in reversed(moneyline_tups)]
	last_ten = rev[:10]
	return last_ten

def get_float_list(last_ten):
	float_list = [float(x[1]) for x in last_ten]
	return float_list

def get_standard_deviation(float_list):
	st_dev = numpy.std(float_list)
	return st_dev

def get_last_ten_dict(float_list, last_ten):
	"""
	creates a dictionary of 'deviation': (strike, last-price)
	key-value pairs.
	"""
	max_dev_list = (abs(x - y) for (x, y) in zip(float_list[1:], float_list[:-1]))
	max_dev_list = [x for x in max_dev_list]
	max_dev_dict = dict(zip(max_dev_list[:len(last_ten)], last_ten))
	return max_dev_dict

def get_max_deviation(max_dev_dict):
	max_dev = max(max_dev_dict)
	return max_dev

def get_result_tup(max_dev_dict, max_dev):
	"""
	returns tuple containing 
	{max-deviation: (strike-price, last-price)}
	"""
	max_dev_put_tup = dict([(x, max_dev_dict[x]) for x in max_dev_dict if x == max_dev])
	return max_dev_put_tup

def extract(max_dev_put_tup):
	x = max_dev_put_tup.keys()
	y = max_dev_put_tup.values()
	y = str(y)
	y = y.split("'")
	result = y[1], y[3], x
	return result

def find_percent_difference(tup_list):
	perc_dict = {}
	for x in tup_list:
		difference = float(x[0]) - float(x[1])
		try:
			percent_difference = difference / float(x[1]) * 100
		except ZeroDivisionError:
			percent_difference = 0
		
		perc_dict[percent_difference] = x
	return perc_dict

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

def print_outputs(args, **kwargs):
	print "MAX DEV DICT " + str(max_dev_dict)
	print 'LAST TEN ' + str(last_ten)
	print "MAX DEVIATION "+ str(max_dev)
	print 'RESULT TUPS: ' + str(max_dev_put_tup)

def beyond_threshold(input_dict, threshold):
	"""
	For now, we'll filter % difference between
	theoretical and actual value at 65%
	"""
	return {x:input_dict[x] for x in input_dict if x >= int(threshold) or x <= int(-threshold)}

def market_holidays_2015(weeks):
	"""
	Option contracts typically expire every 
	Friday, except on Holidays, when they
	may expire Thursday or on another
	specified day.
	"""

	holidays = ['2015-01-01', '2015-19-01', '2015-02-16',
				'2015-04-03', '2015-05-25', '2015-07-03',
				'2015-07-04', '2015-09-07', '2015-11-26',
				'2015-12-25', '2016-12-01']

	return [x for x in weeks if x[:-2] not in holidays]

def prices_above_threshold(prices, threshold):
	"""
	Only return results above a certain price.
	(Contracts worth fractions of a cent often
	have abnormally high percentage differences
	from their theoretical value.) We filter 
	these out because they're basically worthless.
	"""

	return [x for x in prices if float(x) >= threshold]


# def notify_max_deviation_put():
# 	"""
# 	Output of version one of
# 	the program. Finds maximally
# 	deviated put from closet ten
# 	to the money line, with last 
# 	price, strike price, and 
# 	difference from its neighbor.
# 	"""

# 	soup = get_request(URL)
# 	otm_puts = get_otm_elements(soup, cols=7, offset=0, result_range=154)
# 	current_price = get_current_strike_price(soup)
# 	strikes_list = get_strikes_list(soup)
# 	last_ten = get_last_ten(strikes_list, current_price, otm_puts)
# 	float_list = get_float_list(last_ten)
# 	st_dev = get_standard_deviation(float_list)
# 	max_dev_dict = get_last_ten_dict(float_list, last_ten)
# 	max_dev = get_max_deviation(max_dev_dict)
# 	max_dev_put_tup = get_result_tup(max_dev_dict, max_dev)
# 	result = extract(max_dev_put_tup)

# 	email_body = ("**TESTING** \n\n"
# 			   "Maximum deviation is at STRIKE price {0}. "
# 			   "The LAST price is {1}, and has a difference of "
# 			   "{2} from the previous price.").format(result_tup[0],
# 													  result_tup[1],
# 												  str(result_tup[2])[1:-1])
	
# 	if config.settings['DEBUG'] == True:
# 		output_tester(result, email_body)
# 	else:
# 		send_email(result, email_body)

def run(exp_date, soup):

	"""
	Main loop.

	We want 8 results from the money line,
	so since last prices are every 11th element
	in the HTML <td class='otm'>, we take 88
	such elements (8x11=88)

	Offset refers to the element's location
	in the chart (1st column == offset=0)
	"""

	otm_lasts = get_otm_elements(soup, cols=11, offset=0, result_range=88)
	itm_lasts = get_itm_elements(soup, cols=11, offset=0, result_range1=140,
														  result_range2=230)

	otm_lasts = prices_above_threshold(otm_lasts, config.value['threshold'])
	itm_lasts = prices_above_threshold(itm_lasts, config.value['threshold'])

	otm_theoreticals = get_otm_elements(soup, cols=11, offset=3, result_range=88)
	itm_theoreticals = get_itm_elements(soup, cols=11, offset=3, result_range1=140,
												  				 result_range2=230)

	otm_tups = zip(otm_lasts, otm_theoreticals)
	itm_tups = zip(itm_lasts, itm_theoreticals)



	otm_diff = find_percent_difference(otm_tups)
	itm_diff = find_percent_difference(itm_tups)

	"""
	Configuration for threshold of percentage differene between
	theoretical value and actual value.
	"""

	otms_beyond_threshold = beyond_threshold(otm_diff, config.percentage['threshold'])
	itms_beyond_threshold = beyond_threshold(itm_diff, config.percentage['threshold'])

	if config.settings['DEBUG'] == True:
		print 'RESULTS FOUND: '
		print otms_beyond_threshold
		print itms_beyond_threshold
	else:
		pass

	otm_email_body = get_email_body(otms_beyond_threshold, exp_date)
	itm_email_body = get_email_body(itms_beyond_threshold, exp_date)

	if otm_email_body:
		if config.settings['DEBUG'] == True:
			output_tester(otm_email_body)
		else:
			r = prevent_dups(otm_email_body)
			if r == True:
				send_email(otm_email_body)
			else:
				pass
	else:
		pass

	if itm_email_body:
		if config.settings['DEBUG'] == True:
			output_tester(itm_email_body)
		else:
			r = prevent_dups(itm_email_body)
			if r == True:
				send_email(itm_email_body)
			else:
				pass
	else:
		pass

def main():
	"""
	Run main loop for each week.
	"""

	weeks = get_dates()
	not_a_holiday = market_holidays_2015(weeks)
	for exp_date in not_a_holiday:
		calls = get_request(config.settings['URL'], exp_date)
		puts = get_puts(config.settings['URL'], exp_date)
		run(exp_date, calls)
		run(exp_date, puts)

def output_tester(output):
	print "PRINTED"
	print output


def prevent_dups(output):
	header, body, link = output
	lines = [line.strip() for line in open(config.notified['filename'])]
	if body.rstrip() not in lines:
		with open(config.notified['filename'], 'at') as f:
			f.write(body)
			return True
	else:
		print 'in lines'
		return False






if __name__ == '__main__':
	main()


"""

NOTES

Scan 3 strikes away from the moneyline
in either direction.

Give each message/output a unique id number
to avoid sending duplicates

"""

