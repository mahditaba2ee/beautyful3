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


// create request 
document.getElementById('nav-prodile').classList.add('active')
function create_request(url,datas){
    const request = new XMLHttpRequest()
    request.onreadystatechange=function(){
     
        
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





function txt_ch(){
alert('df')
}


function txt_change(txt,name){
    var regex;
    message = ''
    status_text=''
    if(name =='phone'){
       
        regex = new RegExp("^(\\+98|0)?9\\d{9}$");
        message= 'شخص دیگری با این شماره ثبت نام کرده است'
        status_text='phone_status'
       
    }
    if (name =='email'){
        regex = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        message= 'شخص دیگری با این ایمیل ثبت نام کرده است'
        status_text='email_status'

    }
    if (name =='username'){
        if (txt.value.length>=5){
            regex = /^[a-zA-Z0-9]+$/;
            message= 'شخص دیگری با این نام کاربری ثبت نام کرده است'
            status_text='username_status'

        }
        else{
            txt.classList.add('bg-primary')
            return;
        }
}

        var result = regex.test(txt.value);
        if (result==false){
            txt.classList.add('bg-primary')
        }
        else{
            datas={'txt_value':txt.value,'txt_name':name}
            request = create_request('/Accounts/check/information/',datas)
            request.onreadystatechange=function(){
                if(this.readyState== 4){
                    response = JSON.parse(this.responseText)
                    if(response[status_text]==true){
                    txt.classList.remove('bg-primary')

                    }
                    else{
                        txt.classList.add('bg-primary')
                        alert(message)
                    }
                }
                
            }
            
         }

}
   










