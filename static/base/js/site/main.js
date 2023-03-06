loader.hidden=false
all_site.style.opacity='0'


document.getElementsByTagName('body')[0].style.overflowY= 'hidden';

function loaded_body(){
    loader.hidden=true
    all_site.style.opacity='1'
    document.getElementsByTagName('body')[0].style.overflowY= 'scroll';
}



(function ($) {
    "use strict";
    
    // Dropdown on mouse hover
    $(document).ready(function () {
        function toggleNavbarMethod() {
            if ($(window).width() > 992) {
                $('.navbar .dropdown').on('mouseover', function () {
                    $('.dropdown-toggle', this).trigger('click');
                }).on('mouseout', function () {
                    $('.dropdown-toggle', this).trigger('click').blur();
                });
            } else {
                $('.navbar .dropdown').off('mouseover').off('mouseout');
            }
        }
        toggleNavbarMethod();
        $(window).resize(toggleNavbarMethod);
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Vendor carousel
    $('.vendor-carousel').owlCarousel({
        loop: true,
        margin: 29,
        nav: false,
        autoplay: true,
        smartSpeed: 1000,
        responsive: {
            0:{
                items:2
            },
            576:{
                items:3
            },
            768:{
                items:4
            },
            992:{
                items:5
            },
            1200:{
                items:6
            }
        }
    });


    // Related carousel
    $('.related-carousel').owlCarousel({
        loop: true,
        margin: 29,
        nav: false,
        autoplay: true,
        smartSpeed: 1000,
        responsive: {
            0:{
                items:1
            },
            576:{
                items:2
            },
            768:{
                items:3
            },
            992:{
                items:4
            }
        }
    });


    // Product Quantity
    // $('.quantity button').on('click', function () {
    //     var button = $(this);
    //     var oldValue = button.parent().parent().find('input').val();
    //     if (button.hasClass('btn-plus')) {
    //         var newVal = parseFloat(oldValue) + 1;
            
    //     } else {
    //         if (oldValue > 0) {
    //             var newVal = parseFloat(oldValue) - 1;
    //         } else {
    //             newVal = 0;
    //         }
    //     }
    //     button.parent().parent().find('input').val(newVal);
    // });
    
})(jQuery);

var box_top_sec = document.getElementById('box-top-sec')

window.onscroll = function(){
    if(document.documentElement.scrollTop>=50){
        box_top_sec.style.top=0
        box_top_sec.style.opacity='.8'
        box_top_sec.style.transition='1s'
    }
    else{
        box_top_sec.style.top='38px'
        box_top_sec.style.opacity='1'

    }
    hiden_kesho()

    // if(document.documentElement.scrollTop>=1100){
    //     div_product_sec.style.display='block'
    // }
    // else{
    //     div_product_sec.style.display='none'

    // }

};

function menu_icon_click(btn){
    btn.style.transition= '.5s';
    if(btn.style.transform== 'rotate(180deg)'){
        
        btn.style.transform= 'rotate(-1deg)';
        return
    }
    
   
    btn.style.transform= 'rotate(180deg)';

    
    
}

function hiden_kesho_cart(close=false){
    if (close){
        nav_kesho_right.style.right='-2000px'
    }
    else{
        if(kesho.style.left=='0px'){
        
            kesho.style.left='-2000px'
        }
    nav_kesho_right.style.right='0'}

}
function show_div_hidden(){
    if(nav_kesho_right.style.right=='0px'){
        
        nav_kesho_right.style.right='-2000px'
    }
    kesho.style.left='0'

}
function hiden_kesho(){
 
    kesho.style.left='-2000px'

}
function type_show(btn){

    row = document.getElementById('type-category'+btn.dataset.id)
    if(row.style.height=='100%'){
        row.style.height='0'
        row.style.transform='scaleY(0)'
        for (let x = 0; x < row.children.length; x++) {
            const element = row.children[x];
            console.log(element);
            element.hidden=true
        }
    }
    else{
        row.style.height='100%'
        row.style.transform='scaleY(1)'
        for (let x = 0; x < row.children.length; x++) {
            const element = row.children[x];
            element.hidden=false
        }
    }
   
}



hours=(new Date().getHours())

function dark(){
//     if(document.getElementsByTagName('body')[0].classList=='night'){
//      document.getElementsByTagName('body')[0].style.backgroundImage='url(" https://beauty.s3.ir-thr-at1.arvanstorage.com/1.jpg")'
 
//      document.getElementsByTagName('body')[0].classList.remove('night')
 
//     }
//     else{
//      document.getElementsByTagName('body')[0].style.backgroundImage='url("")'
//      document.getElementsByTagName('body')[0].classList.add('night')
 
//  }
if(hours>=18){
    document.getElementsByTagName('body')[0].style.backgroundImage='url("")'
    document.getElementsByTagName('body')[0].classList.add('night')

}
else{
    document.getElementsByTagName('body')[0].style.backgroundImage='url("https://beauty.s3.ir-thr-at1.arvanstorage.com/logo.jpg")'
 
    document.getElementsByTagName('body')[0].classList.remove('night')
}
 
 }
 dark()