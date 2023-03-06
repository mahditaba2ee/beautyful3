
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






var category_option = document.getElementById('category_option')
var type_option = document.getElementById('type_option')
var brand_option = document.getElementById('brand_option');
change_category(category_option.value)

function change_category(value){
        
        if(value=='add'){
            window.location='/category/addcategory'
        }

        else{
        while(brand_option.hasChildNodes()){
            brand_option.removeChild(brand_option.firstChild);
        }
        while(type_option.hasChildNodes()){
            type_option.removeChild(type_option.firstChild);
        }

        datas ={'id':value}
        request = create_request('/Category/choise',datas)
        request.onreadystatechange=function(){
            if(this.readyState==4){
                response = JSON.parse(this.responseText)
                type_lst=response['type_lst'];
                brand_lst = response['brand_lst']
                
                for (type in type_lst) {
                    type_option.add(new Option(type_lst[type],type));
                }
                for (brand in brand_lst) {
                    console.log(brand);
                    brand_option.add(new Option(brand_lst[brand],brand));
                }
               
            }
        }

    

       
                
            }
    }

function add_product(){
    images=[]
    form = document.getElementById('form_add_product')
    var datas = {'name':form['txt_name'].value,'email':form['txt_email'].value,'phone':form['txt_phone'].value,'password1':form['txt_password1'].value
    ,'password2':form['txt_password2'].value}
    

    
    request = create_request('/add',datas)
    request.onreadystatechange=function(){
        
            console.log(this.responseText);
        
    }
}












function changetype(value){
    if(value=='add'){
        var addtype =document.getElementById('addtype')
        addtype.style.display='block'
    }

    else{
        document.getElementById('addtype').style.display='none'

    }
}
        
function changebreand(value){
    if (value=='add'){
        alert()
        document.getElementById('addbrand').style.display='block'
      
    }
    else{
        document.getElementById('addbrand').style.display='none'

    }
    

}

// function send(btn){
//     if(btn.dataset.kind=='category'){
//     $.post('/category/addbrand',{
//         name_brand:document.getElementById('brand-name').value,
//             category:selected.value,
//         },
//         function(data){
//             console.log(data['name'])
//             if (data['status']=='ok'){
//                 document.getElementById('addbrand').style.display='none'
//                 selectElement.add(new Option(document.getElementById('brand-name').value));


//             }
//         }
//         )}
//     if(btn.dataset.kind=='type'){
//         $.post('/category/addtype',{
//             name_type:document.getElementById('type-name').value,
//             category:selected.value,
//         },function(data){
//             if(data['status']=='ok'){
//                 document.getElementById('addtype').style.display='none'
//                 type.add(new Option(document.getElementById('type-name').value));

//             }
//         })
//     }
// }