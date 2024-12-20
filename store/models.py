from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
import json
from django.utils import timezone

# Create your models here.
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  phone = models.CharField(max_length=20, blank=True, null=True)
  dob = models.DateField(blank=True, null=True)
  cart = models.TextField(blank=True, null=True)

  def __str__(self):
    return f'Hồ sơ của {self.user.username}'
  
  def get_cart(self):
    return json.loads(self.cart) if self.cart else {}

  def save_cart(self, cart):
    self.cart = json.dumps(cart)
    self.save()

  def add_to_cart(self, product_id, quantity=1):
    cart = self.get_cart()
    product_id = str(product_id)  # Key phải là chuỗi để tương thích JSON
    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity
    self.save_cart(cart)

  def remove_from_cart(self, product_id):
    """Xóa sản phẩm khỏi giỏ hàng."""
    cart = self.get_cart()
    product_id = str(product_id)
    if product_id in cart:
      del cart[product_id]
      self.save_cart(cart)

  def update_cart(self, product_id, quantity):
    """Cập nhật số lượng sản phẩm trong giỏ hàng."""
    cart = self.get_cart()
    product_id = str(product_id)
    if product_id in cart:
      if quantity > 0:
        cart[product_id] = quantity
      else:
        del cart[product_id]
      self.save_cart(cart)

  def get_cart_items(self):
    """Lấy danh sách sản phẩm trong giỏ hàng."""
    cart = self.get_cart()
    items = []
    for product_id, quantity in cart.items():
      try:
        product = Product.objects.get(id=product_id)
        items.append({'product': product, 'quantity': quantity, 'total_price': product.price * quantity})
      except Product.DoesNotExist:
        continue
    return items

  def cart_item_count(self):
    """Đếm tổng số lượng sản phẩm trong giỏ hàng."""
    cart = self.get_cart()
    return sum(cart.values())
  
def create_profile(sender, instance, created, **kwargs):
  if created:
    user_profile = Profile(user=instance)
    user_profile.save()
post_save.connect(create_profile, sender=User)
  
  
class ShippingAddress(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
  shipping_full_name = models.CharField(max_length=255)
  shipping_phone = models.CharField(max_length=255)
  shipping_address = models.CharField(max_length=255)
  shipping_city = models.CharField(max_length=50)
  shipping_state = models.CharField(max_length=50)
  
  def __str__(self):
    return f'Shipping Address - {self.id}'


class Brand(models.Model):
  name = models.CharField(max_length=30)
  slug = models.SlugField(max_length=50, blank=True, null=True)
  
  def __str__(self):
    return self.name

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = f'nuoc-hoa-chinh-hang-thuong-hieu-{slugify(self.name)}'
    super(Brand, self).save(*args, **kwargs)
  
 
class Gender(models.Model):
  name = models.CharField(max_length=30)
  slug = models.SlugField(max_length=30)
  
  def __str__(self):
    return self.name  
    

class Product(models.Model):
  title = models.CharField(max_length=200)
  slug = models.SlugField(max_length=200, blank=True, null=True)
  brand = models.ForeignKey(Brand, null=True, on_delete=models.SET_NULL)
  gender = models.ForeignKey(Gender, null=True, on_delete=models.SET_NULL)
  origin = models.CharField(max_length=50)
  volume = models.IntegerField()
  description = models.TextField()
  img1 = models.ImageField(upload_to='')
  img2 = models.ImageField(upload_to='')
  img3 = models.ImageField(upload_to='')
  img4 = models.ImageField(upload_to='')
  price = models.DecimalField(max_digits=10, decimal_places=0)
  quantity = models.IntegerField(default=20)
  q_purchase = models.IntegerField(default=0)
  stock = models.IntegerField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def save(self, *args, **kwargs):
    self.stock = self.quantity - self.q_purchase
    if not self.slug:
      self.slug = slugify(self.title)
    super(Product, self).save(*args, **kwargs)
    
  def __str__(self):
    return self.title


class Order(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
  full_name = models.CharField(max_length=250)
  phone = models.CharField(max_length=250)
  shipping_address = models.TextField(max_length=15000)
  amount_paid= models.DecimalField(max_digits=10, decimal_places=0)
  payment_method = models.CharField(max_length=50, choices=[('Chuyển khoản qua ngân hàng', 'Chuyển khoản qua ngân hàng'), ('Thanh toán khi giao hàng', 'Thanh toán khi giao hàng')])
  status = models.CharField(max_length=50, choices=[('Đang giao', 'Đang giao'), ('Đã giao', 'Đã giao')], default='Đang giao')
  created_at = models.DateTimeField(auto_now_add=True)
  date_shipped = models.DateTimeField(blank=True, null=True)
  
  def __str__(self):
    return f'Order - {self.id}'
  
  def save(self, *args, **kwargs):
    if self.status == 'Đã giao' and not self.date_shipped:
      self.date_shipped = timezone.now()
    elif self.status == 'Đang giao':
      self.date_shipped = None
    super(Order, self).save(*args, **kwargs)


class OrderItem(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveBigIntegerField(default=1)
  price = models.DecimalField(max_digits=10, decimal_places=0)
  
  def __str__(self):
    return f'Order Item - {self.id}'
  

class Review(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  order_item = models.OneToOneField(OrderItem, on_delete=models.SET_NULL, null=True)
  star = models.IntegerField()
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f"{self.user.username}'s review of the {self.order_item}"
  

class Contact(models.Model):
  full_name = models.CharField(max_length=200)
  email = models.EmailField(max_length=250)
  content = models.TextField()
  
  def __str__(self):
    return f'Message from {self.full_name}'