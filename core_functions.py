from datetime import date 
from dateutil.relativedelta import relativedelta, calendar

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

def get_strikes(soup):
	"""Returns list of strike prices."""
 	strikes_list = [(x.text).rstrip() for x in soup('a', {'class': 'strikes'})]
 	strikes_list = set(strikes_list)

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

def beyond_threshold(input_dict, threshold):
	"""
	For now, we'll filter % difference between
	theoretical and actual value at 65%
	"""
	return {x:input_dict[x] for x in input_dict if x >= int(threshold) or x <= int(-threshold)}



def prices_above_threshold(prices, threshold):
	"""
	Only return results above a certain price.
	(Contracts worth fractions of a cent often
	have abnormally high percentage differences
	from their theoretical value.) We filter 
	these out because they're basically worthless.
	"""

	return [x for x in prices if float(x) >= threshold]

def prevent_dups(output):
	header, body, link = output
	lines = [line.strip() for line in open(config.notified['filename'])]
	if body.rstrip() not in lines:
		with open(config.notified['filename'], 'at') as f:
			f.write(body)
			print 'New '
			return True
	else:
		print "No new results found"
		return False
