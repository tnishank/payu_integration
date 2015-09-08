from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(r'^checkout/?$', views.checkout, name='ref_checkout'),
    url(r'^success/?$', views.payment_success, name='ref_payment_success'),
    url(r'^fail/?$', views.payment_fail, name='ref_payment_fail'),
    url(r'^cancel/?$', views.payment_cancel, name='ref_payment_cancel'),
    url(r'^payment_verification/?$', views.payment_verify, name='ref_payment_verify'),
    url(r'^payment_status/?$', views.payment_status, name='ref_payment_status'),
    url(r'^invoice/?$', views.generate_invoice, name='ref_generate_invoice'),
    url(r'^cancel_refund_request/?$', views.cancel_refund_request, name='ref_cancel_refund_request'),
    url(r'^cancel_refund_status/?$', views.cancel_refund_status, name='ref_cancel_refund_status'),
    url(r'^get_transaction_detail/?$', views.transaction_detail, name='ref_transaction_detail'),
)
