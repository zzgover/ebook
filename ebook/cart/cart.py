from decimal import Decimal
from django.conf import settings
from product.models import Product


class Cart(object):
    def __init__(self, request):  # request 作为参数

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart



    #添加or更新
    def add(self, product, quantity=1, update_quantity=False):

        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):

        self.session[settings.CART_SESSION_ID] = self.cart
    # session.modified 标记为 True 是为了告诉 Django，session 已经被改动，需要将它保存起来
        self.session.modified = True

    def remove(self, product):

        product_id = str(product.id)
        if product_id in self.cart:

            del self.cart[product_id]
            self.save()

    def __iter__(self):

        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)]['product'] = product
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):

        sum_ = 0
        for item in self.cart.values():
            sum_ = sum_ + item['quantity']
        return sum_

    def get_total_price(self):

        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):

        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
