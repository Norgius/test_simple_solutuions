from django.urls import path
from payment import views

app_name = 'payment'

urlpatterns = [
    path('', views.ShowItems.as_view(), name='items'),
    path('item/<pk>/', views.ShowItem.as_view(), name='item'),

    path('order/<pk>/', views.ShowOrder.as_view(), name='order'),
    path('order/add/<item_id>/', views.AddItemToOrder.as_view(), name='add_item_to_order'),
    path('order/delete/<item_id>/', views.DeleteItemFromOrder.as_view(), name='delete_item_from_order'),

    path('buy/<pk>/', views.CreateStripeSession.as_view(), name='create_stripe_session'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
]
