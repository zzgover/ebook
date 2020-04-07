from django.db import models
from product.models import Product
from django.contrib.auth.models import User
# Create your models here.


class Order(models.Model):
    orderId = models.CharField(max_length=128, primary_key=True)
    user = models.ForeignKey(User,related_name='user',on_delete=models.CASCADE)
    totalNum = models.PositiveIntegerField(default=1)
    totalMoney = models.DecimalField(max_digits=10, decimal_places=2)
    submitDate = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    consign = models.BooleanField(default=False)  # 是否发货
    consignDate = models.DateField(null=True)  # 发货日期
    class Meta:
        ordering = ('-submitDate',)
    def __str__(self):
        return 'Order {}'.format(self.id)


class OrderItem(models.Model):  # 详细订单
    order = models.ForeignKey(Order, related_name='orderItems', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_order', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):

        return 'OrderItems {}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity