from django.shortcuts import render, redirect
from django.contrib import auth, messages
from .forms import *
from .models import *
import json
from django.utils import timezone
from datetime import timedelta
 
# Create your views here.
def home(request):
  male_perfumes = Product.objects.filter(gender__name='Nước hoa Nam')[:4]
  female_perfumes = Product.objects.filter(gender__name='Nước hoa Nữ')[:4]
  unisex_perfumes = Product.objects.filter(gender__name='Nước hoa Unisex')[:4]
  return render(request, 'home.html', {'male_perfumes': male_perfumes, 'female_perfumes': female_perfumes, 'unisex_perfumes': unisex_perfumes})

def register(request):
  form = RegisterForm(request.POST or None)
  if request.POST:
    if form.is_valid():
      auth.login(request, form.save())
      return redirect('home')
  return render(request, 'register.html', {'form': form})

def login(request):
  form = LoginForm(data=request.POST or None)
  if request.POST:
    if form.is_valid():
      auth.login(request, form.get_user())
      return redirect('home')
  return render(request, 'login.html', {'form': form})

def logout(request):
  auth.logout(request)
  return redirect('/')

def account(request):
  if request.user.is_authenticated:
    user = request.user
    form_user = UpdateUserForm(request.POST or None, instance=user)
    form_profile = UpdateProfileForm(request.POST or None, instance=user.profile)
    form_address = ShippingAddressForm(request.POST or None)
    if request.POST:
      id_address = request.POST.get('id_address', '')
      if id_address:
        ShippingAddress.objects.get(id=id_address).delete()
        messages.success(request, 'Xóa địa chỉ thành công')
        return redirect('account')
      if form_address.is_valid():
        new_address = form_address.save(False)
        new_address.user = user
        new_address.save()
        messages.success(request, 'Thêm địa chỉ thành công')
        return redirect('account')
      if form_user.is_valid() and form_profile.is_valid():
        form_user.save()
        form_profile.save()
        messages.success(request, 'Cập nhật thông tin thành công')
        return redirect('account')
    return render(request, 'account.html', {'user': user, 'form_address': form_address, 'form_user': form_user, 'form_profile': form_profile})
  else:
    return redirect('login')
  
def category(request, slug_cat):
  try:
    gender = Gender.objects.get(slug=slug_cat)
  except Gender.DoesNotExist:
    gender = None
  try:
    brand = Brand.objects.get(slug=slug_cat)
  except Brand.DoesNotExist:
    brand = None
  if not gender and not brand:
    return redirect('home')
  if gender or brand:
    if gender:
      cat = gender
      cat_type = 'Gender'
      perfumes = Product.objects.filter(gender=gender).order_by('-created_at')
      orderby = request.GET.get('orderby', '')
      if orderby:
        if orderby == 'high_purchase':
          perfumes = perfumes.order_by('-q_purchase')
        if orderby == 'low_price':
          perfumes = perfumes.order_by('price')
        if orderby == 'high_price':
          perfumes = perfumes.order_by('-price')
        if orderby == 'new_product':
          perfumes = perfumes.order_by('-created_at')
    if brand:
      cat = brand
      cat_type = 'Brand'
      perfumes = Product.objects.filter(brand=brand).order_by('-created_at')
      orderby = request.GET.get('orderby', '')
      if orderby:
        if orderby == 'high_purchase':
          perfumes = perfumes.order_by('-q_purchase')
        if orderby == 'low_price':
          perfumes = perfumes.order_by('price')
        if orderby == 'high_price':
          perfumes = perfumes.order_by('-price')
        if orderby == 'new_product':
          perfumes = perfumes.order_by('created_at')
    return render(request, 'category.html', {'cat': cat, 'perfumes': perfumes, 'cat_type': cat_type, 'orderby': orderby})
  
def product_detail(request, slug_pro):
  try:
    perfume = Product.objects.get(slug=slug_pro)
    reviews = Review.objects.filter(order_item__product=perfume)
    if request.user.is_authenticated:
      orderitems = OrderItem.objects.filter(order__user=request.user, order__status='Đã giao', product=perfume).exclude(review__isnull=False)
      if orderitems.exists():
        perfume.allow_review = True
        if request.POST:
          form = ReviewForm(request.POST)
          if form.is_valid():
            review = form.save(False)
            review.user = request.user
            review.order_item = orderitems.first()
            review.save()
            messages.success(request, 'Gửi đánh giá thành công')
            return redirect('product-detail', perfume.slug)
    if request.POST:
      action = request.POST.get('action')
      quantity = request.POST.get('quantity')
      profile = request.user.profile
      profile.add_to_cart(product_id=perfume.id, quantity=int(quantity))
      return redirect('product-detail', perfume.slug) if action == 'add-cart' else redirect('checkout', request.user)
    return render(request, 'product_detail.html', {'perfume': perfume, 'reviews': reviews})
  except Product.DoesNotExist:
    return redirect('home')
  
def cart(request):
  if request.user.is_authenticated:
    profile = request.user.profile
    cart_items = profile.get_cart_items()
    total_cart = sum([int(item['total_price']) for item in cart_items])    
    if request.POST:
      delete_id = request.POST.get('delete', '')
      if delete_id:
        profile.remove_from_cart(delete_id)
        messages.success(request, 'Đã xóa sản phẩm khỏi giỏ hàng')
        return redirect('cart')
      try:
        data = json.loads(request.POST.get('update', '[]'))
        for item in data:
          product_id = item.get('product_id')
          quantity = int(item.get('quantity', 1))
          profile.update_cart(product_id, quantity)
        messages.success(request, 'Đã cập nhật thay đổi')
        return redirect('cart')
      except Exception as e:
        messages.success(request, f"Error: {e}")
        return redirect
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_cart': total_cart})
  else:
    return redirect('login')
  
def checkout(request, username):
  if request.user.username == username and request.user.profile.cart != None:
    profile = request.user.profile
    cart_items = profile.get_cart_items()
    total_cart = sum([int(item['total_price']) for item in cart_items])
    addresses = request.user.addresses.all()
    if request.POST:
      id_address = request.POST.get('id_address', '')
      method = request.POST.get('payment_method', '')
      payment_method = 'Chuyển khoản qua ngân hàng' if method=='bank' else 'Thanh toán khi nhận hàng'
      if id_address:
        shipping = addresses.get(id=id_address)
        shipping_address = f'{shipping.shipping_address} - {shipping.shipping_city} - {shipping.shipping_state}'
        full_name = shipping.shipping_full_name
        phone = shipping.shipping_phone
      else:
        full_name = request.POST.get('full_name', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        shipping_address = f'{address} - {city} - {state}'
      order = Order.objects.create(user=request.user, 
                                   full_name=full_name, 
                                   phone=phone, 
                                   shipping_address=shipping_address, 
                                   amount_paid=total_cart,
                                   payment_method=payment_method)
      for item in cart_items:
        product = item['product']
        quantity = item['quantity'] 
        total_price = item['total_price']
        OrderItem.objects.create(order=order, product=product, quantity=quantity, price=total_price)
        product.q_purchase += quantity
        product.save()
      profile.cart = ''
      profile.save()
      return redirect('checkout-success')
    return render(request, 'checkout.html', {'cart_items': cart_items, 
                                             'total_cart': total_cart, 
                                             'addresses': addresses})
  else:
    return redirect('home')
  
def checkout_success(request):
  if request.user.is_authenticated:
    recent_order = request.user.orders.filter(created_at__gte=timezone.now() - timedelta(seconds=30)).order_by('-created_at').first()
    if recent_order:
      return render(request, 'checkout_success.html', {'recent_order': recent_order})
    else:
      return redirect('home')
  else: 
    return redirect('home')
  
def order_detail(request, id_order):
  try:
    order = Order.objects.get(id=id_order)
    return render(request, 'order_detail.html', {'order': order})
  except Order.DoesNotExist:
    return redirect('home')
  
def search(request):
  query = request.GET.get('query', '')
  if query:
    perfumes = Product.objects.filter(title__icontains=query)
    if not perfumes:
      h3 = 'Không tìm thấy kết quả nào với từ khóa'
    else:
      h3 = f'Có {perfumes.count()} kết quả tìm kiếm phù hợp'
  else:
    perfumes = None
    h3 = 'Nhập từ khóa để tìm kiếm sản phẩm'
  return render(request, 'search.html', {'perfumes': perfumes, 'query': query, 'h3': h3})

def contact(request):
  if request.POST:
    form = ContactForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'Đã gửi tin nhắn tới cửa hàng')
      return redirect('home')
  return render(request, 'contact.html')