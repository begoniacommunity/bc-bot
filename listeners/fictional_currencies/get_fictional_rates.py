from decimal import Decimal

def get_fictional_rates(currency_code):
    rates = {
        #'AA': {'BB': Decimal('74.7')},
        #'BB': {'AA': Decimal('1') / Decimal('74.7')}
    }
    return rates.get(currency_code)