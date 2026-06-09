from django.urls import path

from . import views


urlpatterns=[

    path("pricing/",views.pricing,name="pricing"),
    path("subscription/",views.subscription,name="subscription"),
    path("select-plan/",views.select_plan,name="select_plan"),
    path("dashboard/",views.billing_dashboard,name="billing_dashboard")

]