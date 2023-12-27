from django.shortcuts import redirect
from django.urls import reverse
from django.http.request import HttpRequest
from django.utils import timezone
from django.db.models import Q
from django.views.generic import View

from discount.models import Discount
from discount.forms import DiscountForm
from payment.models import Order


class CheckDiscount(View):
    def post(self, request: HttpRequest):
        form = DiscountForm(request.POST)
        order = Order.objects.filter(status=Order.OrderStatus.IN_ASSEMBLY).first()
        if form.is_valid():
            code = form.cleaned_data['code'].strip()
            now = timezone.now()
            try:
                discount = Discount.objects.get(
                    Q(valid_to__gte=now) | Q(valid_to=None),
                    code=code,
                    creation_time__lte=now,
                )
                request.session['discount_id'] = discount.id
            except Discount.DoesNotExist:
                request.session['discount_id'] = 'not_active'
        return redirect(reverse('payment:order', kwargs={'pk': order.id}))
