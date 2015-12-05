'''
Created on Oct 10, 2015

@author: thrasher
'''

import urllib2
from datetime import datetime
from datetime import date
import YahooOption
import ConfigParser
from bs4 import BeautifulSoup
from pandas import np, Series
from pandas.io.data import DataReader
from yahoo_finance import Share

class YahooDataFeeder():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def read_config(self):
        """Read configuration file config.ini    
        :return: tickers as list
        """
        my_parser = ConfigParser.ConfigParser()
        my_parser.read('config.ini')
        try:
            tickers_list = my_parser.get('Tickers', 'TickerList')
            return tickers_list.replace(' ', '').replace(';', ',').split(',')
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            return None


    def get_soup(self,url):
        """Cooking the soup
    
        :param url: string
        :return: BeautifulSoup object
        """
        try:
            html_source = urllib2.urlopen(url)
        except urllib2.URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
            return None
        my_soup = BeautifulSoup(html_source, "html.parser")
        return my_soup


    def get_headers(self,search_soup):
        """Scrape headers
    
        Given BeautifulSoup object
        :param search_soup: BeautifulSoup object
        :return: headers as list
        """
    
        div = search_soup.find('div', id='optionsCallsTable')
        if div:
            opt_table = div.find('table')
            if opt_table:
                headers = ['Date', 'Expire Date', 'Option Type']
                headers.extend([self.get_clean(th.text) for th in opt_table.find_all('th')])
                return headers


    def get_quotes(self, search_soup, expire_date, options=None):
        """Scrape quotes row by row
    
        Given BeautifulSoup object, expire-date
        :param search_soup: BeautifulSoup object
        :param expire_date: datetime object
        :param options: list or tuple of string option types, e.g. ['call']. Default is None resulting in both Call and Put
        :return: list of lists of quotes data
        """
    
        all_quotes = []
        today_date = datetime.strftime(date.today(), '%d.%m.%Y')
        exp_date = datetime.strftime(expire_date, '%d.%m.%Y')
        if not options:
            options = ['Call', 'Put']
        for opt in options:
            div = search_soup.find('div', id='options{}sTable'.format(opt))
            if div:
                opt_table = div.find('table')
                if opt_table:
                    tbody = opt_table.find('tbody')
                    if tbody:
                        for tr in tbody.find_all('tr'):
                            row_quotes = [td.text.strip().replace(',', '') for td in tr.find_all('td')]
                            if row_quotes:
                                my_quotes = [today_date, exp_date, opt]
                                my_quotes.extend(row_quotes)
                                all_quotes.append(my_quotes)
                    else:
                        print '\nUnable to find <tbody> tag for {} options for expire date {}\n'.format(opt, exp_date)
                else:
                    print '\nUnable to find <table> for {} options for expire date {}\n'.format(opt, exp_date)
        return all_quotes


    def get_clean(self,s):
        """Clean string from specific chars
    
        Clean headers from specific unicode chars, used as up/down arrows for sort
        :param s: string to clean
        :return: clean string
        """
        return s.replace(u'\n', '').replace(u'\ue004\ue002', '').replace(u'\u2235 Filter', '')


    def get_options(self, ticker):
        expire_list = []
        option_list = []
        result = None
        soup = self.get_soup('http://finance.yahoo.com/q/op?s={}'.format(ticker))
        if soup:
            options_menu = soup.find('div', id='options_menu')
            if options_menu:
                select = options_menu.find('select')
                expire_dates = [datetime.strptime(option.text, '%B %d, %Y') for option in select.find_all('option')]
                expire_dates_with_links = [[datetime.strptime(option.text, '%B %d, %Y'), option['data-selectbox-link']]
                                for option in select.find_all('option')]
                if expire_dates_with_links:
                    #headers = self.get_headers(soup)
#                     csv.register_dialect('yahoo', delimiter=',', quoting=csv.QUOTE_NONE, lineterminator='\n')
#                     if os.path.isfile('{}.csv'.format(ticker)):
#                         with open('{}.csv'.format(ticker), 'r') as f:
#                             current_headers = csv.DictReader(f).fieldnames
#                     else:
#                         current_headers = None
                    #with open('{}.csv'.format(ticker), 'a') as f:
#                         my_writer = csv.DictWriter(f, fieldnames=current_headers, dialect='yahoo')
                        # add headers if new file
#                         if not my_writer.fieldnames:
#                             my_writer.fieldnames = headers
                            #my_writer.writeheader()
                        # loop trough all expire dates
                    for exp_date, link in expire_dates_with_links:
                        print 'Expire date and link: {}, {}'.format(datetime.strftime(exp_date,  '%d.%m.%Y'), link)
                        soup = self.get_soup('http://finance.yahoo.com{}'.format(link))
                        #my_writer.writerows([dict(zip(headers, quotes)) for quotes in self.get_quotes(soup, exp_date)])
                        #exp_date_date = datetime.datetime.strptime(exp_date, "%d.%m.%Y")
                        for quotes in self.get_quotes(soup, exp_date):
                            yahoo_option = YahooOption.YahooOption(quotes)
                            option_list.append(yahoo_option)
                            #print quotes
                        expire_list.append(option_list)
                    result = Series(expire_list, index = expire_dates)  
                else:
                    print type(self).__name__
                    print 'It looks like there are no options for ticker: {}'.format(ticker)
            else:
                print 'It looks like there is no such ticker: {}'.format(ticker)
        else:
            print 'Unable to retrieve html. Check the Internet connection and/or try again later.'
        return result     
            
    def get_tickers_list(self,site):
        if site == None:
            site = "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = urllib2.Request(site, headers=hdr)
        page = urllib2.urlopen(req)
        soup = BeautifulSoup(page, "html.parser")
    
        table = soup.find('table', {'class': 'wikitable sortable'})
        sector_tickers = dict()
        for row in table.findAll('tr'):
            col = row.findAll('td')
            if len(col) > 0:
                sector = str(col[3].string.strip()).lower().replace(' ', '_')
                ticker = str(col[0].string.strip())
                if sector not in sector_tickers:
                    sector_tickers[sector] = list()
                sector_tickers[sector].append(ticker)
        return sector_tickers 

    def get_historical_volatility(self, ticker, days):
        '''Return the annualized stddev of daily log returns of symbol ticker.'''
        try:
            quotes = DataReader(ticker, 'yahoo')['Close'][-days:]
        except Exception, e:
            print "Error getting data for symbol '{}'.\n".format(ticker), e
            return None, None
        logreturns = np.log(quotes / quotes.shift(1))
        historical_volatility = np.sqrt(252*logreturns.var())
        print 'Historical volatility for ticker '+str(ticker)+' is '
        print historical_volatility
        return historical_volatility
    
    def get_current_price(self, ticker):
        '''Return the current EOD price for symbol ticker'''
        share = Share(ticker)
        price = share.get_price()
        try:
            return float(price)
        except ValueError:
            print 'Error when getting the price for ticker {}'.format(ticker)
            return None
        return price
            