from django.shortcuts import render


def home(request):

    return render(request,"core/home.html")

def privacy_policy(request):
     return render(request,"core/privacy_policy.html")
 
def terms_and_conditions(request):
     return render(request,"core/terms_and_conditions.html")