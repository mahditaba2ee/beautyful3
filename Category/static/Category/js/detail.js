
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

id_product = document.getElementById('id_product').dataset.id

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


// stars add and view 
function star_mouse_move(btn,num){
    for(i=1;i<=5;i++){
        document.getElementById('btn'+i).style.color='black'
    }
    for(i=1;i<=num;i++){
        document.getElementById('btn'+i).style.color='yellow'
    }  
}

function star_mouse_leave(num){
    for(i=1;i<=num;i++){
        document.getElementById('btn'+i).style.color='black'
        
    }
    
}

function rank(rank,id,type_request){
    
    var datas = {'rank':rank,'product_id':id,'type_request':type_request} 
    request = create_request('/Option/rank',datas)
    request.onload=function()
    {
         const data = JSON.parse(this.responseText)
        if (data['status']=='notauth'){
            alert('برای ثبت نظر اول لاگین کنید')
        }
        else{
        var username = data['username']
        console.log(username);
        var rank =Number(data['rank'][username])
        for(i=1;i<=rank;i++){
            star=document.getElementById('btn'+i)
            star.style.color='yellow'
        }
        var ranks = data['rank']
        var value_star = (Object.values(ranks))
        
        var avarage=0
        for(x in value_star){
            avarage+= Number(value_star[x])
        }
        avarage = avarage/value_star.length
        document.getElementById('avarage_rank').innerHTML=avarage.toFixed(1)
        document.getElementById('count_rank').innerHTML=`(${value_star.length}) بازخورد `
        for(i=1;i<=5;i++){
            var star = value_star.filter(x => x==i).length
            var width = String((star*100)/value_star.length)+'%'
            c= document.getElementById('rank'+i).style.width=width

        }
    }
    }
}


function star_click(btn){
    rank(btn.dataset.rank,btn.dataset.id,'add')
}

function star_leave(btn){
    rank(btn.dataset.rank,btn.dataset.id,'start')
}




// comment add and view 
comment_body  = document.getElementById('comment_body')
user_id=''
comment_id =''
function reply_comment(btn){
    
    comment_body.value='@'+btn.dataset.username+' '
    comment_id = btn.dataset.comment_id

}

function sumbit_comment(btn){

    datas={'comment_body':comment_body.value,'product_id':btn.dataset.product_id,'comment_id':comment_id}
    request = create_request('/Option/comment',datas,btn)
    request.onreadystatechange=function(){
        if(this.readyState==4){
            btn.innerHTML="نظر"
            // be change
            window.location.reload()
    
    }
    }
    
    
}





function sendproduct(btn){
    var status_btn=btn.dataset.status
    var id = btn.dataset.id
    txt = document.getElementById('product_number'+btn.dataset.id) 
    datas={}
    if(txt.value == 0){
        datas = {'id':btn.dataset.id ,'number':1}
    }
    if (txt.value > 0){
        datas = {'id':btn.dataset.id ,'type_request':'remove'}

    }
    request = create_request('/Orders/cart/add_and_remove',datas)
    request.onreadystatechange= function(){
        if(this.readyState==4){
            response = JSON.parse(this.responseText)
            if(response['cart_operation']=='remove'){
                document.getElementById('product_add').classList.remove('text-danger')
                btn.dataset.status='buy'
                document.getElementById('product_add_title').innerHTML='افزودن به کارت'
                txt.value=0
                

            }
            else{
                document.getElementById('product_add').classList.add('text-danger')
                btn.dataset.status='sell'
                document.getElementById('product_add_title').innerHTML="حذف از کارت"

                txt.value=1

        }
    }
}


    
}







rank(0,id_product,'start')