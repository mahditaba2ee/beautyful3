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


function order_click(){
    message = document.getElementById('message')
    message.hidden=true
    form = document.getElementById('form_information')
    
    var datas = {'fulname':form['txt_fulname'].value,'email':form['txt_email'].value,'phone':form['txt_phone'].value,'ostan':form['txt_ostan'].value
    ,'city':form['txt_city'].value,'codepsty':form['txt_codeposty'].value,'address':form['txt_address'].value}
    request = create_request('/Orders/cart/checkout',datas)
    request.onreadystatechange=function(){
        if(this.readyState==4){
            response = JSON.parse(this.responseText)
            if(response['order_status'] == 'cart_null'){
                console.log(message);
                message.hidden=false
                message.innerHTML='سبد خرید شما خالی است'
            }
            if(response['order_status'] == 'input_null'){
                console.log(message);
                message.hidden=false
                message.innerHTML='اطلاعات زیر را تکمیل نمایید'
            }
            if(response['order_status'] == 'sumbit'){
                
               window.location = ''
            }
        }

    }
    
}

function printer(){
    print(document.getElementById('factor'))
    }