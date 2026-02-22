from django.forms import ModelForm
from .models import *
# from django.contrib.auth.models

class ordersForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class customerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class updateOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'status']

class updateCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email']

class createProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class updateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class createtagForm(ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'

class sellersignupform(ModelForm):
    class Meta:
        model = SellerProfile
        fields = '__all__'