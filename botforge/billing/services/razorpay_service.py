import razorpay
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from billing.models import Payment, Subscription
from django.conf import settings


client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET,
    )
)

@transaction.atomic
@transaction.atomic
def activate_subscription(payment):

    # --------------------------
    # Duplicate Protection
    # --------------------------

    if payment.is_verified:

        return

    company = payment.company

    plan = payment.plan

    today = timezone.now()

    subscription = Subscription.objects.filter(

        company=company

    ).first()

    # --------------------------
    # Calculate Start Date
    # --------------------------

    if subscription:

        if (

            subscription.end_date and

            subscription.end_date > today

        ):

            start_date = subscription.end_date

        else:

            start_date = today

    else:

        start_date = today

    # --------------------------
    # Calculate End Date
    # --------------------------

    if payment.billing_cycle == "monthly":

        end_date = start_date + relativedelta(months=1)

    else:

        end_date = start_date + relativedelta(years=1)

    # --------------------------
    # Create / Update Subscription
    # --------------------------

    if subscription:

        subscription.plan = plan

        subscription.payment = payment

        subscription.billing_cycle = payment.billing_cycle

        subscription.start_date = today

        subscription.end_date = end_date

        subscription.renewal_count += 1

        subscription.is_active = True

        subscription.save()

    else:

        Subscription.objects.create(

        company=company,

        plan=plan,

        payment=payment,

        billing_cycle=payment.billing_cycle,

        start_date=today,

        end_date=end_date,

        is_active=True,

    )

    # --------------------------
    # Update Payment
    # --------------------------

    payment.status = "paid"

    payment.is_verified = True

    payment.save()

    return subscription
    
