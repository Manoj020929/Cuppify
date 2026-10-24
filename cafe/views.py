import json

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import Customer, MenuItem, Order, OrderItem


def get_customer(request):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return None
    return Customer.objects.filter(id=customer_id).first()


def login_view(request):
    if get_customer(request):
        return redirect("menu")

    error = ""
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()

        if not name:
            error = "Please enter your name."
        elif not (phone.isdigit() and len(phone) == 10):
            error = "Phone number must be exactly 10 digits."
        else:
            customer, created = Customer.objects.get_or_create(
                phone=phone, defaults={"name": name}
            )
            request.session["customer_id"] = customer.id
            return redirect("menu")

    return render(request, "cafe/login.html", {"error": error})


def menu_view(request):
    customer = get_customer(request)
    if customer is None:
        request.session.flush()
        return redirect("login")

    items = MenuItem.objects.filter(is_available=True)
    orders = customer.orders.order_by("-id").prefetch_related("items")[:10]
    return render(
        request,
        "cafe/menu.html",
        {"customer": customer, "items": items, "orders": orders},
    )


@require_POST
def place_order_view(request):
    customer = get_customer(request)
    if customer is None:
        return JsonResponse({"error": "Please log in again."}, status=401)

    try:
        data = json.loads(request.body)
    except ValueError:
        return JsonResponse({"error": "Bad request."}, status=400)

    cart = data.get("items")
    if not isinstance(cart, list) or not cart:
        return JsonResponse({"error": "No item was selected."}, status=400)
    if len(cart) > 30:
        return JsonResponse({"error": "Too many items in one order."}, status=400)

    lines = []
    total = 0
    for entry in cart:
        try:
            item_id = int(entry.get("id"))
            qty = int(entry.get("qty"))
        except (TypeError, ValueError, AttributeError):
            return JsonResponse({"error": "Bad item in the order."}, status=400)

        if qty < 1 or qty > 20:
            return JsonResponse({"error": "Quantity must be 1 to 20."}, status=400)

        item = MenuItem.objects.filter(id=item_id, is_available=True).first()
        if item is None:
            return JsonResponse({"error": "An item is not on the menu."}, status=400)

        lines.append((item, qty))
        total += item.price * qty  # the server decides the price

    with transaction.atomic():
        order = Order.objects.create(customer=customer, total=total)
        OrderItem.objects.bulk_create(
            [
                OrderItem(order=order, name=item.name, price=item.price, quantity=qty)
                for item, qty in lines
            ]
        )

    return JsonResponse({"id": order.id, "total": total}, status=201)


def logout_view(request):
    request.session.flush()
    return redirect("login")