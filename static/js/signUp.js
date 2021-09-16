$(document).ready(function(){

$('#goToSignUp').click(function(){
    $('#box').animate({
        height:'409px'
    });
    
    $('#signIn').fadeOut();
    if($('#signIn').hide()){$('#signUp').fadeIn(800);}
    
});

$('#signUp .back').click(function(){
    $('#box').animate({
        height:'353px'
    });
    
    $('#signUp').fadeOut();
    if($('#signUp').hide()){$('#signIn').fadeIn(800);}
    
});

$('.suID input').on("change keyup paste", function(){
    $('.suID #wrong').css('opacity','0');
})
$('.suPW input').on("change keyup paste", function(){
    $('.suPW .wrong').css('opacity','0');
})





});