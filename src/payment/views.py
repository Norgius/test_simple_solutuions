from typing import Any

import stripe
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.http.request import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, View, DetailView
from django.utils import timezone
from django.conf import settings

from payment.models import Item, Order

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateStripeSession(View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponseRedirect:
        order = Order.objects.prefetch_related('items').get(id=pk)
        line_items = []
        for item in order.items.all():
            line_items.append(
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
            )
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=settings.PAYMENT_SUCCESS_URL,
                cancel_url=settings.PAYMENT_CANCEL_URL,
            )
        except Exception:
            return redirect('payment:cancel')
        return redirect(checkout_session.url)


class ShowItem(DetailView):
    model = Item
    template_name = 'item_details.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = f"Товар: {context.get('item').name}"
        return context


class ShowOrder(ListView):
    template_name = 'order.html'
    context_object_name = 'order'
    extra_context = {
        'title': 'Ваш заказ',
    }

    def get_queryset(self) -> QuerySet[Any]:
        return Order.objects.calculate_total_cost().receive_assembled_order()


class AddItemToOrder(View):
    def post(self, request: HttpRequest, item_id: int) -> HttpResponseRedirect | HttpResponse:
        item = get_object_or_404(Item, id=item_id)
        order: Order = Order.objects.receive_assembled_order()
        if order and item not in order.items.all():
            order.items.add(item)
            order.save()
        elif order and item in order.items.all():
            return render(
                request,
                'item_details.html',
                context={'pk': item.id, 'item': item, 'order_id': order.id})
        else:
            order = Order.objects.create()
            order.items.set([item])
            order.save()
        return redirect(reverse('payment:order', kwargs={'pk': order.id}))


class DeleteItemFromOrder(View):
    def post(self, request: HttpRequest, item_id: int) -> HttpResponseRedirect:
        order: Order = Order.objects.receive_assembled_order()
        item = get_object_or_404(Item, id=item_id)
        order.items.remove(item)
        order.save()
        return redirect(reverse('payment:order', kwargs={'pk': order.id}))


class ShowItems(ListView):
    template_name = 'index.html'
    context_object_name = 'items'

    def get_queryset(self) -> QuerySet[Any]:
        return Item.objects.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        order = Order.objects.receive_assembled_order()
        context['order'] = order
        return context


class SuccessView(TemplateView):
    template_name = "successful_payment.html"


class CancelView(TemplateView):
    template_name = "canceled_payment.html"


@csrf_exempt
def stripe_webhook(request: HttpRequest) -> HttpResponse:
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        order = Order.objects.filter(status=Order.OrderStatus.IN_ASSEMBLY).first()
        order.status = Order.OrderStatus.PAID
        order.paid_at = timezone.now()
        order.save()

    return HttpResponse(status=200)
