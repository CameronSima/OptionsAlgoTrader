# import numpy

# def get_current_strike_price(soup):
# 	"""
# 	Finds the curent strike price, needed
# 	to find the money line.
# 	"""
# 	datarow = soup.find('tr', {'class': 'datarow'})
# 	tds = datarow.findAll('td')
# 	current_price = tds[1].text
# 	return current_price

# def get_strikes_list(soup):
# 	"""Finds strike prices."""
# 	strikes_list = [(x.text).rstrip() for x in soup('a', {'class': 'strikes'})]
# 	strikes_list = sorted(set(strikes_list))
# 	return strikes_list

# def get_last_ten(strikes_list, current_price, otm_puts):
# 	up_to_moneyline = [x for x in strikes_list if x <= current_price]
# 	moneyline_tups = zip(up_to_moneyline, otm_puts[:len(up_to_moneyline)])
# 	rev = [x for x in reversed(moneyline_tups)]
# 	last_ten = rev[:10]
# 	print last_ten
# 	return last_ten

# def get_float_list(last_ten):
# 	float_list = [float(x[1]) for x in last_ten]
# 	return float_list

# def get_standard_deviation(float_list):
# 	st_dev = numpy.std(float_list)
# 	return st_dev

# def get_last_ten_dict(float_list, last_ten):
# 	"""
# 	creates a dictionary of 'deviation': (strike, last-price)
# 	key-value pairs.
# 	"""
# 	max_dev_list = (abs(x - y) for (x, y) in zip(float_list[1:], float_list[:-1]))
# 	max_dev_list = [x for x in max_dev_list]
# 	max_dev_dict = dict(zip(max_dev_list[:len(last_ten)], last_ten))
# 	return max_dev_dict

# def get_max_deviation(max_dev_dict):
# 	max_dev = max(max_dev_dict)
# 	return max_dev

# def get_result_tup(max_dev_dict, max_dev):
# 	"""
# 	returns tuple containing 
# 	{max-deviation: (strike-price, last-price)}
# 	"""
# 	max_dev_put_tup = dict([(x, max_dev_dict[x]) for x in max_dev_dict if x == max_dev])
# 	return max_dev_put_tup

# def extract(max_dev_put_tup):
# 	x = max_dev_put_tup.keys()
# 	y = max_dev_put_tup.values()
# 	y = str(y)
# 	y = y.split("'")
# 	result = y[1], y[3], x
# 	return result

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