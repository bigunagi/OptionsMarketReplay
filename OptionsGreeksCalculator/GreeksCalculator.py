'''
Created on Oct 11, 2015

@author: thrasher
'''

from math import log, e
from scipy.stats import norm
from Common.Option import Option
 
class GreeksValueOption(object):
    
    def __init__(self, option, args):
        if option.get_option_class_() == Option.CALL_CLASS:
            self.Type = 1               # 1 for a Call, - 1 for a put
        elif option.get_option_class_() == Option.PUT_CLASS:
            self.Type = -1
        else:
            print "Error when creating GreeksValueOption, option base is not a Call nor a Put type: {}".format(option.option_class)
        try:
            self.underlying_price = float(args[0])                 # Underlying asset price
            self.K = float(option.strike)                 # Option strike K
            self.r = float(args[1])                 # Continuous risk fee rate
            self.q = float(args[2])                 # Dividend continuous rate/ dividend yield?
            self.T = float(option.get_time_to_expiry()) / 365.0         # Compute time to expiry (given in days)
            self._sigma = float(args[3])             # Underlying HISTORICAL volatility = Volatility measured by annual standard deviation
            self.sigmaT = self._sigma * self.T ** 0.5  # sigma*T for reusability
        except ValueError as ex:
            print "Error when passing arguments to GreeksOption calculator, some of the values are not float"
 
    @property
    def d2(self):
        return self.d1 - self.sigmaT
 
class BSVanilla(GreeksValueOption):
    
    def __init__(self, option, args):
        super(BSVanilla, self).__init__(option, args)
 
    @property
    def d1(self):
        return (log(self.underlying_price / self.K) + (self.r - self.q + 0.5 * (self.sigma ** 2)) * self.T) / self.sigmaT
 
    @property
    def sigma(self):
        return self._sigma
    @sigma.setter
    def sigma(self, val):
        self._sigma = val
        self.sigmaT = val * self.T ** 0.5
 
    def Premium(self):
        tmpprem = self.Type * (self.underlying_price * e ** (-self.q * self.T) * norm.cdf(self.Type * self.d1) - \
                self.K * e ** (-self.r * self.T) * norm.cdf(self.Type * self.d2))
        return tmpprem
 
    ############################################
    ############ 1st order greeks ##############
    ############################################
 
    def Delta(self):
        dfq = e ** (-self.q * self.T)
        if self.Type == 1:
            result = dfq * norm.cdf(self.d1)
            if ((result < 0.0) or (result > 1.0)):
                print "Delta calculated is wrong! It should be between 0.0 and 1.0 for CALL options"
        else:
            result = dfq * (norm.cdf(self.d1) - 1)
            if ((result > 0.0) or (result < -1.0)):
                print "Delta calculated is wrong! It should be between -1.0 and 0.0 for PUT options"
        return result
 
    # Vega for 1% change in vol
    def Vega(self):
        return 0.01 * self.underlying_price * e ** (-self.q * self.T) * \
          norm.pdf(self.d1) * self.T ** 0.5
 
    # Theta for 1 day change
    def Theta(self):
        df = e ** -(self.r * self.T)
        dfq = e ** (-self.q * self.T)
        tmptheta = (1.0 / 365.0) \
            * (-0.5 * self.underlying_price * dfq * norm.pdf(self.d1) * \
               self.sigma / (self.T ** 0.5) + \
            self.Type * (self.q * self.underlying_price * dfq * norm.cdf(self.Type * self.d1) \
            - self.r * self.K * df * norm.cdf(self.Type * self.d2)))
        return tmptheta
 
    def Rho(self):
        df = e ** -(self.r * self.T)
        return self.Type * self.K * self.T * df * 0.01 * norm.cdf(self.Type * self.d2)
 
    def Phi(self):
        return 0.01 * -self.Type * self.T * self.underlying_price * \
             e ** (-self.q * self.T) * norm.cdf(self.Type * self.d1)
 
    ############################################
    ############ 2nd order greeks ##############
    ############################################
 
    def Gamma(self):
        return e ** (-self.q * self.T) * norm.pdf(self.d1) / (self.underlying_price * self.sigmaT)
 
    # Charm for 1 day change
    def Charm(self):
        dfq = e ** (-self.q * self.T)
        if self.Type == 1:
            return (1.0 / 365.0) * -dfq * (norm.pdf(self.d1) * ((self.r - self.q) / (self.sigmaT) - self.d2 / (2 * self.T)) \
                            + (-self.q) * norm.cdf(self.d1))
        else:
            return (1.0 / 365.0) * -dfq * (norm.pdf(self.d1) * ((self.r - self.q) / (self.sigmaT) - self.d2 / (2 * self.T)) \
                            + self.q * norm.cdf(-self.d1))
 
    # Vanna for 1% change in vol
    def Vanna(self):
        return 0.01 * -e ** (-self.q * self.T) * self.d2 / self.sigma * norm.pdf(self.d1)
 
    # Vomma
    def Vomma(self):
        return 0.01 * -e ** (-self.q * self.T) * self.d2 / self.sigma * norm.pdf(self.d1)
 
# Geometric Continuous Average-Rate Options
# Following Kemna and Vorst (1990), see Haug
class BSAsian(GreeksValueOption):
    
    def __init__(self, option,  args):
        super(BSAsian, self).__init__(option, args)
        self.sigmaT = self.sigmaa * self.T ** 0.5
 
    @property
    def d1(self):
        return (log(self.underlying_price / self.K) + (self.ba + 0.5 * (self.sigmaa ** 2)) * self.T) / self.sigmaT
 
    @property
    def sigmaa(self):
        return self._sigma / (3.0 ** 0.5)
 
    @property
    def sigma(self):
        return self._sigma
    @sigma.setter
    def sigma(self, val):
        self._sigma = val
        self.sigmaT = self.sigmaa * self.T ** 0.5
 
    @property
    def ba(self):
        return 0.5 * (self.r - self.q - (self._sigma ** 2) / 6.0)
 
    def Premium(self):
        tmpprem = self.Type * (self.underlying_price * e ** ((self.ba - self.r) * self.T) * norm.cdf(self.Type * self.d1) - \
                self.K * e ** (-self.r * self.T) * norm.cdf(self.Type * self.d2))
        return tmpprem


#excample of parameters
# Option parameters
#sigma = 0.12        # Flat volatility
#strike = 105.0      # Fixed strike
#riskfree = 0.00     # Continuous risk free rate
#divrate = 0.00      # Continuous div rate
#y time to expire in days

#BSMerton([1,x,strike,riskfree,divrate,y,sigma]