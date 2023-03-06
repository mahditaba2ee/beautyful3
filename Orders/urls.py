from django.urls import path
from .views import *

app_name = 'Orders'
urlpatterns=[
    path('cart/view',CartView.as_view(),name='cart_view'),

    path('cart/add_and_remove',Cart_Add_and_remove_View.as_view(),name='cart_add'),
    path('pay_type',PayTypeView.as_view(),name='paytype'),

    path('cart/checkout',CheckOutView.as_view(),name='checkout'),
    path('copon',CoponView.as_view(),name='copon'),
    path('orders',OrderView.as_view(),name='orders'),
    path('archive/orders',Archive_Order_view.as_view(),name='archive_orders'),
    path('cart/list/item',Add_Product_To_Cart_Kesho.as_view(),name='archive_orders'),




    
    

]