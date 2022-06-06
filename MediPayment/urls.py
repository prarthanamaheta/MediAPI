from django.urls import path
from . import views

from MediPayment.views import PaymentList, SuccessView

urlpatterns = [
    path('payment/', PaymentList.as_view(), name='payment-list'),
    path('checkout/', views.create_checkout_session, name='checkout'),
    path('success/', SuccessView.as_view())
]
