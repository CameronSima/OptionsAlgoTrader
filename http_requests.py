import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Request():
	def __init__(self, url):
		self.driver = webdriver.Firefox()
		self.driver.get(url)

	def get_put(self):
		self.element = self.driver.find_element_by_id('radioPricerCallPutP')
		self.element.click()
		self.html = self.driver.page_source
		self.soup = BeautifulSoup(self.html)

		self.wait = WebDriverWait(self.driver, 10)
		self.element = self.wait.until(EC.element_to_be_clickable((By.ID, 'radioPricerCallPutC')))

		return self.soup

	def get_soup(self):
		self.html = self.driver.page_source
		self.soup = BeautifulSoup(self.html)
		return self.soup


	def get_week(self, element_num):
		self.xpath = ("/html/body/form/"
						"table/tbody/tr/td"
						"/div/span[3]/div["
						"1]/div/div/div[2]"
						"/div/table/tbody/"
						"tr/td/div/span[2]"
						"/a[%s]") % str(element_num)
	

		self.week_link = self.driver.find_element(By.XPATH, self.xpath)
		self.week_link.click()
		self.wait = WebDriverWait(self.driver, 10)
		self.element = self.wait.until(EC.element_to_be_clickable((By.ID, 'radioPricerCallPutC')))



def get_week_1(request):
	request.get_week(1)
	return request.get_soup()

def get_week_2(request):
	request.get_week(1)
	return request.get_soup()

def get_week_3(request):
	request.get_week(2)
	return request.get_soup()

def get_week_4(request):
	request.get_week(3)
	return request.get_soup()

def get_week_5(request):
	request.get_week(4)
	return request.get_soup()

def get_monthly(request):
	return request.get_soup()


# def get_calls(url, exp_date):
# 	data = {
# 	    '__VIEWSTATE': ('dDwtMjgzNDc5MzI0OztsPGN'
# 	                   'oa0Fkak5vblN0ZE9wdGlvbn'
# 	                   'M7Y2hQcmljZXJFbmFibGVEa'
# 	                   'XZpZGVuZHM7cmFkaW9Qcmlj'
# 	                   'ZXJDYWxsUHV0QztyYWRpb1B'
# 	                   'yaWNlckNhbGxQdXRQO2Noa1'
# 	                   'JvbGxPdmVyczs+Pi6ZHd/3Y'
# 	                   'fvEgTRO5zXzTzEOqOTU'),

# 	    '__VIEWSTATEGENERATOR': 'B2404176',

# 	    'hidDisableSiteStats': '0',
# 	    'txtTestDriveH':'false',
# 	    'txtSymbol':'SPY',
# 	    'hdnSymPassBack':'false',
# 	    'hdnSymEnabled':'true',
# 	    'hdnPushpinEnabled':'1',
# 	    'hdnAccount':'0',
# 	    'hdnIsT3':'0',
# 	    'lstMarket':'0',
# 	    'lstRange':'4',
# 	    'lstChainType':'3',
# 	    'lstMonths': exp_date,
# 	    'txtPricerVol':'12.24',
# 	    'txtPricerStockPrice':'211.21',
# 	    'txtPricerTimeToMaturity':'11',
# 	    'txtPricerInterest':'1.00',
# 	    'txtPricerDividendDate':'12/19/2014',
# 	    'txtPricerDividend':'1.13',
# 	    'lstPricerDivFreq':'91',
# 	    'radioPricerCallPut':'Calls',
# 	    'hidChainsExist':'Exists',
# 	    'hidIsDetached':'0',
# 	    'txtStrike':'0',
# 	    'txtDisableRowOvers':'Enable',
# 	    'txtDisplayXSpreads':'0',
# 	    'txtPricerCheckCalls':'1',
# 	    'txtLoadedSymbol':'SPY',
# 	    'txtLoadedRange':'4',
# 	    'txtLoadedChainType':'3',
# 	    'txtLoadedExpiration':'3/20/2015;0',
# 	    'txtUnderlyingQt':('SPY|211.209|211.14'
# 	                      '|211.16|0|5|TRUE|21'
# 	                      '1.21|210.48|7415270'
# 	                      '3|-0.03000000000000'
# 	                      '11|2/23/2015 5:02:22'
# 	                      ' PM|211.209|211.14|21'
# 	                      '1.16|211.21|210.48|-0.03'),

# 	    'txtStreamDelay':'1000',
# 	    'txtStreamOptionQuotes':'1',
# 	    'txtSortDir':'0',
# 	    'txtSessionID':'C73763A1C9E747CDBDB18D0276D6B780',
# 	    'txtIsMini':'0',

# 	}

# 	response = requests.post(url, data=data)
# 	soup = BeautifulSoup(response.text)
# 	return soup
