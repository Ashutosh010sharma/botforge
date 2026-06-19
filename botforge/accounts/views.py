from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from .forms import CompanyRegisterForm
from .models import Company
from django.contrib.auth import logout
from billing.models import (
    Plan,
    Subscription
)
from django.utils.timezone import localtime


def register_view(request):

    form = CompanyRegisterForm()

    if request.method == "POST":

        form = CompanyRegisterForm(request.POST)

        try:

            if form.is_valid():

                with transaction.atomic():

                    user = form.save(
                        commit=False
                    )

                    # Hash password
                    password = form.cleaned_data[
                        "password"
                    ]

                    user.set_password(
                        password
                    )

                    user.save()


                    # Company.objects.create(
                    #     user=user,
                    #     company_name=request.POST.get(
                    #         "company_name"
                    #     ),
                    #     website_url=request.POST.get(
                    #         "website_url"
                    #     )
                    # )

                    login(
                        request,
                        user
                    )

                    messages.success(
                        request,
                        "Registration completed successfully."
                    )

                    return redirect(
                        "dashboard"
                    )

            else:

                for field, errors in form.errors.items():

                    for error in errors:

                        messages.error(
                            request,
                            f"{field}: {error}"
                        )

        except Exception as e:

            messages.error(
                request,
                f"Registration failed: {str(e)}"
            )

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )


def login_view(request):

    form = AuthenticationForm(
        request,
        data=request.POST or None
    )

    try:

        if request.method == "POST":

            if form.is_valid():

                user = form.get_user()

                login(
                    request,
                    user
                )

                messages.success(
                    request,
                    "Login successful."
                )

                return redirect(
                    "dashboard"
                )

            else:

                messages.error(
                    request,
                    "Invalid username or password."
                )

    except Exception as e:

        messages.error(
            request,
            f"Login failed: {str(e)}"
        )

    return render(
        request,
        "accounts/login.html",
        {
            "form": form
        }
    )


@login_required
def dashboard(request):

    company = Company.objects.filter(
        user=request.user
    ).first()

    subscription = None

    if company:

        subscription = Subscription.objects.filter(

            company=company,

            is_active=True

        ).select_related(
            "plan"
        ).first()

    context = {

        "company": company,

        "subscription": subscription

    }

    return render(

        request,

        "accounts/dashboard.html",

        context

    )

def logout_view(request):

    try:

        logout(request)

        messages.success(
            request,
            "Logged out successfully."
        )

    except Exception as e:

        messages.error(
            request,
            f"Logout failed : {str(e)}"
        )

    return redirect(
        "login"
    )
    
@login_required

def company_setup(request):

    try:

        company = Company.objects.filter(
            user=request.user
        ).first()

        if company:

            return JsonResponse({

                "status": False,

                "message": "Company already exists."

            })

        if request.method == "POST":

            # logo_name = None

            # if request.FILES.get("logo"):

            #     logo = request.FILES.get(
            #         "logo"
            #     )

            #     import time
            #     import os

            #     extension = os.path.splitext(
            #         logo.name
            #     )[1]

            #     logo_name = (
            #         f"company_{int(time.time())}"
            #         f"{extension}"
            #     )

            #     upload_path = os.path.join(
            #         "media",
            #         "company_logos",
            #         logo_name
            #     )

            #     os.makedirs(
            #         os.path.dirname(
            #             upload_path
            #         ),
            #         exist_ok=True
            #     )

            #     with open(
            #         upload_path,
            #         "wb+"
            #     ) as destination:

            #         for chunk in logo.chunks():

            #             destination.write(
            #                 chunk
            #             )

            company = Company.objects.create(

                user=request.user,

                company_name=request.POST.get(
                    "company_name"
                ),

                website_url=request.POST.get(
                    "website_url"
                ),

                industry=request.POST.get(
                    "industry"
                ),

                location=request.POST.get(
                    "location"
                ),

                description=request.POST.get(
                    "description"
                )

                # logo_url=logo_name

            )

            free_plan = Plan.objects.filter(
                slug="free",
                is_active=True
            ).first()

            if free_plan:

                Subscription.objects.get_or_create(

                    company=company,

                    defaults={

                        "plan": free_plan,

                        "is_active": True

                    }

                )

            return JsonResponse({

                "status": True,

                "message": (
                    "Company created successfully."
                )

            })

        return render(

            request,

            "accounts/company_setup.html"

        )

    except Exception as e:

        return JsonResponse({

            "status": False,

            "message": str(e)

        })
        
@login_required
def get_profile_details(request):

    user = request.user

    company = Company.objects.filter(user=user).first()

    subscription = Subscription.objects.filter(
        company=company,
        is_active=True
    ).select_related("plan").first() if company else None

    data = {

        "full_name": user.get_full_name() or user.username,

        "username": user.username,

        "email": user.email,

        "avatar": user.first_name[:1].upper() if user.first_name else user.username[:1].upper(),

        "member_since": user.date_joined.strftime("%d %B %Y"),

        "email_verified": True,      # replace with your verification field

        "account_status": "Active" if user.is_active else "Inactive",

        "current_plan": subscription.plan.name if subscription else "No Active Plan",

        "workspace": company.company_name if company else "Not Configured",

        "last_login": (
            localtime(user.last_login).strftime("%d %b %Y %I:%M %p")
            if user.last_login else "Never"
        )
    }

    return JsonResponse({
        "status": True,
        "data": data
    })