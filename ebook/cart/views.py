from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from product.models import Product
from .cart import Cart
from .forms import CartUpdateBookForm


@require_POST
def cart_add(request, p_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=p_id)
    q = int(request.POST.get('quantity'))
    if request.POST.get("update"):
        update_q = request.POST['update']
    else:
        update_q = False
    cart.add(product=product, quantity=q, update_quantity=update_q)
    return redirect('cart:cart_detail')


def cart_remove(request, p_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=p_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:  # 为 cart 字典里的每一商品项加上更新数量表单键值对
        item['update_quantity_form'] = CartUpdateBookForm(
            initial={'quantity': item['quantity'],
                     'update': True})

    return render(request, 'cart/cart.html', {'cart': cart})
