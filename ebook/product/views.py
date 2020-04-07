from django.shortcuts import render
from .models import Category, Product
from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddBookForm
# Create your views here.
# 首页函数
def index(request):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    products_order = products.order_by('-created')[:8]
    return render(request, 'product/index.html',{'categories': categories, 'products': products,'products_order': products_order})
# 商品列表函数
def product_list(request, category_pk):
    context = {}
    categories = Category.objects.all()
    category = get_object_or_404(Category, pk=category_pk)
    products = Product.objects.filter(category_id=category_pk)
    cart_form = CartAddBookForm()
    context['category'] = category
    context['products'] = products
    context['categories'] = categories
    context['cart_form'] = cart_form
    return render(request, 'product/product_list.html', context)
# 商品详情函数
def product_detail(request, product_pk):
    context = {}
    categories = Category.objects.all()
    product = get_object_or_404(Product, pk=product_pk)
    cart_form = CartAddBookForm()
    context['product'] = product
    context['categories'] = categories
    context['cart_form'] = cart_form

    # all_pages_count =product.all().count()
    # #current_page = page_info  # 获取用户当前想要访问的页码
    # if current_page is None:
    #     current_page = 1
    # # 每页显示的记录个数
    # per_page = 3
    # base_url = '/product/product_list/'
    # # 用自定义的分页器生成每页对象
    # page_info = PageInfo(current_page, all_pages_count, per_page, base_url, c_id)
    # # 每页显示的记录的起始位置
    # products = product.all()[page_info.start(): page_info.end()]
    # context['products'] = products
    # context['page_info'] = page_info

    return render(request, 'product/product_details.html', context)