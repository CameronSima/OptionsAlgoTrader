import config
import http_requests
import core_functions as cf
import misc_functions as mf
import messaging
import testing

if config.settings['DEBUG'] == True:
	import timing

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

	otm_lasts = cf.get_otm_elements(soup, cols=11, offset=0, result_range=88)
	itm_lasts = cf.get_itm_elements(soup, cols=11, offset=0, result_range1=140,
															 result_range2=230)

	otm_lasts = cf.prices_above_threshold(otm_lasts, config.value['threshold'])
	itm_lasts = cf.prices_above_threshold(itm_lasts, config.value['threshold'])

	otm_theoreticals = cf.get_otm_elements(soup, cols=11, offset=3, result_range=88)
	itm_theoreticals = cf.get_itm_elements(soup, cols=11, offset=3, result_range1=140,
												  					result_range2=230)

	otm_tups = zip(otm_lasts, otm_theoreticals)
	itm_tups = zip(itm_lasts, itm_theoreticals)




	otm_diff = cf.find_percent_difference(otm_tups)
	itm_diff = cf.find_percent_difference(itm_tups)

	"""
	Configuration for threshold of percentage difference between
	theoretical value and actual value.
	"""

	otms_beyond_threshold = cf.beyond_threshold(otm_diff, config.percentage['threshold'])
	itms_beyond_threshold = cf.beyond_threshold(itm_diff, config.percentage['threshold'])

	if config.settings['DEBUG'] == True:
		print 'RESULTS FOUND: '
		print otms_beyond_threshold
		print itms_beyond_threshold
	else:
		pass

	otm_email_body = messaging.get_email_body(otms_beyond_threshold, exp_date)
	itm_email_body = messaging.get_email_body(itms_beyond_threshold, exp_date)

	if otm_email_body:
		if config.settings['DEBUG'] == True:
			testing.output_tester(otm_email_body)
		else:
			r = cf.prevent_dups(otm_email_body)
			if r == True:
				messaging.send_email(otm_email_body)
			else:
				pass
	else:
		pass

	if itm_email_body:
		if config.settings['DEBUG'] == True:
			testing.output_tester(itm_email_body)
		else:
			r = cf.prevent_dups(itm_email_body)
			if r == True:
				messaging.send_email(itm_email_body)
			else:
				pass
	else:
		pass

def main():
	"""
	Run main loop for each week.
	"""

	weeks = cf.get_dates()
	not_a_holiday = cf.market_holidays_2015(weeks)
	for exp_date in not_a_holiday:
		calls = http_requests.get_request(config.settings['URL'], exp_date)
		puts = http_requests.get_puts(config.settings['URL'], exp_date)
		run(exp_date, calls)
		run(exp_date, puts)

if __name__ == '__main__':
	main()


"""

NOTES

Scan 3 strikes away from the moneyline
in either direction.

Give each message/output a unique id number
to avoid sending duplicates

"""

