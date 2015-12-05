'''
Created on Oct 11, 2015

@author: thrasher
'''
import traceback
from  OptionsDataFeeder import YahooDataFeeder
from OptionsGreeksCalculator import GreeksCalculator

if __name__ == '__main__':
    dataFeeder = YahooDataFeeder.YahooDataFeeder()
    #get list of tickers (by default from S&P500)
    tickers = dataFeeder.get_tickers_list(None)
    #print tickers.keys()

    for field_key in tickers.keys():
        for tkr in tickers[field_key]:  # loop trough tickers
            print '\nStart download for ticker {}'.format(tkr.upper())            
            hist_volatility = dataFeeder.get_historical_volatility(tkr,30) #30 days
            curent_price = dataFeeder.get_current_price(tkr)
            options_table = dataFeeder.get_options(tkr)
            try:
                for expire_date_list in options_table:
                    for option in expire_date_list:
                        greeks = GreeksCalculator.BSVanilla(option, [curent_price, 0.0, 0.0, hist_volatility])
                        print "Delta is " + str(greeks.Delta())
                        print "Gamma is " + str(greeks.Gamma())
                        print "Theta is " + str(greeks.Theta())
            except Exception as ex:
                traceback.print_exc()
            print 'Download complete for ticker {}'.format(tkr.upper())

            