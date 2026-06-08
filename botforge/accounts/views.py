from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from .forms import CompanyRegisterForm
from .models import Company
from django.contrib.auth import logout


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
        user=request.user,
        
    ).first()

    context = {

        "company": company

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