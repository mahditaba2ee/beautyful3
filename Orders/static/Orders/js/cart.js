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

document.getElementById('nav-prodile').classList.add('active')
type_pay()
// 3 ragham adad 20,000
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
function type_pay(){
    var elements = document.getElementsByClassName('pay_type')
    date = ""
    for (let x = 0; x < elements.length; x++) {
        const element = elements[x];
        if (element.checked){
            data = element.dataset.pay_type
            
            break
        }
        
    }
    datas={'pay_type':data}
    request  = create_request('/Orders/pay_type',datas)
    request.onreadystatechange=function(){
        
        if(this.readyState==4){
            response = JSON.parse(this.responseText)
            document.getElementById('price_post').innerHTML=separate(Number(response['post_price']))
            document.getElementById('price_with_post_price').innerHTML=separate(Number(response['order_price'])+Number(response['post_price']))
        }
    }
}

function copon_click(){
    copon_code = document.getElementById('input_copon').value
    datas = {'copon_code':copon_code}
    request = create_request('/Orders/copon',datas)
    request.onreadystatechange=function(){
        if(this.readyState==4){
            response = JSON.parse(this.responseText)
            if (response['copon_check']){
                alert('بن تخفیف اعمال شد و در فاکتور شما نمایش داده میشود')
            }
            else{
                alert('کد بن تخفیف اشتباه یا وجود ندارد')
            }
        }
    }
}
function buy_click(){
    
    window.location='/Orders/cart/checkout'
    
}