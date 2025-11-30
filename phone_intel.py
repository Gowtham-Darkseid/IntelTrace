"""Phone intelligence: carrier lookup, country code detection."""
import phonenumbers
from phonenumbers import geocoder, carrier


class PhoneIntel:
    def __init__(self):
        pass

    def parse_number(self, number, region=None):
        try:
            pn = phonenumbers.parse(number, region)
            return pn
        except Exception:
            return None

    def carrier_info(self, number, region=None):
        pn = self.parse_number(number, region)
        if not pn:
            return {}
        return {
            'number': phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.E164),
            'country': geocoder.country_name_for_number(pn, 'en'),
            'carrier': carrier.name_for_number(pn, 'en')
        }

    def collect(self, number):
        return self.carrier_info(number)
