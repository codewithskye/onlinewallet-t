from django.shortcuts import render, redirect
from .models import Payment, UserWallet
from django.conf import settings
from django.contrib.auth.models import User


def initiate_payment(request):
    if request.method == "POST":
        amount = request.POST['amount']
        user_email = User.objects.get(pk=request.user.pk)
        email = user_email.email
        # email = request.POST['email']

        pk = settings.PAYSTACK_PUBLIC_KEY

        payment = Payment.objects.create(amount=amount, email=email, user=request.user)
        payment.save()

        context = {
            'payment': payment,
            'field_values': request.POST,
            'paystack_pub_key': pk,
            'amount_value': amount,
        }
        return render(request, 'app/make_payment.html',
                       context
                       )

    return render(request, 'app/payment.html')

# Secret key: sk_live_4ee57b3fc56327894060cc0dc52c8983817d6d47

# Public key: pk_live_71803a31de8f59639cd26ddde3a35fe755d40b03

def verify_payment(request, ref):
    payment = Payment.objects.get(ref=ref)
    status, verified = payment.verify_payment()
    print('status checking', status)

    # if verified:
        # user = request.user
        # Transaction.objects.filter(creator=user, is_complete=True, transaction_type='send', amount=payment.amount).order_by('-create_date')

    #     user_wallet = UserWallet.objects.get(user=request.user)
    #     user_wallet.balance += payment.amount
    #     user_wallet.save()
    # transaction history
    #     print(request.user.username, " funded wallet successfully")
    #     return render(request, "success.html")
    # else :
             # user = request.user
        # Transaction.objects.filter(creator=user, is_complete=True, transaction_type='send', amount=payment.amount).order_by('-create_date')
    return render(request, "success.html")