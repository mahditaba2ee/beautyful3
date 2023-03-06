document.getElementById('nav-type').classList.add('active')


var id_btn = 0
function type_product_click(btn , page=1,order='name'){
    
        id_btn = btn
        const request = new XMLHttpRequest()
        
        request.open('GET','/type/products/?type='+btn.dataset.id + '&page='+page+'&order='+order )
        request.onload=function(){
            console.log(this.responseText);
         
                document.getElementById('product').innerHTML = this.responseText  
                
        }
        request.send()
    
    
    
    
}

$('.show-type').click(function () {
    $('html, body').animate({scrollTop: document.getElementById('show-type').offsetTop}, 2000, 'easeInOutExpo');
    return false;
});





order = 'name'
function page_click(btn){
    type_product_click(id_btn,btn.dataset.num,order)
}

function oreder_change(value){
    type_product_click(id_btn,1,value)
    order = value
}