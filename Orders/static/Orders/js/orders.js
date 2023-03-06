

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
document.getElementById('nav-order').classList.add('active')

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



function order_click(btn){
    var id = btn.dataset.id
    datas = {'order_id':id}
    request = create_request('/Orders/orders',datas)
    request.onreadystatechange=function(){
        if(this.readyState==4){
            response = JSON.parse(this.responseText)
            if (response['status_order']=='order_view'){
            var tbl_name = 'tbl'+id
            tbl = document.getElementById(tbl_name)
            tbl.animate({scrollTop: 0}, 1500, 'easeInOutExpo');
            tbl.classList.add('animate__animated', 'animate__bounceOutLeft');
        
            tbl.addEventListener('animationend', () => {
          tbl.hidden=true
        });
        }}
    }
  
   
}
       



function printer_order(btn){
    var id = btn.dataset.id
    var tbl_name = 'tbl'+id
    tbl = document.getElementById(tbl_name).innerHTML
    var WinPrint = window.open("", "title", "attributes");
    WinPrint.document.write(tbl);
    WinPrint.document.close();
    WinPrint.focus();
    WinPrint.print();
    WinPrint.close();

    
}