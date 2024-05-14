from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.

def cart_summary(request):
    #getting the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities=cart.get_quants
    totals = cart.cart_total()

    return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities":quantities, "totals":totals})


def cart_add(request):
    #cart
    cart = Cart(request)
    #test for POST
    if request.POST.get('action') == 'post':
        #stuff
        product_id = int(request.POST.get('product_id'))
        product_quant = int(request.POST.get('product_quant'))


        #lookup product in the database
        product = get_object_or_404(Product, id=product_id)

        #save to session
        cart.add(product=product, quantity=product_quant)

        #cart quantity
        cart_quantity = cart.__len__()



        #response = JsonResponse({'Product Name:': product.name})
        response = JsonResponse({'quant': cart_quantity})
        messages.success(request,("Product you selected was added to the cart"))
        return response

   

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':

        product_id = int(request.POST.get('product_id'))
        #call delete in cart
        cart.delete(product=product_id)

        response = JsonResponse({ 'product':product_id })
        messages.success(request,("You Remove the Product"))
        return response 
        # return redirect ('cart_summary')




def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':

        product_id = int(request.POST.get('product_id'))
        product_quant = int(request.POST.get('product_quant'))

        cart.update(product=product_id, quantity=product_quant)

        response = JsonResponse({ 'quant':product_quant })
        messages.success(request,("Product was updated"))
        return response 
        # return redirect ('cart_summary')

