'''
Created on Oct 11, 2015

@author: thrasher
'''
from datetime import date

class Option(object):
    '''
    classdocs
    '''
    CALL_CLASS = 0
    PUT_CLASS = 1


    def __init__(self, option_class, date_check, date_expiry, strike, contract_name, bid, ask, volume, open_interest, implied_volatility):
        '''
        Constructor
        '''
        self._option_class_ = option_class
        if not isinstance(date_check, date):
            print 'Error when creating option object, check date is not type date_time'
            return
        self._date_check_ = date_check
        if not isinstance(date_expiry, date):
            print 'Error when creating option object, expiry date is not type date_time'
            return
        self._date_expiry_ = date_expiry
        if not self.isFloat(strike, float):
            print 'Error when creating option object, strike cannot be converted to float'
            return
        self._strike_ = strike
        self._contract_name_ = contract_name
        if not self.isFloat(bid, float):
            print 'Error when creating option object, bid cannot be converted to float'
            return
        self._bid_ = bid
        if not self.isFloat(ask, float):
            print 'Error when creating option object, ask cannot be converted to float'
            return
        self._ask_ = ask
        if not self.isInt(volume, float):
            print 'Error when creating option object, ask cannot be converted to float'
            return
        self._volume_ = volume
        if not self.isInt(volume, open_interest):
            print 'Error when creating option object, open_interest cannot be converted to float'
            return
        self._open_interest_ = open_interest
        if not self.isFloat(implied_volatility, float):
            print 'Error when creating option object, implied_volatility cannot be converted to float'
            return
        self._implied_volatility = implied_volatility

    def get_option_class_(self):
        return self._option_class_


    def get_date_check_(self):
        return self._date_check_


    def get_date_expiry_(self):
        return self._date_expiry_


    def get_strike_(self):
        return self._strike_


    def get_contract_name_(self):
        return self._contract_name_


    def get_bid_(self):
        return self._bid_


    def get_ask_(self):
        return self._ask_


    def get_volume_(self):
        return self._volume_


    def get_open_interest_(self):
        return self._open_interest_


    def get_implied_volatility_(self):
        return self._implied_volatility_


    def set_option_class_(self, value):
        self._option_class_ = value


    def set_date_check_(self, value):
        self._date_check_ = value


    def set_date_expiry_(self, value):
        self._date_expiry_ = value


    def set_strike_(self, value):
        self._strike_ = value


    def set_contract_name_(self, value):
        self._contract_name_ = value


    def set_bid_(self, value):
        self._bid_ = value


    def set_ask_(self, value):
        self._ask_ = value


    def set_volume_(self, value):
        self._volume_ = value


    def set_open_interest_(self, value):
        self._open_interest_ = value


    def set_implied_volatility_(self, value):
        self._implied_volatility_ = value


    def del_option_class_(self):
        del self._option_class_


    def del_date_check_(self):
        del self._date_check_


    def del_date_expiry_(self):
        del self._date_expiry_


    def del_strike_(self):
        del self._strike_


    def del_contract_name_(self):
        del self._contract_name_


    def del_bid_(self):
        del self._bid_


    def del_ask_(self):
        del self._ask_


    def del_volume_(self):
        del self._volume_


    def del_open_interest_(self):
        del self._open_interest_


    def del_implied_volatility_(self):
        del self._implied_volatility_

        
    def get_bid_ask_spread(self):
        return self._ask_ - self._bid_
    
    def get_time_to_expiry(self):
        delta = self._date_expiry_ - self._date_check_
        if (delta.days < 0):
            print "Error, the option considered has already expired or some date errors"
            print "/nDate Expiry: {}".format(self._date_expiry_)
            print "/nDate check: {}".format(self._date_check_)
        return delta.days
        
        
    def isFloat(self, value):
        try:
            float(value)
            return True
        except:
            return False
        
    def isInt(self, value):
        try:
            int(value)
            return True
        except:
            return False
        
    option_class = property(get_option_class_, set_option_class_, del_option_class_, "option_class's docstring")
    date_check = property(get_date_check_, set_date_check_, del_date_check_, "date_check_'s docstring")
    date_expiry = property(get_date_expiry_, set_date_expiry_, del_date_expiry_, "date_expiry_'s docstring")
    strike = property(get_strike_, set_strike_, del_strike_, "strike_'s docstring")
    contract_name = property(get_contract_name_, set_contract_name_, del_contract_name_, "contract_name_'s docstring")
    bid = property(get_bid_, set_bid_, del_bid_, "bid_'s docstring")
    ask = property(get_ask_, set_ask_, del_ask_, "ask_'s docstring")
    volume = property(get_volume_, set_volume_, del_volume_, "volume_'s docstring")
    open_interest = property(get_open_interest_, set_open_interest_, del_open_interest_, "open_interest_'s docstring")
    implied_volatility = property(get_implied_volatility_, set_implied_volatility_, del_implied_volatility_, "implied_volatility's docstring")