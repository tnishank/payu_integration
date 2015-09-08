from hashlib import sha512
from django.conf import settings
KEYS = ('key', 'txnid', 'amount', 'productinfo', 'firstname', 'email',
        'udf1', 'udf2', 'udf3', 'udf4', 'udf5', 'udf6', 'udf7', 'udf8',
        'udf9', 'udf10')


def generate_hash(*args, **kwargs):
    hash = sha512('')
    for key in KEYS:
        try:
            key = str(kwargs[key])
        except KeyError:
            key = ''
        hash.update("%s%s" % (key, '|'))
    hash.update(settings.PAYU_INFO.get('merchant_salt'))
    return hash.hexdigest().lower()


def verify_hash(data):
    hash = sha512('')
    if not data.get('additionalCharges'):
        hash.update("%s" % (settings.PAYU_INFO.get('merchant_salt')))
    else:
        hash.update("%s" % data.get('additionalCharges'))
        hash.update("%s%s" % ('|', settings.PAYU_INFO.get('merchant_salt')))

    hash.update("%s%s" % ('|', str(data.get('status', ''))))
    for key in KEYS[::-1]:
        hash.update("%s%s" % ('|', str(data.get(key, ''))))
    return hash.hexdigest().lower() == data.get('hash')
