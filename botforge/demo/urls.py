from django.urls import path
from .views import *

urlpatterns=[

    path('school/',school_demo_bot,name='school_demo_bot'),
    path('healthcare/',healthcare_demo_bot,name='healthcare_demo_bot'),
    path('ecommerce/',ecommerce_demo_bot,name='ecommerce_demo_bot'),
    path('chat/<str:bot_type>/',chatbot_api,name='chatbot_api')
    
   
]