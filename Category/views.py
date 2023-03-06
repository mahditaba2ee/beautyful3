from django.shortcuts import render,redirect
from django.views import View
from .models import *
from django.http import HttpRequest, HttpResponse, JsonResponse
from Product_option.models import CommentModel,ReplayCommentModel
from utils.utils import shopping_cart,page,filtering
from Orders.cart import Cart
from .forms import AddProductForm
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
# from django import views
# import django
# 
# from django.shortcuts import redirect, render
# from django.urls import reverse_lazy ,reverse
# 
# 
# from .forms import AddProductForm,AddCtegoryForm
# from django.core.files.base import ContentFile
# from django.utils.text import slugify
# from .cart import Cart
# from Accounts.views import UserProfileView
# from django.contrib import messages
# 
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import login_required
# import datetime
# from .send_email import send_email
# from .utils import shopping_cart,filtering,page


# Create your views here.
# @method_decorator(cache_page(5*60),name='dispatch')
class CategoryView(View):
    def dispatch(self, request, *args, **kwargs):
        self.products = ProductModel.objects.filter(available=True)
        self.slids_images = ImagdeSlidModel.objects.all()[:5]
        return super().dispatch(request, *args, **kwargs)

    def get(self,request):
        categories = CategoryModel.objects.all()
        most_like_product = self.products[:8] 
        off_product = self.products.filter(special=True)[:8]
        buys = []
        all_like_me_count=0
        if request.session.get('cart') is not None:
            buys = shopping_cart(request)
            if request.user.is_authenticated:
                all_like_me_count = request.user.all_like_me_count()
        cart = Cart(request)
        print(request.session['cart'])
        return render(request,'Category/home.html',{'page':'home','categories':categories,'most_like_product':most_like_product,
        'off_product':off_product,'slids_images':self.slids_images,'buys':buys,'all_like_me_count':all_like_me_count,
        'len_cart':cart.get_len_cart,'cart':cart})
        

class ProductDetailsView(View):
    def get(self,request,*args,**kwargs):
       
        
        product = ProductModel.objects.get(slug=kwargs['product_slug'])
        simiar_products = ProductModel.objects.filter(type=product.type)
        comments = CommentModel.objects.filter(product=product)
        buys = []
        if request.session.get('cart') is not None:
            buys = shopping_cart(request)
        number=0
        if product.id in buys:
            id_product = str(product.id)
            number = request.session['cart'][id_product]['number']
        cart = Cart(request)

        return render(request,'Category/detail.html',{'product':product,'simiar_products':simiar_products,'comments':comments,'buys':buys,'number':number,'cart':cart})
# @method_decorator(cache_page(5*60),name='dispatch')
class SearchCategoryView(View):
    def dispatch(self, request, *args, **kwargs):
        
        self.category = CategoryModel.objects.get(slug=kwargs['category_slug'])
        self.products = ProductModel.objects.filter(category = self.category)
        
        return super().dispatch(request, *args, **kwargs)
    def get(self,request,category_slug,type_slug=None,name_product=None,search=None):
        search_name_product=self.category.name
        order = request.GET.get('order','name')
        page_type = ''
        type_slug_select=None
        p = request.GET.get('page',1) 
        print('sss'*80)
        print(p) 
        # if request.GET.get('is_ajax'):
        
        #     self.products = page(self.products,p) 
        #     return render(request,'Category/shop_ajax.html',{"products":self.products,'p':int(p)})
            
        lst_name = TypeProductModel.objects.filter(category = self.category)
        page_type= 'category_search'
        buys = shopping_cart(request)
        if type_slug:
            
            type = TypeProductModel.objects.get(slug = type_slug)
            search_name_product=type.name
            type_slug_select = type.slug
            self.products=self.products.filter(type=type)
            lst_name = set(name.name for name in type.product_to_type.all() )
            page_type= 'type_search'
        if name_product:
            self.products = self.products.filter(name=name_product)
            search_name_product=name_product
        if search:
            self.products=self.products.filter(name__contains = search)
        
        order_convert_to_farsi={
            'name':'نام',
            '-like_count':"بیشترین لایک",
            'all_price':" ارزانترین",
            '-all_price':"گرانترین",
            "created":"جدیدترین",
            "name":"نام"
        }.get(order,'noting')

        self.products=page(self.products.order_by(order),p)
        if request.GET.get('is_ajax'):
           
            return render(request,'Category/shop_ajax.html',{"products":self.products,'p':int(p)})
        cart =Cart(request)
        return render(request,'Category/category_search.html',{"products":self.products,'category_slug':self.category.slug,'type_slug_select':type_slug_select,
        'buys':buys,'p':int(p),'lst_product':lst_name,'page_type':page_type,'order_convert_to_farsi':order_convert_to_farsi,'search_name_product':search_name_product,'order':order,'cart':cart})


class BoxSearchView(View):
    def get(Self,request,text_search):
        p = request.GET.get('page',1)
        print(text_search)
        order = request.GET.get('order','name')
        products=page(ProductModel.objects.filter(full_name__contains = text_search).order_by(order),p)
        order_convert_to_farsi={
            'name':'نام',
            '-like_count':"بیشترین لایک",
            'all_price':" ارزانترین",
            '-all_price':"گرانترین",
            "created":"جدیدترین",
            "name":"نام"
        }.get(order,'noting')
        
        return render(request,'Category/category_search.html',{"products":products,'text_search':text_search,'order_convert_to_farsi':order_convert_to_farsi,'order':order,'p':int(p),'page_type':'text_search'})


class ShopView(View):
    def dispatch(self, request, *args, **kwargs):
        self.categories = CategoryModel.objects.all()
        self.brands = BrandModel.objects.all()
        self.products = ProductModel.objects.all().order_by('created')
        return super().dispatch(request, *args, **kwargs)
    def get(self,request):
        is_ajax = request.GET.get('ajax',False)
        page_number = request.GET.get('page',1)
        order = request.GET.get('order','name')
        cart = Cart(request)
        if is_ajax ==False:
            products = page(self.products,page_number)
            return render(request,'Category/shop.html',{'brands':self.brands,'categories':self.categories,'products':products,'p':int(page_number),'cart':cart})
        if is_ajax:
            products = filtering(request,self.products.order_by(order))
            products=page(products,page_number)
            return render(request,'Category/shop_ajax.html',{'products':products,'p':int(page_number)})

     



class TypeProductView(View):
    def get(self,request):
        type_id = request.GET.get('type',False)
        order = request.GET.get('order','name')
        if type_id:
            type = TypeProductModel.objects.get(id = type_id)  
            products= ProductModel.objects.filter(type = type).order_by(order)
            p = request.GET.get('page',1)
            products = page(products,p)
            return render(request,'Category/shop_ajax.html',{'products':products,'p':int(p),'page_type':'type_list'})
        typies = TypeProductModel.objects.all()
        return render(request,'Category/list_type.html',{'typies':typies})




class LikeCategoryView(View):
        
    def get(self,request): 
        buys = shopping_cart(request)
        products = ProductModel.objects.filter(like = request.user)
        return render(request,'Category/category_search.html',{"products":products,'buys':buys})




class Most_View(View):

    def dispatch(self, request, *args, **kwargs):
        self.products = ProductModel.objects.all()[:8]
        return super().dispatch(request, *args, **kwargs)
    def get(self,request): 
        p = request.GET.get('page',1)
        buys = shopping_cart(request)         
        products=page(self.products,p)
        return render(request,'Category/category_search.html',{"products":products,'buys':buys,'p':int(p)})




class Add_Slide_View(View):
    
    def get(self,request):
        
        id_slide=request.GET.get('id_slide',False)
        if id_slide:
            slide = ImagdeSlidModel.objects.get(id = id_slide)
            return render(request,'Category/Add_slide.html',{'slide':slide})
        return render(request,'Category/Add_slide.html')
        
    def post(self,request):
        cd = request.POST
        id_slide=request.GET.get('id_slide',False)
        img = request.FILES.get('img')
        if img is None:
            messages.info(request,'عکسی را انتخاب کنید','info')
            return redirect('Category:add_slide')
        url=cd['txt_url']
        title=cd['txt_title']
        des=cd['txt_des']
        if id_slide:
            slide = ImagdeSlidModel.objects.get(id = id_slide)
            slide.title=title
            slide.des=des
            slide.url=url
            slide.image=img
            slide.save()
            messages.success(request,'ویرایش انجام شد','success')
            return redirect('Category:add_slide')
       
        ImagdeSlidModel.objects.create(image=img,url=url,title=title,des=des)
        return HttpRequest('ok')
        




class AddProductView(View):
    def get(self,request):
        categories = CategoryModel.objects.all()
        brands = BrandModel.objects.all()
        type = TypeProductModel.objects.all()
        return render(request,'Category/add_product.html',{'categories':categories,'brands':brands,'type':type})
  
    def post(self,request):
        brand_id=request.POST['brand_option']
        type_id = request.POST['type_option']
        category_id = request.POST['category_option']
        

        form =AddProductForm(request.POST)
        
        # return HttpResponse(request.POST.get('avalable'))
        category = CategoryModel.objects.get(id=category_id)
        brand = BrandModel.objects.get(category=category,id =brand_id )
        type = TypeProductModel.objects.get(id=type_id )
        try:
            if form.is_valid():
                
                cd = form.cleaned_data
                product = ProductModel.objects.create(name=cd['name'],full_name=cd['full_name'],des=cd['des'],all_price=cd['all_price'],off_price=cd['off_price'] ,
                category=category,brand=brand,type=type)              
                product.save()
                
            file = request.FILES.getlist("images[]")
            
            for img in file:
                ImageProductModel.objects.create(product=product,image=img)
            messages.success(request,'کالا اضافه شد','success')
            return redirect('Category:add_product')
        except:
            messages.danger(request,'کالا اضافه نشد','danger')

            return redirect('Category:add_product')

        
       



     
class ChoiseView(View):
    
    def post(self,request):
        id = request.POST['id']
        category = CategoryModel.objects.get(id=id)
        typies = TypeProductModel.objects.filter(category=category)
        brands = BrandModel.objects.filter(category=category)
        brand_lst={}
        type_lst={}
        for brand in brands:
            brand_lst[brand.id]=brand.name
        for type in typies:
            type_lst[type.id]=type.name
        
        return JsonResponse({'brand_lst':brand_lst,'type_lst':type_lst})





































# class ProductDetailsView(View):
#     def get(self,request,product_slug,*args,**kwargs):
#         print(product_slug)
#         product = ProductModel.objects.get(slug=product_slug)
#         buys = []
#         number = 1 
#         if request.session.get('cart') is not None:
#             buys = shopping_cart(request)
#             if request.session.get('cart').get(str(product.id)) is not None:
#                 number = request.session.get('cart')[str(product.id)]['number']
        
#         products = ProductModel.objects.filter(category=product.category)
#         comment = CommentModel.objects.filter(product = product,is_replay=False)
#         images = ImageProductModel.objects.filter(product=product)
#         print(comment)
#         # comment_replay = ReplayCommentModel.objects.filter(comment = comment)
        
#         return render(request,'category/detail.html',{'product':product,'comment':comment,'images':images,'products':products,'buys':buys,'number':number})

#     def post(self,request,*args,**kwargs):
#         return HttpResponse(request.POST['comment'])

# class OrderView(LoginRequiredMixin,View):
#     def get(self,request):
#         a=OrderModel.objects.filter(user = request.user)
#         if request.user.address =='':
#             messages.info(request,'برای ثبت سفارش لطفا اطلاعات خود را وارد نمایید','info')
#             return redirect('/accounts/profie?next=orderview')
        
#         order_create = OrderModel.objects.create(user = request.user,address = request.user.address,phone=request.user.phone,name=f'{request.user.name}{request.user.family}')
#         cart = Cart(request)
        
#         global  OrderItems
#         my_lst=[]
#         for order in cart:
#             pruduct = ProductModel.objects.get(id=order['product'].id)
            
#             my_lst.append(order['product'].user.id)
#             OrderItems =  OrderItemsModel.objects.create(order = order_create,user_created =  order['product'].user ,product=pruduct,price=int(order['product'].price),number=int(order['number']))
#         #در اینجا باید کاربر به صفحه پرداخت هدایت شود
#         del request.session['cart']
#         request.session.modified = True
#         my_set = set(my_lst)
#         for id in my_set:
           
#             user = User.objects.get(id=id)
#             for order in cart:
#                 if order['product'].user.id == user.id:
#                     ProductNotModels.objects.create(user = user,product=order['product'])
#         return HttpResponse(my_lst)



# class LastOrderView(View):
#     def get(self,request):
#         cart =Cart(request)
#         pay_type = request.session['pay_type']
#         print(request.session['persen'])
#         persen = request.session['persen']['off_persen']
#         price_with_off=cart.get_price_with_off(persen)
#         if pay_type == 'pay_person':
#             price_with_off_and_send=price_with_off
#         else:
#             price_with_off_and_send=price_with_off + cart.get_price_send_product
#         return render(request,'category/last_order_view.html',{'price_with_off':int(price_with_off),'price_with_off_and_send':int(price_with_off_and_send),
#         'cart':cart,'pay_type':pay_type})

# class PayTypeView(View):
#     def post(self,request):
#         request.session['pay_type'] = request.POST.get('pay_type')

#         return JsonResponse({'pay_type':request.session['pay_type']})
    
        
# class SendOrderView(View):
#     def get(self,request):
#         if request.user.is_superuser:
#             users = User.objects.filter(is_admin=True)
#             orders = OrderModel.objects.filter(usersender=None,view=False)
#             return render(request,'category/send_order.html',{'orders':orders,'users':users})

#         if request.user.is_admin:
#             user = User.objects.get(id = request.user.id)
#             notification =  OrderItemsModel.objects.filter(user_created = user)       
#             noti_view = notification.filter(view=True).order_by('order')
#             noti_not_view = notification.filter(view=False)
             
#             print(noti_not_view.exists())
        
#             my_lst=[]
#             for n in notification:
#                 my_lst.append(n.order.id)
                
#             my_set=set(my_lst)
            
#             return render(request,'category/not_product.html',{'noti_view':noti_view,'noti_not_view':noti_not_view,'order_id':my_set})

#     def post(self,request):
#         id = request.POST['id']
        
#         notification =  OrderItemsModel.objects.get(id= id)     
#         notification.view=True
#         notification.save()
#         order = OrderModel.objects.get(id = notification.order.id)
#         items = OrderItemsModel.objects.filter(order= order)
#         my_lst=[]
#         all_from_user=1
#         for o in items:
#             my_lst.append(o.product.name)
#             if o.user_created != request.user:
#                 all_from_user=0
#             if o.view == False:
#                 return
#         try:
#             send_email(my_lst,order.id,order.user.email,order.address,order.user.name,order.user.family)
#             if all_from_user == 1:
#                 order.usersender=request.user

#         except:
#             notification.view=False
#             notification.save()
#             return JsonResponse({'status':'not_net'})
        
        
#         order.view = True
#         order.save()
            
        
        
#         send_email(my_lst,order.id,order.user.email,order.address,order.user.name,order.user.family)
#         return JsonResponse({'status':'ok','all':all_from_user})
      


# class OldOrderView(View):
#     def get(self,request):
#         if request.user.is_superuser:
#             orders = OrderModel.objects.filter(view=True)
#             return render(request,'category/old_orders.html',{'orders':orders})
#         else:
#             orders = OrderModel.objects.filter(usersender=request.user)
#             return render(request,'category/old_orders.html',{'orders':orders})


# class SubmitOrderView(View):
#     def post(self,request):
#         orderid = request.POST.get('id')
#         order = OrderModel.objects.get(id = orderid)
#         order.view=True
#         order.save()
#         messages.success(request,'سبد خرید تایید شد','success')
#         return JsonResponse({'status':'ok'})
        


# class BackOrderView(View):
#     def post(self,request):
#         orderid = request.POST.get('id')
#         order = OrderModel.objects.get(id = orderid)
#         order.usersender=None
#         order.save()
#         messages.success(request,'سبد خرید برگشت داده شد','success')
#         return JsonResponse({'status':'ok'})



# class SendOrderUserView(View):
#     def post(self,request):
#         iduser = request.POST.get('iduser')
#         idorder = request.POST.get('idorder')
#         user = User.objects.get(id = iduser)
#         order = OrderModel.objects.get(id = idorder )
#         order.usersender = user
#         order.save()
#         messages.success(request,'سبد خرید تایید شد','success')
#         return JsonResponse({'status':'ok'})


# from django.db.models import Q
# # class SearchView(View):
# #     def get(self,request,strproduct):

# #         buys =[]
# #         if request.session.get('cart') is not None:
# #             buys = shopping_cart(request)
# #         categories = CategoryModel.objects.all()

# #         try:
# #             try:
# #                 type = TypeProductModel.objects.get(slug = strproduct)
# #                 products = ProductModel.objects.filter(Q(type=type))

# #             except:
# #                 products = ProductModel.objects.filter(Q(name__contains=strproduct)|Q(des__contains=strproduct))
# #             return render(request,'category/search.html',{"products":products,'categories':categories,'buys':buys})
# #         except:
# #             return render(request,'category/search.html',{'categories':categories,'buys':buys})

        



# #         category = CategoryModel.objects.get(name_category=slug)
# #         if brand_slug is not None:
# #             brand = BrandModel.objects.get(slug=brand_slug)
# #             products = ProductModel.objects.filter(brand=brand)

# #         else:
# #             products = ProductModel.objects.filter(category=category)

        
# #         lenorders=0
# #         if request.user.is_authenticated:
# #             lenorders = len(OrderModel.objects.filter(usersender=request.user,view=False))
# #         images=[]
# #         for p in products:
# #             images.append(ImageProductModel.objects.filter(product=p).first()) 
        
# #         category = CategoryModel.objects.all()
# #         return render(request,'category/list_category.html',{"products":products,'images':images,'lenorders':lenorders,'category':category})

# class SearchCategoryView(View):
#     def get(self,request,category_slug):
#         category = CategoryModel.objects.get(slug=category_slug)
#         buys = []
#         if request.session.get('cart') is not None:
#             buys = shopping_cart(request)
#         products = ProductModel.objects.filter(category = category)
#         return render(request,'category/category_search.html',{"products":products,'buys':buys})

        
# class ChoiseView(View,LoginRequiredMixin):
    
#     def post(self,request):
#         category = CategoryModel.objects.get(name_category=request.POST['value'])
#         type = TypeProductModel.objects.filter(category=category)
#         brand = BrandModel.objects.filter(category=category)
#         mylst=[]
#         mylst2=[]
#         for b in brand:
#             mylst.append(b.name_brand)
#         for t in type:
#             mylst2.append(t.name)
#         return JsonResponse({'status':mylst,'mylst2':mylst2})


# class StarAddView(View):
    
    

#     def post(self,request):

#         product_id = request.POST['id']
#         product = ProductModel.objects.get(id = product_id)
#         username = request.user.username
#         star_count = request.POST['count']
        

#         if not request.user.is_authenticated: 
#             if star_count =='start':
#                 return JsonResponse({'star':product.star})
 
#             return JsonResponse({'status':'notauth'})
#         if star_count !='start':
#             product.star[str(username)] =str( star_count)
#             product.save()
#         return JsonResponse({'star':product.star,'username':username})

# class StarView(View):
#     def post(self,request):
        
#         product_id = request.POST['product_id']
#         product = ProductModel.objects.get(id = product_id)
#         lst=[]
#         for value in product.star.values():
#             lst.append(value)
        
        

#         return JsonResponse({'star':lst})



# class SharePostView(View):
#     def post(self,request):
#         users = User.objects.all()
#         return render(request,'category/share.html',{'users':users})


# class AddBrandView(View):
#     def post(self,request):
#         cd = request.POST
#         try:
#             category = CategoryModel.objects.get(name_category=cd['category'])
#             BrandModel.objects.create(category=category,name_brand=cd['name_brand'])
#             return JsonResponse({'status':'ok'})
#         except:
#             return JsonResponse({'status':'err'})



# class AddCategoryView(View):
#     def get(self,request):
#         form = AddCtegoryForm
#         return render(request,'category/add_category.html',{"form":form})
#     def post(self,request):
#         cd = request.POST
#         media = request.FILES
#         try:
#             category = CategoryModel.objects.create(name_category=cd['name'],slug=cd['slug'],img=media['img'])
#             if (request.POST.get('avalable',False)=='on'):
#                 category.available=True
#                 category.save()
#             messages.success(request,'کالا افزوده شد','success')
#             return redirect('category:addproduct') 

#         except:
            
#             messages.info(request,'کالا افزوده نشد','info')
#             return redirect('category:addcategory') 


# class AddTypeView(View):
#     def post(self,request):
#         cd = request.POST
#         try:
#             category = CategoryModel.objects.get(name_category=cd['category'])
#             TypeProductModel.objects.create(category=category,name=cd['name_type'])
#             return JsonResponse({'status':'ok'})
#         except:
#             return JsonResponse({'status':'err'})



# class CoponView(View):
#     def post(self,request):
#         copon_code = request.POST.get('copon')
#         copon_model = CoponModel.objects.filter(end__gte=datetime.datetime.now())
#         for c in copon_model:
#             if c.copon_code == copon_code:
#                 if request.user in c.users.all():
#                     print(type(c.persen))
#                     request.session['persen']={}
#                     request.session['persen']['off_persen'] = c.persen
#                     print(request.session['persen'])
#                     request.session.save()
#                     return JsonResponse({'price':Cart(request).get_price_with_off(c.persen)})
                
             
        
        
            


# class OrderSumbitView(View):
    
#     def post(self,request):
#         cd = request.POST
#         cart = Cart(request)
        
#         if cart.is_null()==False:

#             if(cd['name'] != '' and cd['address']!='' and cd['phone']!=''and cd['ostan']!='' and cd['city']!=''):
#                 user=''
#                 if request.user.is_authenticated:
#                     user = request.user
#                 price_off=(cart.get_price_with_off(request.session['persen']['off_persen']))
#                 order = OrderModel.objects.create(user=user,name = cd['name'],email=cd['email'],address=cd['address'],phone=cd['phone'],ostan=cd['ostan'],city=cd['city'],price_off=price_off)
#                 for item in cart:
#                     OrderItemsModel.objects.create(order = order,product=item['product'],price = item['price'],number=item['number'])
#                 order.price_all=order.total_price()
#                 if request.session['pay_type'] != 'pay_person':
#                     order.price_with_post = price_off+ cart.get_price_send_product
#                 order.save()
#                 del request.session['cart']
#                 request.session.modified = True
#                 return JsonResponse({'status':'ok'})

#             else:
#                 return JsonResponse({'status':'input_null'})
#         else:
#             return JsonResponse({'status':'cart_null'})









# class ShopView(View):
#     def get(self,request):
#         self.quety_product = ProductModel.objects.all()
        
#         is_ajax=(request.GET.get('ajax',False))
#         products = filtering(request,self.quety_product)
#         search = request.GET.get('search',False)

#         if is_ajax==False:
#             search = request.GET.get('search',False)
#             p = request.GET.get('page',1)
#             products = page(self.quety_product,p)
#             categories = CategoryModel.objects.all()
#             brands = BrandModel.objects.all()
#             return render(request,'category/shop.html',{'brands':brands,'products': products,'categories':categories,'p':int(p)})


#         if search:
#             new_p=[]
#             if products is None:
#                 products = self.quety_product
#             for p in products:
#                 if search in p.name or search in p.category.name_category:
#                     new_p.append(p)
#             products=new_p
#         p = request.GET.get('page',1)
#         products = page(products,p)
#         return render(request,'category/shop_ajax.html',{'products':products,'p':int(p)})
#     def post(self,request):
#         pass



# class SearchView(View):
#     def get(self,request):
#         search = request.GET['search']
#         brand =''
#         name = search.split(' ')[0]
#         products = ProductModel.objects.filter(Q(name__contains=name)| Q(des__contains=name))
        
#         try:
#             brand = search.split(' ')[1]
#         except:
#             pass
#         product_brand=[]
#         print(brand)
#         print('ssddssdd')
#         if brand!='':
#             for p in products:
#                 print(p.brand.name_brand)

#                 if brand in p.brand.name_brand :
#                     product_brand.append(p)
#         print(product_brand)
#         if product_brand !=[]:
#             products = product_brand
        
#         return render(request,'category/shop_ajax.html',{'products':products})
        
#         print(p)
#         return render(request,'category/shop_ajax.html',{'products':products})
#         buys =[]
#         if request.session.get('cart') is not None:
#             buys = shopping_cart(request)
#         categories = CategoryModel.objects.all()

#         try:
#             try:
#                 type = TypeProductModel.objects.get(slug = strproduct)
#                 products = ProductModel.objects.filter(Q(type=type))

#             except:
#                 products = ProductModel.objects.filter(Q(name__contains=strproduct)|Q(des__contains=strproduct))
#             return render(request,'category/search.html',{"products":products,'categories':categories,'buys':buys})
#         except:
#             return render(request,'category/search.html',{'categories':categories,'buys':buys})

        



#         category = CategoryModel.objects.get(name_category=slug)
#         if brand_slug is not None:
#             brand = BrandModel.objects.get(slug=brand_slug)
#             products = ProductModel.objects.filter(brand=brand)

#         else:
#             products = ProductModel.objects.filter(category=category)

        
#         lenorders=0
#         if request.user.is_authenticated:
#             lenorders = len(OrderModel.objects.filter(usersender=request.user,view=False))
#         images=[]
#         for p in products:
#             images.append(ImageProductModel.objects.filter(product=p).first()) 
        
#         category = CategoryModel.objects.all()
#         return render(request,'category/list_category.html',{"products":products,'images':images,'lenorders':lenorders,'category':category})