import stripe
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from MediPayment.models import Transaction
from MediPayment.serializers import PaymentSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.price_id = settings.STRIPE_PRICE_ID
YOUR_DOMAIN = settings.DOMAIN


class PaymentList(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = PaymentSerializer


@csrf_exempt
def create_checkout_session(request):
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': stripe.price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://127.0.0.1:8000/Payment/success/',
            cancel_url='http://127.0.0.1:8000/Payment/fail/',
        )
        request.session['payment_id'] = checkout_session.id

    except stripe.error.CardError as e:
        print("A payment error occurred: {}".format(e.user_message))

    # return "success"
    return Response('success', status=status.HTTP_303_SEE_OTHER)


class SuccessView(APIView):
    queryset = Transaction.objects.all()
    serializer_class = PaymentSerializer

    def get(self, request, *args, **kwargs):
        session = stripe.checkout.Session.retrieve(
            request.session['payment_id'],
            expand=['customer_details']
        )
        try:
            if session.status == 'complete':
                t = Transaction(payment_id=request.session['payment_id'],
                                amount=session.amount_total / 100, status='success',
                                name=session.customer_details.name,
                                email=session.customer_details.email)
                t.save()
                subject = 'Thanking for donation'
                message = f'Hi {session.customer_details.name}, thank you for donating and helping MediCare.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [session.customer_details.email, ]
                send_mail(subject, message, email_from, recipient_list)
                return Response('success', status=status.HTTP_202_ACCEPTED)

        except:

            t = Transaction(payment_id=request.session['payment_id'],
                            amount=session.amount_total, status='fail',
                            name=session.customer_details.name)
            t.save()
            return Response('fail', status=status.HTTP_503_SERVICE_UNAVAILABLE)
