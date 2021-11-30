$(document).ready(function(){
    $(".owl-carousel").owlCarousel();
  });

$('.owl-carousel').owlCarousel({
    loop:true,
    margin:10,
    dots: false,
    autoplay:true,
    autoplayTimeout:3000,
    autoplayHoverPause:true,
    responsiveClass:true,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:2
        },
        1000:{
            items:3
        },
        1250:{
            items:4
        }
    }
})