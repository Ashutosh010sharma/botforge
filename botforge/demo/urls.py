from django.urls import path
from .views import *

urlpatterns=[

    path('school/',school_demo_bot,name='school_demo_bot'),
    path('school/chat/',school_chat_api, name='school_chat_api')
]