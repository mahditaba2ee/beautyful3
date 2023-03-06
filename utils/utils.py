from django.core.paginator import Paginator
from Orders.models import CoponModel
import datetime
def shopping_cart(request):
    buys=[]
    if request.session.get('cart') is not None:
        for product_id in list(request.session['cart'].keys()):
                    buys.append(int(product_id))
    return buys


def page(products,page_number):
    paginator = Paginator(products,8)
    page_number = page_number
    page_obj =paginator.get_page(page_number)
    return page_obj


def filtering (request,quety_product):
        products=[]
        
        prices = request.GET.get('lst_price','')
        brands = request.GET.get('lst_brand','')
        categories = request.GET.get('lst_categories','')
        
        if prices != '' or brands!='' or categories!='' :
            prices = prices.split(',')
            brands = brands.split(',')
            categories = categories.split(',')
            
            if prices!=['']:
                    
                for price in prices:
                    
                    if price == '1':
                        for p in quety_product:
                            if p.all_price >=0 and p.all_price<=20000:
                                products.append(p)
                    if price == '2':
                        for p in quety_product:
                            if p.all_price >20000 and p.all_price<=50000:
                                products.append(p)
                    if price == '3':
                        for p in quety_product:
                            if p.all_price >50000 and p.all_price<=80000:
                                products.append(p)
                    if price == '4':
                        for p in quety_product:
                            if p.all_price >80000:
                                products.append(p)
            else:
                products = quety_product
            
            brand_product=[]
            if brands!=['']:   
                for p in products:  
                    if str(p.brand.id) in brands:
                        brand_product.append(p)
                else:
                    products=[] 
            if brand_product !=[]:
                products=brand_product
            cat_product=[]
            if categories!=['']:       
                for p in products:
                    if str(p.category.id) in categories:
                         cat_product.append(p)
                else:
                    products=[]
            if cat_product:
                products=cat_product
           
            return products
        return quety_product
def copon_check(request,copon_code):
   
   
    copon_code = copon_code
    copon_model = CoponModel.objects.filter(end__gte=datetime.datetime.now())
    for c in copon_model:
        if c.copon_code == copon_code:
            if request.user in c.users.all():
                return c.persen
        return 0


