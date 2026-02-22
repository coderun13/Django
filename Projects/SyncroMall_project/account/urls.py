from .import views
from django.urls import path, include

urlpatterns = [
    # home and dashboard
    path('', views.landing_page, name='home'),
    path('dash/', views.dash, name='dashboard'),
    path('landing_page/', views.landing_page, name='landing_page'),

    # seller/buyer login_aignup
    path('seller_signup/', views.seller_signup, name='seller_signup'),
    path('buyer_signup/', views.buyer_signup, name='buyer_signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # Status
    path('delivered_orders/', views.delivered_orders, name='delivered_orders'),
    path('pending_orders/', views.pending_orders, name='pending_orders'),
    path('out_for_delivery/', views.out_for_delivery, name='out_for_delivery'),

    # products
    path('product/', views.product, name='product'),
    path('product_detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('create_product/', views.create_product, name='create_product'),
    path('update_product/<str:pk>/', views.update_product, name='update_product'),
    path('delete_product/<str:pk>/', views.delete_product, name='delete_product'),
    path('catalog/', views.product_catalog, name='product_catalog'),

    # Tags
    path('createtag/', views.createtag, name='createtag'),
    path('tag_list/', views.tag_list, name= 'tag_list'),
    path('upload_tag/', views.upload_tag_csv, name='upload_tag_csv'),
    path('update_tag/<int:pk>/', views.update_tag, name='update_tag'),
    path('delete_tag/<int:pk>/', views.delete_tag, name='delete_tag'),
    path('download_tag_template/', views.download_tag_template, name='download_tag_template'),

    # customers
    path('customer/<int:pk_test>/', views.cust, name='customer'),
    path('customers/', views.customer_list, name='customer_list'),
    path('create_customer/', views.create_customer, name='create_customer'),
    path('update_customer/<str:pk>/', views.update_customer, name='update_customer'),
    path('delete_customer/<str:pk>/', views.delete_customer, name='delete_customer'),

    # orders
    path('orders/', views.order_list, name='order_list'),
    path('create_order/', views.create_order, name='create_order'),
    path('place_order/<int:pk>/', views.place_order, name='place_order'),
    path('update_order/<str:pk>/', views.update_order, name='update_order'),
    path('updateorder/<str:pk>/', views.updateorder, name='updateorder'),
    path('delete_order/<str:pk>/', views.delete_order, name='delete_order'),
]