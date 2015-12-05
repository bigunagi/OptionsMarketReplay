'''
Created on Oct 11, 2015

@author: thrasher
'''
from Common.Option import Option
import datetime

class YahooOption(Option):
    '''
    classdocs
    '''
    YAHOO_ARRAY_SIZE = 13

    def __init__(self, yahoo_array):
        '''
        Constructor
        '''
        if not len(yahoo_array) == self.YAHOO_ARRAY_SIZE:
            print 'Error creating Yahoo Option! No standard array provided, {}'.format(len(yahoo_array))
            return
        self.set_date_check_(datetime.datetime.strptime(yahoo_array[0], "%d.%m.%Y"))
        self.set_date_expiry_(datetime.datetime.strptime(yahoo_array[1], "%d.%m.%Y"))
        if yahoo_array[2]=='Call':
            self.set_option_class_(Option.CALL_CLASS)
        elif yahoo_array[2]=='Put':
            self.set_option_class_(Option.CALL_CLASS)
        else:
            print 'Error creating Yahoo Option! No call or put option defined'
            return
        self.set_strike_(yahoo_array[3])
        self.set_contract_name_(yahoo_array[4])
        self.set_bid_(yahoo_array[6])
        self.set_ask_(yahoo_array[7])
        self.set_volume_(yahoo_array[10])
        self.set_open_interest_(yahoo_array[11])
        self.set_implied_volatility_(yahoo_array[12])
    