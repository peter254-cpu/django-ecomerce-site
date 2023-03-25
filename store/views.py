from django.shortcuts import render
from django.http import JsonResponse
import datetime
from .models import *
import json
from .utils import cookieCart,cartData, guestOrder 
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, 'store/profile.html')

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    
    products = Product.objects.all()
    context = {'products': products,'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context ={'order': order, 'cartItems': cartItems, 'items': items}
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)
 # a view to update the backend
def UpdateItem(request):
    data = json.loads(request.body)
    action = data['action']
    productId = data['productId']
    print('Action:', action)
    print('product:', productId)

    #crreate or update order item
    #going to use productId to get the product and
    # get_or_create in order to work with 
    # status false coz the complete attribute means
    # it is an open cart that we can add to

    customer = request.user.customer
    product = Product.objects.get(id = productId)
    order , customer =Order.objects.get_or_create(customer=customer, complete = False)
    orderItem,created = OrderItem.objects.get_or_create(order = order, product = product)

    #finally action logic we need to add update create an item in to the cart
    if action == "add":
        orderItem.quantity=(orderItem.quantity + 1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()
    return JsonResponse('item was added', safe=False)
def processorder(request):
    #logic to create a transaction id using datestamp
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer, complete = False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
     
    if total == float(order.get_cart_total):
        order.complete = True
    order.save()
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )
    return JsonResponse("payment complete!", safe=False)
