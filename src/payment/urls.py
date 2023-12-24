from django.urls import path
from payment import views

app_name = 'payment'

urlpatterns = [
    path('items/', views.ShowItems.as_view(), name='items'),
    path('item/<pk>', views.ShowItem.as_view(), name='item'),
    path('buy/<pk>', views.CreateStripeSession.as_view(), name='create_stripe_session'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
]
