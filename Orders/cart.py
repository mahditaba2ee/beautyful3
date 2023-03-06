

from Category.models import ProductModel

class Cart:
    def __init__(self,request):
        self.session = request.session
        cart = self.session.get('cart')
        if cart is None:
            cart = self.session['cart']={}
        self.cart = cart
        

    def Add(self,product,number):
        product_id = str(product.id)
        if product_id not in self.cart.keys():
            price =product.all_price
            if product.special:
                price=product.off_price
            self.cart[product_id]={'number':0,'price':str(price)}
        self.cart[product_id]['number'] = number
        self.cart[product_id]['all_price'] = int(self.cart[product_id]['number'])* int(self.cart[product_id]['price'])
        self.session.modified = True
        return True
    def Remove(self,product):
        product_id = str(product.id)
        if product_id in self.cart.keys():
            del self.cart[product_id]
        self.session.modified = True


    def __iter__(self):
        
        product_ids = self.cart.keys()
        products = ProductModel.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
           cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            
            item['total'] =str( int(item['number']) * int(item['price']))
            yield item
            


   
    def get_order_price(self):
        order_price = 0
        for c in self.cart:
            order_price +=self.cart[c]['all_price']
        return order_price
        
    def get_all_price_product(self,product_id):
        product_id = str(product_id)
        return (int(self.cart[product_id]['all_price']))

    def get_post_price(self,pay_type):
        if pay_type =='pay_person':
            return 0
        return 20000
    
    def get_price_with_off(self,per):
        total=0
        for product in  self.cart:
            
            total += int(self.cart[product]['number']) * int(self.cart[product]['price'])
        print('8'*80)
        print(total)
        return total - ((total * per)/100)

    def get_order_price_with_post_price(self,pay_type,per=0):
        post_price = self.get_post_price(pay_type)
        order_price = self.get_price_with_off(per)
        return post_price+order_price
        
    @property
    def get_len_cart(self):
        return len(self.cart.keys())
    @property
    def get_price_send_product(self):
        return 20000
    def all_price(self):
        return int(self.get_price_send_product )+ int(self.get_total)
    
    def is_null(self):
        for item in self.cart:
            return False
        return True