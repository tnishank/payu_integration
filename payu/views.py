# Django import
from django.conf import settings
from django.shortcuts import render_to_response, render
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext

# Third party import
from rest_framework.decorators import api_view
from uuid import uuid4
import requests
import json


# App import
from .utils import verify_hash, generate_hash
from payu_integration.responses import send_200, send_422, send_400
from payments_wrapper import payment_verification, get_invoice, \
    cancel_or_refund_request, check_action_status, get_transaction_detail,\
    payment_check, create_hash_for_post_payment

key = settings.PAYU_INFO["merchant_key"]


@api_view(['POST', 'GET'])
def checkout(request):
    """
    Information needed to checkout
    """
    if request.method == 'POST':
        txnid = uuid4().hex
        productinfo = "sample product info"
        amount = request.data.get('amount')
        firstname = request.data.get('firstname')
        email = request.data.get('email')
        phone = request.data.get('phone')
        key = settings.PAYU_INFO['merchant_key']
        surl = request.build_absolute_uri(reverse('ref_payment_success'))
        furl = request.build_absolute_uri(reverse('ref_payment_fail'))
        curl = request.build_absolute_uri(reverse('ref_payment_cancel'))
        hashh = generate_hash(
            txnid=txnid,
            productinfo=productinfo,
            amount=amount,
            firstname=firstname,
            email=email,
            key=key)

        payload = {'txnid': txnid,
                   'productinfo': productinfo,
                   'amount': amount,
                   'firstname': firstname,
                   'email': email,
                   'phone': phone,
                   'key': key,
                   'hash': hashh,
                   'surl': surl,
                   'furl': furl,
                   'curl': curl}
        response = requests.post(settings.PAYU_INFO["payment_url"], data=payload)
        return send_200({"message": response.url})

    else:
        return render(request, 'checkout.html')


@csrf_exempt
def payment_success(request):
    """
    After successful transaction payu will redirect here to proceed further
    """
    if request.method == 'POST':
        if not verify_hash(request.POST):
            return send_400({"message": "Data got tampered"})
        else:
            return render_to_response('success.html', RequestContext(request))

@csrf_exempt
def payment_fail(request):
    """
    Payu will redirect here when payment get failed
    """
    if request.method == 'POST' or 'GET':
        return render_to_response('failure.html', RequestContext(request))

@csrf_exempt
def payment_cancel(request):
    """
    After cancelling the transaction at payu end will be redirected here
    """
    if request.method == 'POST' or 'GET':
        return render_to_response('cancel.html', RequestContext(request))

@api_view(['POST'])
def payment_verify(request):
    """
    Verifies transaction returns related details
    """
    txnid = request.POST['txnid']
    command = "verify_payment"
    hashh = create_hash_for_post_payment(command=command, var1=txnid)
    payload = {"key": key, "command": command, "var1": txnid, "hash": hashh}
    response = payment_verification(payload)
    return send_200({"message": response})


@api_view(['POST'])
def payment_status(request):
    """
    Verifies transaction returns some extra details as compared with payment_verify
    """
    mihpayid = request.POST['mihpayid']
    command = "check_payment"
    hashh = create_hash_for_post_payment(command=command, var1=mihpayid)
    payload = {"key": key, "command": command, "var1": mihpayid, "hash": hashh}
    response = payment_check(payload)
    return send_200({"message": response})


@api_view(['POST'])
def generate_invoice(request):
    """
    Generates invoice to user from PayU
    """
    txnid = request.data.get("txnid")
    amount = request.data.get("amount")
    productinfo = request.data.get("productinfo")
    firstname = request.data.get("firstname")
    email = request.data.get("email")
    phone = request.data.get("phone")
    validation_period = request.POST["validation_period"]
    send_email_now = request.POST["send_email_now"]
    command = "create_invoice"
    var1 = json.dumps({"amount": amount,
                       "txnid": txnid,
                       "productinfo": productinfo,
                       "firstname": firstname,
                       "email": email,
                       "phone": phone,
                       "validation_period": validation_period,
                       "send_email_now": send_email_now})
    hashh = create_hash_for_post_payment(command=command, var1=var1)
    payload = {"key": key, "command": command, "var1": var1, "hash": hashh}
    response = get_invoice(payload)
    return send_200({"message": response})


@api_view(['POST'])
def cancel_refund_request(request):
    """
    Request for cancel or refund transaction
    """
    mihpayid = request.POST['payu_id']
    token_id = uuid4().hex
    amount = request.POST['amount']
    key = settings.PAYU_INFO["merchant_key"]
    command = 'cancel_refund_transaction'
    hashh = create_hash_for_post_payment(
        command=command,
        var1=mihpayid,
        var2=token_id,
        var3=amount)
    payload = {
        'key': key,
        'command': command,
        'hash': hashh,
        'var1': mihpayid,
        'var2': token_id,
        'var3': amount}
    response = cancel_or_refund_request(payload)
    return send_200({"message": response})


@api_view(['POST'])
def cancel_refund_status(request):
    """
    Returns status of cancel or refund request transaction
    """
    request_id = request.POST['request_id']
    command = 'check_action_status'
    hashh = create_hash_for_post_payment(command=command, var1=request_id)
    payload = {
        'key': key,
        'command': command,
        'hash': hashh,
        'var1': request_id}
    response = check_action_status(payload)
    return send_200({"message": response})


@api_view(['POST'])
def transaction_detail(request):
    """
    Returns transaction detail between window of date
    """
    old_date = request.POST['old_date']
    recent_date = request.POST['recent_date']
    command = 'get_Transaction_Details'
    hashh = create_hash_for_post_payment(command=command, var1=old_date)
    payload = {
        'key': key,
        'command': command,
        'hash': hashh,
        'var1': old_date,
        'var2': recent_date}
    response = get_transaction_detail(payload)
    return send_200({"message": response})
