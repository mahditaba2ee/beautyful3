// import {csrf_token } from './csrf.js'
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

function create_request(url,datas,btn){
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


var message = document.getElementById('message')

// functions
document.getElementById('nav-lagin').classList.add('active')






function login_click(btn){
    message.hidden=true
    const email = document.getElementById('txt_email').value
    const password1 = document.getElementById('txt_password').value
    const datas = {'email':email,'password':password1}
    var request= create_request('/Accounts/login',datas,btn)
    request.onreadystatechange=function(){

        if(this.readyState==4){
        btn.innerHTML='ورود'
        try{
            message.classList.add('animate__fadeInRight')
            message.addEventListener('animationend', () => {
                message.hidden=false
            })
            response = JSON.parse(this.responseText)
        
            message.hidden=false
            message.append(response['login'])
            if (response['login'] == 'user_not_found'){
                message.hidden=
                message.innerHTML=' نام کاربری یا رمز عبور صحیح نمیباشد'
                
            }
            if(response['login']=='form_not_valid'){ 
                message.innerHTML='لطفا مقادیر را بررسی کنید'
             
            }
        }
        catch{
         document.getElementById('main').innerHTML=this.responseText;   
        }

            setTimeout(function(){
                message.classList.remove('animate__fadeInRight')
                message.classList.add('animate__bounceOutLeft');
                message.addEventListener('animationend', () => {
                    message.classList.remove('animate__bounceOutLeft');
                    message.hidden=true
                })
    
            },3000)
    }
    }
 

}





function otpcode_click(btn){
    message.hidden=true

    otpcode = document.getElementById('txt_otpcode').value
    var datas = {'otpcode':otpcode}
    var request = create_request('/Accounts/verify_otp_code',datas,btn)
    request.onreadystatechange=function(){
        console.log(this.responseText);
        if(this.readyState==4){
            btn.innerHTML='ورود'
            response = JSON.parse(this.responseText)
            if(response['status_login']=='login'){
                window.location.reload('127.0.0.1:8000/')
            }
            if(response['status_login']=='no_login'){
                message.hidden=false
                message.innerHTML='کد نا معتبر است'
            }
        }
    }
}




function register_click(btn){
    
    message.hidden=true
    form = document.getElementById('form_register')
    var datas = {'username':form['txt_username'].value,'email':form['txt_email'].value,'phone':form['txt_phone'].value,'password1':form['txt_password1'].value
    ,'password2':form['txt_password2'].value}
    var request=create_request('/Accounts/register',datas,btn)
    request.onreadystatechange=function(){
        if(this.readyState==4){
        response = JSON.parse(this.responseText);
        btn.innerHTML='ثبت نام'
        error_message=''
        // بررسی ارور ها و نمایش آن به کاربر در حال ثبت نام
        if (response['register'] == 'form_error'){
            for (err in response['error']){
                if(response['error'][err]=='email'){
                    error_message +=' ایمیل،'
                }
                if(response['error'][err]=='username'){
                    error_message +=' نام کاربری،'
                }
                if(response['error'][err]=='phone'){
                    error_message +=' شماره موبایل،'
                }
                if(response['error'][err]=='password2'){
                    error_message +=' رمز عبور،'
                }
            }
            error_message +=' بررسی کنید'
                message.hidden=false
                message.innerHTML=error_message
        }
        if (response['register'] == 'user_register'){
            message.hidden=false
            message.innerHTML='تبریک! ثبت نام با موفقیت انجام شد'
        }
        
    }


}

}

