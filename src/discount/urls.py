from django.urls import path
from discount import views

app_name = 'discount'

urlpatterns = [
    path('check/', views.CheckDiscount.as_view(), name='check'),
]
