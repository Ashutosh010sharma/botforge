from django.urls import path

from . import views


urlpatterns=[

    path("pricing/",views.pricing,name="pricing"),
    path("subscription/",views.subscription,name="subscription"),
    path("select-plan/",views.select_plan,name="select_plan"),
    path("dashboard/",views.billing_dashboard,name="billing_dashboard"),
    path("create-payment-order/",views.create_payment_order,name="create_payment_order"),
    path("verify-payment/",views.verify_payment,name="verify_payment"),
    path("razorpay/webhook/",views.razorpay_webhook,name="razorpay_webhook")

]