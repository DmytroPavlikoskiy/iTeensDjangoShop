from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
# <<<<<<< HEAD
from django.http import HttpResponse
from products.models import Product, Category, ProductImage
# =======
from products.models import Product
# >>>>>>> origin/checkout
from card.models import Order, OrderItem
from django.http import JsonResponse
from card.cart import HybridCart
from payment.utils import get_liqpay_context
# <<<<<<< HEAD
from users.forms import UserRegistrationForm
import json
# =======
# >>>>>>> origin/checkout

# @require_POST
# def cart_add(request, product_id):
#     cart = HybridCart(request)
#     product = get_object_or_404(Product, id=product_id)
#     cart.add(product=product)
#     messages.success(request, "Товар добавлен в корзину!")
#     # редирект без namespace
#     return redirect('product_list')


# @require_POST
# def cart_add(request, product_id):
#     cart = HybridCart(request)
#     product = get_object_or_404(Product, id=product_id)
#     cart.add(product=product)
#     messages.success(request, "Товар добавлен в корзину!")
#     # редирект без namespace
#     return redirect('product_list')
@require_POST
def cart_add(request, product_id):
    cart = HybridCart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    
    # Замість messages і redirect повертаємо JSON
    return JsonResponse({
        'success': True,
        'cart_total_items': len(cart),  # Кількість товарів у кошику
        'message': "Товар додано!"
    })


@require_POST
def cart_add_with_quantity(request, product_id):
    cart = HybridCart(request)
    product = get_object_or_404(Product, id=product_id)

    try:
        data = json.loads(request.body.decode('utf-8'))
        # Перетворюємо в int і перевіряємо на адекватність
        quantity = int(data.get("quantity", 1))
        
        if quantity <= 0:
            return JsonResponse({
                'success': False,
                'message': "Кількість має бути більшою за 0!"
            }, status=400) # Повертаємо 400 помилку для некоректних даних
            
    except (json.JSONDecodeError, ValueError, TypeError):
        return JsonResponse({'success': False, 'message': 'Invalid data'}, status=400)

    # Важливо: перевір, щоб в HybridCart метод add приймав quantity
    cart.add(product=product, quantity=quantity)
    
    return JsonResponse({
        'success': True,
        'cart_total_items': len(cart),
        'message': f"Додано {quantity} шт."
    })

@require_POST
def card_add_product_detail(request):
    if request.method == "POST":
        data_json = json.loads(request.body)
        product_id = data_json.get("product_id")
        quantity = data_json.get("quantity")

        #Зробити валідацію

        cart = HybridCart(request)
        try:
            product = Product.objects.filter(id=product_id, available=True)
        except Exception as ex:
            print(ex)
        cart.add(product=product, quantity=quantity)
        messages.success(request, "Товар добавлен в корзину!")
        return redirect('product_detail')
    else:
        return HttpResponse(403, "forbidden")

def cart_remove(request, product_id):
    cart = HybridCart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


def cart_detail(request):
    cart = HybridCart(request)
    
    cart_product_ids = [item['product'].id for item in cart]
    cart_categories = Product.objects.filter(id__in=cart_product_ids).values_list('category', flat=True)
    
    recommendations = Product.objects.filter(
        category__in=cart_categories,
        available=True
    ).exclude(id__in=cart_product_ids).order_by('?')[:4]
    
    return render(request, 'stors/cart_d.html', {
        'cart': cart,
        'cart_total_items': len(cart),
        'recommendations': recommendations
    })
