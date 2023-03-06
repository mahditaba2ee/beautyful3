function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');


function separate(Number) 
{
Number+= '';
Number= Number.replace(',', '');
x = Number.split('.');
y = x[0];
z= x.length > 1 ? '.' + x[1] : '';
var rgx = /(\d+)(\d{3})/;
while (rgx.test(y))
y= y.replace(rgx, '$1' + ',' + '$2');
return y+ z;
}
// create request 

function create_request(url,datas,btn=NaN){
    const request = new XMLHttpRequest()
    request.onreadystatechange=function(){
        if(request.readyState==1){
            btn.innerHTML='در حال بارگیری '

        }
        
    }
    const formdata = new FormData()
    request.open('POST',url)
    
    request.setRequestHeader('X-CSRFToken',csrftoken)
    var data;
    for (data in datas) {
        formdata.append(data,datas[data])

    }
    request.send(formdata)
    return request
}



function add_product(btn,home=''){
    var status_btn=btn.dataset.status
    var id = btn.dataset.id
    datas={}
    if(status_btn == 'buy'){
        datas = {'id':id ,'number':1}
    }
    if (status_btn== 'sell'){
        datas = {'id':id ,'type_request':'remove'}

    }
    request = create_request('/Orders/cart/add_and_remove',datas)
    request.onreadystatechange= function(){
        if(this.readyState==4){
            response = JSON.parse(this.responseText)
            if(response['cart_operation']=='remove'){
                btn.classList.remove('text-danger')
                btn.dataset.status='buy'
                btn.style.animation='pullDown'
                
                

            }
            else{

                btn.classList.add('text-danger')
                btn.dataset.status='sell'


        }
        
            document.getElementById('len_cart').innerHTML=response['len_cart']
            if (response['len_cart']!=0){
                
                document.getElementById('shop_icon').classList.add('text-danger')

            }
            if (response['len_cart']==0){
                document.getElementById('shop_icon').classList.remove('text-danger')
            }
            all_item_cart = create_request('/Orders/cart/list/item','')
            all_item_cart.onreadystatechange= function(){
                console.log(this.responseText);
                if(this.readyState==4){
                    document.getElementById('all_cart_item').innerHTML=this.responseText
                }
            
            }

        
    }
}   

    

}


function like_product(btn,home=''){
    
    datas={'id_product':btn.dataset.id_product,'is_like':btn.dataset.status}
    request = create_request('/Option/like',datas)
    request.onreadystatechange=function(){
        if(this.readyState==4){
            response = JSON.parse(this.responseText);
            like_status =response['like_status']
            if (like_status == 'like'){
                btn.classList.add('text-danger')
                btn.dataset.status='dislike'
            }
            if(like_status=='dislike'){
                btn.classList.remove('text-danger')
                btn.dataset.status='like'

            }
            if(like_status=='no_login'){
                
                alert('برای پسندیدن کالا باید لاگین کنید')
                return

            }
            btn.children[0].innerHTML=response['like_number'];
            if (home=='home'){
                document.getElementById('len_like').innerHTML=response['all_like_me_count']
                if (response['all_like_me_count']!=0){
                    
                    document.getElementById('like_icon').classList.add('text-danger')
    
                }
                if (response['all_like_me_count']==0){
                    document.getElementById('like_icon').classList.remove('text-danger')
            
    
                }
        }
    }
    }
}


function btn_change_number_product(type,btn,page_request='detail'){
    id = btn.dataset.id

    txt =document.getElementById('product_number'+id)
    if(type=='minus'){
        if (txt.value !=0)
        {
        txt.value = Number(txt.value)-1
    }
    }
    if (type=='plus'){
       txt.value =Number(txt.value)+1
    }
    txt_num_product(txt,page_request)

}


function txt_num_product(txt,page_request){
    datas={}
    if (txt.value==0){
        txt.value=0
      
        datas = {'id':txt.dataset.id ,'type_request':'remove'}
    }
    else{
        if (txt.value >9){
            txt.value=9
        }
        if (txt.value <0){
            txt.value=0
        }
        
        datas = {'id':txt.dataset.id ,'number':txt.value}
        
       
        
    }
    request = create_request('/Orders/cart/add_and_remove',datas)
        request.onreadystatechange= function(){
            if(this.readyState==4){
                response = JSON.parse(this.responseText)
                if(response['cart_operation']=='remove'){
                    alert('ss')
                    if(page_request=='detail'){
                    document.getElementById('product_add').classList.remove('text-danger')
                }
                    if(page_request=='cart'){
                    insert_price(response)

                    }
                }

                else{
                    if (page_request == 'detail'){
                   
                        document.getElementById('product_add').classList.add('text-danger')
                    }
                    if(page_request=='cart'){
                   insert_price(response)
                       

                    }
                    // else{
                    //     window.location.reload()
                    // }

            }
        }
    }
   


}

function insert_price(response){
    post_price = Number(response['post_price'])
    order_price = Number(response['order_price'])
    all_price_product = Number(response['all_price_product'])
    document.getElementById('price'+txt.dataset.id).innerHTML=separate(all_price_product)
    document.getElementById('total_price').innerHTML = separate(order_price)
    document.getElementById('price_with_post_price').innerHTML=separate(order_price+post_price)
}






function remove_cart(row){
    var id_product = row.dataset.id_product
    datas =datas = {'id':id_product ,'type_request':'remove'}
    request = create_request('/Orders/cart/add_and_remove',datas)
    request.onreadystatechange=function(){
        response = JSON.parse(this.responseText)

        if (this.readyState==4){
            

            row = document.getElementById('row'+id_product)
            
            row.classList.add('animate__animated', 'animate__bounceOutLeft');
            row.addEventListener('animationend', () => {
                row.hidden=true
              });
            document.getElementById('total_price').innerHTML = separate(Number(response['order_price']))
            
            
            
        }
    }
          
}


function search_click(){
    window.location='/text_search/'+document.getElementById('search').value
}
function myGreeting(){
msg = document.getElementById('message')
if (msg){
    msg.classList.add('animate__animated', 'animate__bounceOutLeft');
    msg.addEventListener('animationend', () => {
        msg.hidden=true})
    }
}
const mytime = setTimeout(myGreeting,5000);

