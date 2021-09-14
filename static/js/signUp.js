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

});