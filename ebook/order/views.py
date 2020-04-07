from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .models import OrderItem, Order
from account.models import UserProfile
from product.models import Product
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import View
from datetime import datetime
from django.db import transaction
from cart.cart import Cart
from .models import OrderItem, Order
from account.models import UserProfile
from product.models import Product
from alipay import AliPay
from django.views.decorators.csrf import csrf_exempt

# 生成订单
# order/order_created
class OrderCreatedView(View):
    @transaction.atomic()
    def get(self, request):

        context = {}
        # 获取当前用户购物车
        cart = Cart(request)
        tran_id = transaction.savepoint()  # 创建事务的保存点
        # 创建订单
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(request.user.pk)
        order = Order.objects.create(orderId=order_id, user=request.user, totalMoney=cart.get_total_price(),
                                     totalNum=len(cart))
        # 遍历购物车中的商品，创建订单明细
        for item in cart:
            product = Product.objects.select_for_update().get(id__exact=item['product'].id)  # 悲观锁
            product = Product.objects.get(id__exact=item['product'].id)
            if product.stock >= item['quantity']:
                product.stock -= item['quantity']  # 减库存
                product.available = False  # 商品改为不可用
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                 quantity=item['quantity'])
                Product.objects.filter(id__exact=item['product'].id).update(stock=product.stock)  # 更新库存

            else:
                transaction.savepoint_rollback(tran_id)  # 回滚到保存点
                return redirect('/cart/')
        cart.clear()
        userprofile = UserProfile.objects.filter(belong_to=request.user)[0]  # 这里要注意，使用 objects 管理器进行筛选后的
        # 结果是一个集合（QuerySet），要集合中的某一个元素需要加上索引号
        request.session['order_id'] = order.orderId
        request.session['total_money'] = str(order.totalMoney)
        context['order'] = order
        context['userprofile'] = userprofile
        transaction.savepoint_commit(tran_id)  # 提交事务
        return render(request, 'order/order_created.html', context)

# 提交订单
# order/order_create/
class OrderCreateView(View):
    def get(self, request):

        context = {}
        cart = Cart(request)
        # 如果购物车不空，检查用户是否填写了个人信息，没有用户信息则需要重定向到个人信息页面
        if len(cart) != 0:  # 购物车里有商品,len 函数是 cart 类中定义的__len__函数
            user = UserProfile.objects.filter(belong_to=request.user).exists()  # 这里要注意，使用 objects 管理器进行筛选后的
            # 结果是一个集合（QuerySet），要集合是的某一个元素需要加上索引号
            if user is False:
                return redirect('%s?next=%s' % ('/account/info/', request.path))  # redirect 中使用 url 格式的参数
            else:
                userprofile = UserProfile.objects.get(belong_to=request.user)
                context['userprofile'] = userprofile
                context['cart'] = cart
                return render(request, 'order/order_create.html', context)
        else:

            context['error'] = '购物车为空！'
        return redirect('cart/', context)


# 支付函数
def ali():
    # 商户 app_id
    app_id = "2016101700708422" # 复制来自支付宝生成的 id
    # 服务器异步通知页面路径 需 http: // 格式的完整路径，不能加?id = 123这类自定义参数，必须外网可以正常访问
    # 对于 PC 网站支付的交易，在用户支付完成之后，支付宝会根据 API 中商户传入的 notify_url，通过 POST 请求的形式将支付结果作为参数通知到商户系统
    # 发 post 请求
    notify_url = "http://127.0.0.1:8000/order/page1/"
    return_url = "http://127.0.0.1:8000/order/return_pay/"
    merchant_private_key_path = "keys/pri" # 设置公钥和私钥的地址，文件上下两行 begin 和 end 是必须的，公钥就放在第二行。
    alipay_public_key_path = "keys/pub"
    alipay = AliPay(
        appid=app_id,
        app_notify_url=notify_url,
        app_private_key_path=merchant_private_key_path,
        alipay_public_key_path=alipay_public_key_path, # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        sign_type="RSA2",
        debug=True, # 默认 False,

    )
    return alipay

# 去支付，调用支付宝 API，传递相应参数
# order/pay/
class OrderPayView(View):
    @csrf_exempt
    def get(self, request, order_id):
        if order_id == 0:
            order_id = request.session['order_id']
            print(order_id)
            money = float(request.session['total_money'])
        else:
            money = float(Order.objects.get(pk=order_id).totalMoney)
        alipay = ali()
        # 生成支付的 url
        query_params = alipay.api_alipay_trade_page_pay(
            subject="书", # 商品简单描述
            out_trade_no=order_id, # 商户订单号
            total_amount=money, # 交易金额(单位: 元 保留俩位小数)
            return_url="http://127.0.0.1:8000/order/return_pay/"
        )
        pay_url ="https://openapi.alipaydev.com/gateway.do?{}".format(query_params)
    # 支付宝网关链接，去掉 dev 就是生产环境了。
        return redirect(pay_url)
    # 沙箱支付完成后的重定向返回页面处理
@csrf_exempt
def return_pay(request):
    alipay = ali()
    if return_verify(request):
# 商户网站支付单号
        out_trade_no = request.GET.get('out_trade_no')
        print(out_trade_no)
# 修改支付单的支付状态
#         while True:
#             paid_order = Order.objects.filter(orderId=out_trade_no)
#             if paid_order:
#                 paid_order[0].paid = True # 将订单状态修改为已支付
#                 paid_order[0].save()
#                 return redirect('account:userorder')
#             else:
#                 response = alipay.api_alipay_trade_query(out_trade_no)
#                 code = response.get('code')
#                 if code == '10000' and response.get('trade_status') =='TRADE_SUCCESS':# 支付成功
#                     paid_order[0].paid = True # 将订单状态修改为已支付  # 更新订单状态
#                     paid_order[0].save()
#                 elif code == '40004' or (code == '10000' and response.get('trade_status') == 'WAIT_BUYER_PAY'):
#                     import time
#                     time.sleep(5)
#                     continue
#                 else:
#                     # 支付出错
#                     print(code)
#             return redirect('account:userorder')
        paid_order = Order.objects.filter(orderId=out_trade_no)

        paid_order[0].paid = True # 将订单状态修改为已支付  # 更新订单状态
        paid_order[0].save()
        return redirect('account:userorder')


    # else:
    #     print("支付宝签名验证失败")
# 支付宝同步通知签名验证，防止黑客攻击
def return_verify(request):
    alipay = ali()
# 获取支付宝同步通知传来的参数数据，转换为一个字典
    data = {x: request.GET.get(x) for x in request.GET.keys()}
    signature = data.pop("sign")
# 签名验证
    success = alipay.verify(data, signature)
    if success:
        return True
    else:
        return False








