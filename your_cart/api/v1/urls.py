from django.urls import path
from .views import *


app_name = 'your_cart'

urlpatterns = [
    path('sum', get_sum)
]