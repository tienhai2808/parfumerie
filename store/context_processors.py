from .models import Profile, Brand


def cart_item_count(request):
  if request.user.is_authenticated:
    profile = Profile.objects.filter(user=request.user).first()
    if profile:
      return {'cart_item_count': profile.cart_item_count()}
  return {'cart_item_count': 0}

def all_brand(request):
  brands = Brand.objects.all()
  return {'brands': brands}