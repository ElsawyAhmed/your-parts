from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('sum', get_sum, name='get-sum')
]