from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .form import BookForm,Registeration,LoginForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from.models import Book,Cart
from django.urls import reverse
from django.conf import settings
import stripe
stripe.api_key=settings.STRIPE_SECRET_KEY

# Create your views here.

def home(request):
    # return HttpResponse ("<h1>WELCOME TO APP1 HOME</h1>")
    return render(request,'app1/home.html')

def about(request):
    return render(request,'app1/about.html')

def contact(request):
    return render(request,'app1/contact.html')

@login_required
def view_table(request):
    a=Book.objects.all()
    return render(request,'app1/view.html',{"table":a})

@login_required
def createbook(request):
    a=BookForm(request.POST or None, request.FILES or None)
    if a.is_valid():
        a.save()
        return redirect('Table view')
    return render(request,'app1/createbook.html',{'form':a})

@login_required
def update_book(request,id):
    form=Book.objects.get(id=id)
    a=BookForm(request.POST or None,request.FILES or None, instance=form)
    if a.is_valid():
        a.save()
        return redirect('Table view')
    return render(request,'app1/update.html',{'update':a})

@login_required
def delete_book(request,id):
    a=Book.objects.get(id=id)
    if request.method=="POST":
     a.delete()
     return redirect('Table view')
    return render(request,'app1/delete.html',{'dlt':a})

def user_creation(request):
    a=Registeration(request.POST or None)
    if request.method=='POST' and a.is_valid():
        a.save()
        return redirect ('Table view')
    return render(request,'app1/regform.html',{'form':a})

def loginform(request):
    a=LoginForm(request, data=request.POST or None)
    if request.method=='POST' and a.is_valid():
         user=a.get_user()
         login(request,user)
         return redirect('Table view')
    return render(request,'app1/log.html',{'form':a})

def logout_view(request):
    logout(request)
    return redirect('log')

def view_cart(request):
    a=Cart.objects.filter(user=request.user)
    return render(request,'app1/cart.html',{'cart':a})

def Addcart(request,bookid):
    a=Book.objects.get(id=bookid)
    cart_items,created=Cart.objects.get_or_create(book=a, user=request.user)
    if not created:
        cart_items.quantity+=1
        cart_items.save()
    return redirect('v')

# def delete_view(request,bookid):
#     a=Book.objects.get(id=bookid)
#     cart_items,created=Cart.objects.get_or_create(book=a, user=request.user)
#     if created:
#         cart_items.quantity-=1
#         cart_items.delete()
#         cart_items.save()
#     return redirect ('v')    

def buy_now(request,bookid):
    cart_items=get_object_or_404(Cart, user=request.user, id=bookid)
    book=cart_items.book

    session=stripe.checkout.Session.create (
         payment_method_types=['card'],
         line_items=[
           {
              'price_data':{
                  'currency':'inr',
                  'product_data':{
                      'name': book.name,
                   },
                   'unit_amount':int(float(book.price)*100),
               },
               'quantity':cart_items.quantity,
               
           }   
        ],

        mode="payment",
        success_url=request.build_absolute_uri(reverse('success')),
        cancel_url=request.build_absolute_uri(reverse('v')),
    )
    return redirect(session.url)

def success(request):
    return render(request,'APP1/success.html')