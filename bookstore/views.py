from django.shortcuts import render,redirect
from .models import *
from .forms import OrderForm, CreateNewUser, CustomerForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# My decorators
from .decorators import notLoggedUsers, allowedUsers, forAdmins

# For Recaptcha
import requests
from django.conf import settings


# Create your views here.
@login_required(login_url='login')
# @allowedUsers(allowedGroups=['admin'])
@forAdmins
def home(request):
   customers = Customer.objects.all()
   orders = Order.objects.all()
   t_orders = orders.count() # Total Orders
   
   p_orders = orders.filter(status='Pending').count() # Pending Orders
   d_orders = orders.filter(status='Delivered').count() # Delevired Orders
   in_orders = orders.filter(status='In Progress').count() # In Prgoress Orders
   out_orders = orders.filter(status='Out Progress').count() # Out of Progress orders
   
   context = {
      'customers':customers,
      'orders':orders,
         't_orders':t_orders,
         'p_orders':p_orders,
         'd_orders':d_orders,
         'in_orders':in_orders,
         'out_orders':out_orders,
      }
   
   return render(request, 'dashboard.html',context)


@login_required(login_url='login')
@forAdmins
def books(request):
   books = Book.objects.all()
   context = {'books':books}
   return render(request, 'books.html',context)



@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin'])
def customer(request,pk):
   customer = Customer.objects.get(id=pk)
   orders = customer.order_set.all()
   num_orders = orders.count()
   searchFilter = OrderFilter(request.GET, queryset=orders)
   orders = searchFilter.qs
   context = {
      'customer': customer,
      'orders': orders,
      'num_orders': num_orders,
      'searchFilter':searchFilter,
   }
   return render(request, 'customer.html',context)




# def create(request):
   
#    form = OrderForm()
#    if request.method == "POST":
#       # print(request.POST)
#       form = OrderForm(request.POST)
#       if form.is_valid():
#          form.save()
#          return redirect('/')

#    context = {'form':form}
#    return render(request, 'my_order_form.html',context)


@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin'])
def create(request,pk):
      OrderFormSet = inlineformset_factory(Customer,Order,fields=('book', 'status'),extra=5)
      customer = Customer.objects.get(id=pk)
      formset = OrderFormSet(queryset = Order.objects.none(), instance=customer)
      # form = OrderForm()
      if request.method == 'POST':
         # print(request.POST)
         # form = OrderForm(request.POST)
         formset = OrderFormSet(request.POST , instance=customer)
         if formset.is_valid():
            formset.save()
            return redirect('/')
      #context = {'form':form}
      context = {'formset':formset}

      return render(request , 'my_order_form.html', context )


@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin'])

def update(request, pk):
   
      order = Order.objects.get(id=pk)
      formset = OrderForm(instance=order) 
      if request.method == 'POST': 
         formset = OrderForm(request.POST, instance=order)
         if formset.is_valid():
            formset.save()
            
            return redirect('/')

      # context = {'form':form}
      context = {'formset':formset}


      return render(request , 'my_order_form.html', context )



@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin'])

def delete(request,pk):
   
   order = Order.objects.get(id=pk)
   if request.method == "POST":
      order.delete()
      return redirect("/")
   context = {'order':order}
   return render(request, 'delete_form.html',context)


# def Login(request):
#    context = {}
#    return render(request, 'login.html',context)

@notLoggedUsers
def register(request):
   
      form = CreateNewUser()
      
      if request.method == 'POST':
         form = CreateNewUser(request.POST)
         
         if form.is_valid():
            
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
               'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
               'response':recaptcha_response,
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
            result = r.json()
            if result['success']:
               user = form.save()
               username = form.cleaned_data.get('username')
               messages.success(request, f'{username} Created Successfully!')
               return redirect('login')
            else:
               messages.error(request ,  ' invalid Recaptcha please try again!') 
      
      context = {'form':form}
      return render(request,'register.html',context)

@notLoggedUsers
def userLogin(request):
      if request.method == 'POST': 
         username = request.POST.get('username')
         password = request.POST.get('password')
         user = authenticate(request , username=username, password=password)
         if user is not None:
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
               'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
               'response':recaptcha_response,
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
            result = r.json()
            if result['success']:
               login(request, user)
               print("Login Request: ")
               print(request.POST)
               return redirect('home')
               
            
         else:
               messages.error(request, 'Username Or Password Error!')
   
      context = {}

      return render(request , 'login.html', context )


def userLogout(request):  
   logout(request)
   return redirect('login') 


@login_required(login_url='login')
@allowedUsers(allowedGroups=['customer'])
def userProfile(request):
   orders = request.user.customer.order_set.all()

   t_orders = orders.count() # Total Orders
   
   p_orders = orders.filter(status='Pending').count() # Pending Orders
   d_orders = orders.filter(status='Delivered').count() # Delevired Orders
   in_orders = orders.filter(status='In Progress').count() # In Prgoress Orders
   out_orders = orders.filter(status='Out Progress').count() # Out of Progress orders
   
   context = {
      
         'orders':orders,
         't_orders':t_orders,
         'p_orders':p_orders,
         'd_orders':d_orders,
         'in_orders':in_orders,
         'out_orders':out_orders,
      }
   
   return render(request, 'profile.html', context)

@login_required(login_url='login')
def profileInfo(request):
   customer = request.user.customer
   form = CustomerForm(instance=customer)
   
   if request.method == 'POST':
      form = CustomerForm(request.POST, request.FILES, instance=customer)
      if form.is_valid():
         form.save()
   
   context = {'form':form}
   return render(request, 'profile_info.html', context)