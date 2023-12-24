from typing import Any
import stripe
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, View, DetailView
from django.conf import settings

from payment.models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateStripeSession(View):
    def post(self, request, pk):
        item = get_object_or_404(Item, id=pk)
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': int(item.price),
                            'product_data': {
                                'name': item.name,
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=settings.PAYMENT_SUCCESS_URL,
                cancel_url=settings.PAYMENT_CANCEL_URL,
            )
        except Exception as e:
            raise e
            return redirect('payment:cancel')
        return redirect(checkout_session.url)


class ShowItem(DetailView):
    model = Item
    template_name = 'item_details.html'
    context_object_name = 'item'
    extra_context = {
        'title': 'Главная страница',
    }

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = f"Товар: {context.get('item').name}"
        return context


class ShowItems(ListView):
    model = Item
    template_name = 'index.html'
    context_object_name = 'items'
    extra_context = {
        'title': 'Главная страница',
    }


class SuccessView(TemplateView):
    template_name = "successful_payment.html"


class CancelView(TemplateView):
    template_name = "canceled_payment.html"
