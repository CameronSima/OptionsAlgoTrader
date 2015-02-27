import requests
from bs4 import BeautifulSoup
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