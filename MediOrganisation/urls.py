from django.urls import path

from MediPayment.views import PaymentList


urlpatterns = [
    path('organisation/', PaymentList.as_view(),name='payment-list'),
]