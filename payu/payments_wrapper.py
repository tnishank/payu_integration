# Web services API for Payu

import requests
from hashlib import sha512

from payu_integration import settings

url = "https://test.payu.in/merchant/postservice.php?form=2"


def payment_verification(payload):
    """
    API call for 'verify_payment'
    """
    response = requests.post(url, data=payload)
    return response.json()


def payment_check(payload):
    """
    API call for 'check_payment'
    """
    response = requests.post(url, data=payload)
    return response.json()


def get_invoice(payload):
    """
    API call for 'create_invoice'
    """
    response = requests.post(url, data=payload)
    return response.json()


def cancel_or_refund_request(payload):
    """
    API call for 'cancel_refund_transaction'
    """
    response = requests.post(url, data=payload)
    return response.json()


def check_action_status(payload):
    """
    API call for 'check_action_status'
    """
    response = requests.post(url, data=payload)
    return response.json()


def get_transaction_detail(payload):
    """
    API call for 'get_Transaction_Details'
    """
    response = requests.post(url, data=payload)
    return response.json()


def create_hash_for_post_payment(*args, **kwargs):
    """
    Creates hash for Payu's web services api calls
    """
    KEYS = ('command', 'var1')
    hash = sha512(settings.PAYU_INFO["merchant_key"])
    for key in KEYS:
        try:
            hash.update("%s%s" % ('|', kwargs[key]))
        except KeyError:
            pass
    hash.update("%s%s" % ('|', settings.PAYU_INFO["merchant_salt"]))
    return hash.hexdigest().lower()
