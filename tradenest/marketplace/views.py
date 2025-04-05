from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from django.contrib import messages
from .models import Product, Cart, Favorite


def product_list(request):
    products = Product.objects.all()
    return render(request, 'marketplace/product_list.html', {'products': products})

def marketplace_view(request):
    products = Product.objects.all()
    return render(request, "marketplace/marketplace.html", {"products": products})

@login_required
def buy_or_sell_view(request):
    return render(request, "marketplace/buy_or_sell.html")

@login_required
def sell_view(request):
    return render(request, 'marketplace/sell.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('buy_or_sell')  # go to Buy or Sell after login
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect("marketplace")
    else:
        form = ProductForm()
    return render(request, "marketplace/add_product.html", {"form": form})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Cart.objects.create(user=request.user, product=product)
    return redirect("cart")

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, "marketplace/cart.html", {"cart_items": cart_items})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'marketplace/product_detail.html', {'product': product})

@login_required
def checkout(request):
    return render(request, 'marketplace/checkout.html')

from django.contrib.auth.forms import UserCreationForm

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. You can now log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user  # Assign the logged-in user as the seller
            product.save()  # Save the product to the database
            return redirect('marketplace')  # Redirect to the marketplace after successful submission
    else:
        form = ProductForm()

    return render(request, 'marketplace/add_product.html', {'form': form})