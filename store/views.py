from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store.html', context)


def products(request, pk):
    data = cartData(request)
    cartItems = data['cartItems']

    product = Product.objects.get(id=pk)
    category = Category.objects.all()
    context = {'product': product,
               'cartItems': cartItems, 'category': category}
    return render(request, 'product.html', context)


def category(request, cat):
    data = cartData(request)
    cartItems = data['cartItems']

    cat = cat.replace('-', ' ')  # replace hyphens with spaces
    # grab category from the url
    try:
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category)
        context = {'products': products,
                   'category': category, 'cartItems': cartItems}
        return render(request, 'category.html', context)
    except:
        messages.success(request, ('That category does not exist!'))
        return redirect('store')


def item_search(request):
    query = request.GET.get('q')

    # Search products by name or tags
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(tags__name__icontains=query)
    ).distinct()

    context = {'products': products, 'query': query}
    return render(request, 'search_results.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have been logged in!'))
            return redirect('/')
        else:
            messages.success(request, ('There was an error, please try again!'))
            return redirect('login/')
    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out!'))
    return redirect('/')


def wishlist(request):
    context = {}
    return render(request, 'wishlist.html', context)


def updateWishlist(request):
    pass


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'cart.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity) + 1
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity) - 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item added', safe=False)


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'checkout.html', context)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingDetails.objects.create(
            customer=customer,
            order=order,
            address_level_1=data['shipping']['address_level_1'],
            address_level_2=data['shipping']['address_level_2'],
            country=data['shipping']['country'],
            state=data['shipping']['state'],
            city=data['shipping']['city'],
            pincode=data['shipping']['pincode'],
            contact=data['shipping']['contact']
        )

    return JsonResponse('Transaction Successful!', safe=False)


def testing(request):
    return render(request, 'test.html')


# def userProfile(request, slug):
#     customer = get_object_or_404(Customer, user__username=slug)
#     return render(request, 'profile.html', {'customer': customer})


# view to remove item form wishlist or cart
# def removeProduct(request, product_id):
#     # data = json.loads(request.body)
#     # productId = data['productId']
#     # Assuming you have a Product model
#     product = get_object_or_404(Product, id=product_id)

#     # Delete the product
#     product.delete()

#     return JsonResponse({'message': 'Product removed successfully'})
