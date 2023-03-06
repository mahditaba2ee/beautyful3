
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
document.getElementById('nav-shop').classList.add('active')
    

function csrfSafeMethod(method) {
// these HTTP methods do not require CSRF protection
return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


var lst_price =[]
var lst_brand =[]
lst_categories=[]

order = 'name'


function filter(num=1,search='',order='name'){
    const request = new XMLHttpRequest()
    // request.open('GET','/category/shop?lst_price=12&?lst_brand=52')
    request.open('GET','/shop?lst_price='+lst_price+'&lst_brand='+lst_brand+'&ajax=true'+'&lst_categories='+lst_categories +'&page='+num +'&search='+search+'&order='+order)
    request.onload=function(){
            document.getElementById('product').innerHTML = this.responseText

        
    }
    request.send()
  
}
function page(num){
    filter(num)
    page_link = document.getElementsByClassName('page-item')
    for (let x = 0; x < page_link.length; x++) {
        const element = page_link[x];
        element.classList.remove('active')
    }
}
// function oreder_change(value){
//     filter(1,'',value)
//     order=value
// }


function change(check,filter_price){
    if(check.checked){
        lst_price.push(filter_price)
    }
    else{
        x= lst_price.indexOf(filter_price)
        lst_price.splice(x,1)
    }
    filter()
   

}
function brand_change(btn){
    if (btn.checked){
        lst_brand.push(btn.dataset.id)

    }
    else{
        x= lst_brand.indexOf(btn.dataset.id)
        lst_brand.splice(x,1)
    }
    filter()
}
function cat_change(btn){
    if (btn.checked){
        lst_categories.push(btn.dataset.id)

    }
    else{
        x= lst_categories.indexOf(btn.dataset.id)
        lst_categories.splice(x,1)
    }
    filter()
}




function search(){
    filter(1,document.getElementById('input_search').value)
    

}

function d(){
    prices_check = document.getElementsByName('price')
    for (let x = 0; x < prices_check.length; x++) {
        const element = prices_check[x];
        element.checked=false
        
    }
    brands_chech = document.getElementsByName('brand')
    for (let x = 0; x < brands_chech.length; x++) {
        const element = brands_chech[x];
        element.checked=false
    }
}
d()


function page_click(btn){
    filter(btn.dataset.num,'')
    scrrol()
}
function show_filter(btn,filter){
    var filter_lst = document.getElementById(filter)
    if(filter_lst.hidden==false){
            btn.classList='fas fa-plus'
            filter_lst.hidden=true
               
    }
    else{
        btn.classList='fas fa-minus'
        filter_lst.hidden=false
       
    }



}


function scrrol(){
    // document.getElementById('loader').hidden=true
    // document.getElementsByTagName('body')[0].style.opacity='1'
    // document.getElementsByTagName('body')[0].style.overflowY= "scroll";
    $('html, body').animate({scrollTop: document.getElementById('scroll').offsetTop-150}, 2000, 'easeInOutExpo');
    return false;
}