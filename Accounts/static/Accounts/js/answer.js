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
document.getElementById('nav-add').classList.add('active')


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

// برای لاگین در منوی اصلی گزینه ثبت نام و ورود را انتخاب کرده و سپس با زدن نام کاربری (username یا email یا شماره تماس) و رمز عبور وارد صفحه تایید دو مرحله ای میشوید که با وارد کردن کد که برای شما ایمیل شده است وارد حساب خود میشوید
function answer(btn){
    row = document.getElementById('que_'+btn.dataset.id)
    txt_answer = document.getElementById('txt_que_'+btn.dataset.id).value
    datas = {'id':btn.dataset.id,'answer':txt_answer}
    request = create_request('/Accounts/answer',datas)
    request.onreadystatechange=function(){
        if(this.readyState==4){
            row.classList.add('animate__animated', 'animate__bounceOutLeft');
            row.addEventListener('animationend', () => {
                row.hidden=true
              });

        
    }}
}