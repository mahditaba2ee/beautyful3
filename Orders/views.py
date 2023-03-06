from django.shortcuts import render,redirect
from django.views import View
from .cart import Cart
from Category.models import ProductModel
from django.http import HttpRequest, HttpResponse, JsonResponse
from .models import CoponModel,OrderItemsModel,OrderModel
import datetime
from utils.utils import copon_check
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

class CartView(View):
    def dispatch(self, request, *args, **kwargs):
        cart = Cart(request)
      
        if cart.is_null():
            messages.success(request,'سبد خرید شما خالی است ','success') 
            return redirect('Category:home')  
        return super().dispatch(request, *args, **kwargs)
    def get(self,request):
        cart = Cart(request)

        # print(request.session['persen'])   
        # request.session['persen']['off_persen']=0
        # request.session.save()
        return render(request,'Orders/cart.html',{'cart':cart})

class Cart_Add_and_remove_View(View):
    def post(self,request):
        cart = Cart(request)
        post_price = cart.get_post_price('')
        product = ProductModel.objects.get(id=request.POST.get('id'))
        type_request = request.POST.get('type_request','add')
        if type_request == 'remove':
            cart.Remove(product)
            order_price=cart.get_order_price()
            
            len_cart = Cart(request).get_len_cart  
            return JsonResponse({'cart_operation':'remove','len_cart':len_cart,'order_price':order_price,'post_price':post_price})

        else:
            number = request.POST.get('number',1)
            cart.Add(product,number)
            order_price=cart.get_order_price()

            all_price_product = cart.get_all_price_product(product.id)
            len_cart = Cart(request).get_len_cart
            
            return JsonResponse({'cart_operation':'add','len_cart':len_cart,'all_price_product':all_price_product,'order_price':order_price,'post_price':post_price})

        
class Add_Product_To_Cart_Kesho(View):
    def post(self,request):
        cart = Cart(request)
        return render(request,'Orders/cart_item_ajax.html',{'cart':cart})

class PayTypeView(View):
    def post(self,request):
        cart = Cart(request)
        pay_type = request.POST.get('pay_type','pay_online')
        request.session['pay_type'] = request.POST.get('pay_type','pay_online')
        return JsonResponse({'order_price':cart.get_order_price(),'post_price':cart.get_post_price(pay_type),'order_price':cart.get_order_price()})
   

class CoponView(View):
    def post(self,request):       
        copon_code = request.POST.get('copon_code')
        copon_valid=copon_check(request,copon_code)
        request.session['off_per']=copon_valid
        return JsonResponse({'copon_check':copon_valid})
       



class CheckOutView(View):
    def dispatch(self, request, *args, **kwargs):
        cart = Cart(request)
        if cart.is_null():
            messages.success(request,'سبد خرید شما خالی است ','success') 
            return redirect('Category:home')  
        per_off = request.session.get('off_per',None)
        if per_off is None:
            per_off=0
        
        self.pay_type = request.session['pay_type']
        self.cart=cart
        self.price_post=cart.get_post_price(self.pay_type)
        self.order_price = cart.get_order_price()
        self.get_price_with_off=cart.get_price_with_off(per_off)
        self.get_order_price_with_post_price=cart.get_order_price_with_post_price(self.pay_type,per_off)
        return super().dispatch(request, *args, **kwargs)
    def get(self,request):  
        return render(request,'Orders/checkout.html',{'cart':self.cart,'post_price':self.price_post,
        'order_price':self.order_price,'order_price_with_off':int(self.get_price_with_off),
        'get_order_price_with_post_price':int(self.get_order_price_with_post_price)})

    def post(self,request):
        cd = request.POST
      
        cart =self.cart
        if cart.is_null()==False:
            if(cd['fulname'] != '' and cd['address']!='' and cd['phone']!=''and cd['ostan']!='' and cd['city']!='' and cd['codepsty']!=''):
                user=''
                if request.user.is_authenticated:
                    user = request.user
                
                order = OrderModel.objects.create(user=user,name = cd['fulname'],email=cd['email'],address=cd['address'],phone=cd['phone'],ostan=cd['ostan'],city=cd['city'],codepsty=cd['codepsty']
                ,price_all=self.order_price,price_off=self.get_price_with_off,price_with_post=self.get_order_price_with_post_price,pay_type=self.pay_type)
           
                for item in cart:
                    OrderItemsModel.objects.create(order = order,product=item['product'],price = item['price'],number=item['number'])
                
                del request.session['cart']
                request.session.modified = True
                messages.success(request,'سبد خرید شما با موفقیت ثبت شد','success')
                return JsonResponse({'order_status':'sumbit'})

            else:
                return JsonResponse({'order_status':'input_null'})
        else:
            return JsonResponse({'order_status':'cart_null'})







class OrderView(View):
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                self.orders = OrderModel.objects.filter(view=False)
                return super().dispatch(request, *args, **kwargs)
        return render(request,'404.html')
    def get(self,request):
        search = request.GET.get('search')
        orders = self.orders
        if search:
            orders =self.orders.filter(Q(id__contains=search)|Q(phone__contains=search))
        return render (request,'Orders/Orders.html',{'orders':orders})

    def post(self,request):
        order_id = request.POST.get('order_id',None)
        if order_id:
            order = OrderModel.objects.get(id=order_id)
            order.view=True
            order.user_view=request.user
            order.save()
            return JsonResponse({'status_order':'order_view'})
        return JsonResponse({'status_order':'err'})

class Archive_Order_view(View):
    def dispatch(self, request, *args, **kwargs):
        self.orders = OrderModel.objects.filter(view=True)
        return super().dispatch(request, *args, **kwargs)
    def get(self,request):
        search = request.GET.get('search')
        orders = self.orders
        if search:
            orders =self.orders.filter(Q(id__contains=search)|Q(phone__contains=search))
        return render (request,'Orders/Orders.html',{'orders':orders})

    def post(self,request):
        order_id = request.POST.get('order_id',None)
        if order_id:
            order = OrderModel.objects.get(id=order_id)
            order.view=True
            order.save()
            return JsonResponse({'status_order':'order_view'})
        return JsonResponse({'status_order':'err'})





