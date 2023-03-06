function view_list(){
    const request = new XMLHttpRequest()
    request.open('GET','?is_ajax=True')
    request.onload=function(){
        
            document.getElementById('product').innerHTML = this.responseText

        
    }
    request.send()
}
function product_search(btn){
    var name = btn.dataset.name
    var cat = btn.dataset.category
    var slug = btn.dataset.slug
    window.location='/search/'+cat+'/'+slug+'/'+name
}


function page_change(btn){
    // const request = new XMLHttpRequest()
    // request.open('GET','?order='+document.getElementById('order_value').value+'&page='+btn.dataset.num+'&is_ajax='+true)

    // request.onreadystatechange=function(){
        
    // document.getElementById('products').innerHTML=this.responseText
   
    
    // }
    // request.send()
    window.location='?order='+document.getElementById('order_value').value+'&page='+btn.dataset.num
}
function oreder_change(value){
    window.location='?order='+value 
}