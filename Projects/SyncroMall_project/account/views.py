from urllib import request
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import redirect, render,get_object_or_404
import csv
import io
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *


from .forms import createProductForm, createtagForm, customerForm, ordersForm, updateCustomerForm, updateOrderForm, updateProductForm
from .views import *
from .models import *
from .filters import OrderFilter

# Create your views here.

# Landing page view
def landing_page(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    context = {
        'total_customers': total_customers,
        'total_orders': total_orders,
        'customers': customers,
        'orders': orders
    }
    return render(request, 'landing_page.html', context)

# home view
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()
    out_of_delivery = orders.filter(status="Out for delivery").count()
    customers = Customer.objects.all()
    context = {
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
        'out_of_delivery': out_of_delivery,
        'customers': customers,
        'orders': orders
    }
    return render(request, 'account/dashboard.html', context)

# dashboard view
def dash(request):
    customers = Customer.objects.all()
    products = Product.objects.all()
    orders = Order.objects.all()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()
    out_of_delivery = orders.filter(status="Out for delivery").count()
    context = {
        'customers': customers,
        'products': products,
        'orders': orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
        'out_of_delivery': out_of_delivery
    }
    return render(request, 'account/dashboard.html', context)



# seller signup form
def seller_signup(request):
    if request.method == 'POST':
        # Capture only what we need
        d = request.POST      
        # Create User
        user = User.objects.create_user(
            username=d['email'], 
            email=d['email'], 
            password=d['password'],
            first_name=d['full_name']
        )       
        # Create Profile
        SellerProfile.objects.create(
            user=user,
            phone=d['phone'],
            shop_name=d['shop_name'],
            gstin=d.get('gstin', '') # Optional field
        )        
        login(request, user)
        return redirect('dashboard')
    return render(request, 'signup_login/seller_signup.html')

# seller or buyer login/logout
def login_user(request):
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        
        if user is not None:
            login(request, user)
            
            # ROLE-BASED REDIRECTION LOGIC
            if hasattr(user, 'seller_profile'):
                messages.success(request, f"Welcome back to your Shop, {user.first_name}!")
                return redirect('dashboard') # Seller's Admin Panel
            else:
                messages.success(request, f"Hello {user.first_name}, happy shopping!")
                return redirect('landing_page') # Buyer's Home Page
        else:
            messages.error(request, "Invalid Email or Password. Please try again.")
            return redirect('login')

    return render(request, 'signup_login/user_login.html')

def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('landing_page')

# buyer_signup
def buyer_signup(request):
    if request.method == 'POST':
        d = request.POST
        # Create the User
        user = User.objects.create_user(
            username=d['email'],
            email=d['email'],
            password=d['password'],
            first_name=d['first_name'],
            last_name=d['last_name']
        )
        login(request, user)
        messages.success(request, "Account created! Welcome to SyncroMall.")
        return redirect('landing_page') # Redirect to the shopping home

    return render(request, 'signup_login/buyer_signup.html')



# status view
def out_for_delivery(request):
    orders = Order.objects.filter(status="Out for delivery")
    context = {
        'orders': orders,
    }
    return render(request, 'status/out_for_delivery.html', context)

def pending_orders(request):
    orders = Order.objects.filter(status="Pending")
    context = {
        'orders': orders,
    }
    return render(request, 'status/pending_orders.html', context)

def delivered_orders(request):
    orders = Order.objects.filter(status="Delivered")
    context = {
        'orders': orders,
    }
    return render(request, 'status/delivered_orders.html', context)



# product view
def product(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'product.html', context)

# product detail view
def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    context = {
        'product': product,
    }
    return render(request, 'product/product_detail.html', context)

def create_product(request):
    form = createProductForm()
    if request.method == 'POST':
        form = createProductForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('/product/')
    context = {
        'form': form,
    }
    return render(request, 'product/create_product.html', context)

# update product view
def update_product(request, pk):
    product = Product.objects.get(id=pk)
    form = updateProductForm(instance=product)
    if request.method == 'POST':
        form = updateProductForm(request.POST,request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/product/')
    context = {
        'form': form,
    }
    return render(request, 'product/update_product.html', context)

# delete product view
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('/product/')
    context = {
        'product': product,
    }
    return render(request, 'product/delete_product.html', context)

# Product Catalog
def product_catalog(request):
    products = Product.objects.all()
    all_tags = Tag.objects.all()
    tag_name = request.GET.get('tag')
    if tag_name:
        products = products.filter(tags__name=tag_name)
    
    context = {
        'products': products,
        'all_tags': all_tags,
    }
    return render(request, 'product/product_catalog.html', context)



# create tag view
def createtag(request):
    form = createtagForm()
    if request.method == 'POST':
        form = createtagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/tag_list')
    context = {
        'form': form,
    }
    return render(request, 'tag/create_tag.html', context)

# Tag list
def tag_list(request):
    all_tags = Tag.objects.all()
    context = {
        'tags': all_tags 
    }
    return render(request, 'tag/tag_list.html', context)

# Tag Upload
def upload_tag_csv(request):
    if request.method == "POST":
        csv_file = request.FILES.get('file')    
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a valid CSV file.')
            return redirect('tag_list')

        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        
        for row in csv.reader(io_string, delimiter=',', quotechar="|"):
            _, created = Tag.objects.update_or_create(
                name=row[0],
            )
        messages.success(request, 'Tags imported successfully.')
        return redirect('tag_list')
        
    return render(request, 'tag/upload_tag.html')

# download-tag-template
def download_tag_template(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tag_template.csv"'

    writer = csv.writer(response)
    # Define your header row
    writer.writerow(['name'])
    # Add a couple of sample rows
    writer.writerow(['Electronics'])
    writer.writerow(['Summer Collection'])
    writer.writerow(['New Arrival'])

    return response

# UPDATE TAG
def update_tag(request, pk):
    tag = get_object_or_404(Tag, id=pk)
    if request.method == "POST":
        tag.name = request.POST.get('name')
        tag.save()
        return redirect('tag_list')
    return render(request, 'tag/update_tag.html', {'tag': tag})

# DELETE TAG
def delete_tag(request, pk):
    tag = get_object_or_404(Tag, id=pk)
    if request.method == "POST":
        tag.delete()
        return redirect('tag_list')
    return render(request, 'tag/delete_tag.html', {'tag': tag})

# filter products by tag view
def products(request):
    products = Product.objects.all() #
    all_tags = Tag.objects.all() # This is the crucial line

    # Filter by tag if a query exists
    tag_filter = request.GET.get('tag')
    if tag_filter:
        products = products.filter(tags__name=tag_filter) #

    context = {
        'products': products,
        'all_tags': all_tags, # Ensure this matches your template loop
    }
    return render(request, 'products.html', context)



# customer view with pk
def cust(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()

    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()

    context = {
        "customer": customer,
        "orders": orders,
        "order_count": order_count,
        "delivered": delivered,
        "pending": pending,
    }

    return render(request, "customer.html", context)

# customer view with pk_test
def cust(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    total_orders = orders.count()
    myFilter = OrderFilter(request.GET,queryset=orders)
    orders = myFilter.qs
    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': total_orders,
        'myFilter': myFilter
    }
    return render(request, 'customer.html', context)

# customer list view
def customer_list(request):
    customers = Customer.objects.all()
    context = {
        'customer': customers,
    }
    return render(request, 'account/customer_list.html', context)

# create customer view
def create_customer(request):
    form = customerForm()
    if request.method == 'POST':
        form = customerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form,
    }
    return render(request, 'account/customer_form.html', context)

# Update customer view
def update_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = updateCustomerForm(instance=customer)
    if request.method == 'POST':
        form = updateCustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/customers/')
    context = {
        'form': form,
    }
    return render(request, 'account/update_customer.html', context)

# delete customer view
def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('/customers/')
    context = {
        'item': customer,
    }
    return render(request, 'account/delete_customer.html', context)



# order list view
def order_list(request):
    orders = Order.objects.all()
    context = {
        'orders': orders,
    }
    return render(request, 'orders.html', context)

# create order view
def create_order(request):
    form = ordersForm()
    if request.method == 'POST':
        form = ordersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form,
    }
    return render(request, 'order/order_form.html', context)

# place_order
def place_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    return render(request, 'order/order_form.html', {'form': formset})

# update order view
def updateorder(request, pk):
    order = Order.objects.get(id=pk)
    form = updateOrderForm(instance=order)
    if request.method == 'POST':
        form = updateOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/orders/')
    context = {
        'form': form,
    }
    return render(request, 'order/order_form.html', context)

# update order view
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = updateOrderForm(instance=order)
    if request.method == 'POST':
        form = updateOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            instance=form.save(commit=False)
            instance.customer = order.customer #keep the same customer
            instance.save()
            return redirect('/dash/')
    else:
        form = updateOrderForm(instance=order)

    context = {
        'form': form,
        'order': order,
        'customer': order.customer,
    }
    return render(request, 'order/update_order.html', context)

# delete order view
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {
        'item': order,
    }
    return render(request, 'order/delete_order.html', context)