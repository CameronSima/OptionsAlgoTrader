import requests
from bs4 import BeautifulSoup
import numpy

r = requests.get('https://www.optionsxpress.com.au/OXNetTools/Chains/index.aspx?SessionID=&Symbol=SPY&Range=4&lstMarket=0&ChainType=&AdjNonStdOptions=OFF&lstMonths=&FromVB6=True')
soup = BeautifulSoup(r.text)
results = [x for x in soup('td', {'class': 'otm'})]


"""
A list of on the money puts. Doesn't 
take into consideration the money line.
"""

nums = [x for x in range(154) if x%7==0]
otm_puts = [results[x].text for x in nums if x <= len(results)]

"""
Finds the curent strike price, needed
to find the money line.
"""

datarow = soup.find('tr', {'class': 'datarow'})
tds = datarow.findAll('td')
current_price = tds[1].text

"""Finds strike prices."""

strikes_list = [(x.text).rstrip() for x in soup('a', {'class': 'strikes'})]
strikes_list = sorted(set(strikes_list))

up_to_moneyline = [x for x in strikes_list if x <= current_price]

moneyline_tups = zip(up_to_moneyline, otm_puts[:len(up_to_moneyline)])

rev = [x for x in reversed(moneyline_tups)]
last_ten = rev[:10]

float_list = [float(x[1]) for x in last_ten]

st_dev = numpy.std(float_list)

"""
creates a dictionary of 'deviation': (strike, last-price)
key-value pairs.
"""

max_dev_list = (abs(x - y) for (x, y) in zip(float_list[1:], float_list[:-1]))
max_dev_list = [x for x in max_dev_list]
max_dev_dict = dict(zip(max_dev_list[:len(last_ten)], last_ten))

max_dev = max(max_dev_dict)

max_dev_put_tup = [max_dev_dict[x] for x in max_dev_dict if x == max_dev]


# print "MAX DEV DICT " + str(max_dev_dict)

# print 'LAST TEN ' + str(last_ten)

# print "MAX DEVIATION "+ str(max_dev)

print max_dev_put_tup


